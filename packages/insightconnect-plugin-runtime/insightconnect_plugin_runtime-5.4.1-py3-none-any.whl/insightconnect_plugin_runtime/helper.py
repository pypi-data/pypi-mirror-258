# -*- coding: utf-8 -*-
import base64
import hashlib
import logging
import os
import re
import shlex
import ssl
import subprocess
import time
from datetime import datetime, timedelta
from io import IOBase
from typing import Any, Callable, Dict, List, Union
from urllib import request

import requests

from insightconnect_plugin_runtime.exceptions import PluginException

CAMEL_CASE_REGEX = r"\b[a-z0-9]+([A-Z][a-z]+[0-9]*)*\b"
CAMEL_CASE_ACRONYM_REGEX = r"\b[a-z0-9]+([A-Z]+[0-9]*)*\b"
PASCAL_CASE_REGEX = r"\b[A-Z][a-z]+[0-9]*([A-Z][a-z]+[0-9]*)*\b"

DEFAULTS_HOURS_AGO = 24


def extract_value(begin, key, end, s):
    """
    Returns a string from a given key/pattern using provided regular expressions.

    It takes 4 arguments:
    * begin: a regex/pattern to match left side
    * key: a regex/pattern that should be the key
    * end: a regex/pattern to match the right side
    * s: the string to extract values from

    Example: The following will use pull out the /bin/bash from the string s
    s = '\nShell: /bin/bash\n'
    shell = get_value(r'\s', 'Shell', r':\s(.*)\s', s)

    This function works well when you have a list of keys to iterate through where the pattern is the same.
    """

    regex = begin + key + end
    r = re.search(regex, s)
    if hasattr(r, "group"):
        if r.lastindex == 1:
            return r.group(1)
    return None


def clean_dict(dictionary):
    """
    Returns a new but cleaned dictionary.

    * Keys with None type values are removed
    * Keys with empty string values are removed

    This function is designed so we only return useful data
    """

    newdict = dict(dictionary)
    for key in dictionary.keys():
        if dictionary.get(key) is None:
            del newdict[key]
        if dictionary[key] == "":
            del newdict[key]
    return newdict


def clean_list(lst):
    """
    Returns a new but cleaned list.

    * None type values are removed
    * Empty string values are removed

    This function is designed so we only return useful data
    """

    newlist = list(lst)
    for i in lst:
        if i is None:
            newlist.remove(i)
        if i == "":
            newlist.remove(i)
    return newlist


def clean(obj):
    """
    Returns a new but cleaned JSON object.

    * Recursively iterates through the collection
    * None type values are removed
    * Empty string values are removed

    This function is designed so we only return useful data
    """

    cleaned = clean_list(obj) if isinstance(obj, list) else clean_dict(obj)

    # The only *real* difference here is how we have to iterate through these different collection types
    if isinstance(cleaned, list):
        for key, value in enumerate(cleaned):
            if isinstance(value, list) or isinstance(value, dict):
                cleaned[key] = clean(value)
    elif isinstance(cleaned, dict):
        for key, value in cleaned.items():
            if isinstance(value, dict) or isinstance(value, list):
                cleaned[key] = clean(value)

    return cleaned


def return_non_empty(input_dict: Dict[str, Any]) -> Union[Dict[Any, Any], Any]:
    """
    return_non_empty. Cleans the dictionary recursively.

    :param input_dict: Input dictionary to be cleaned.
    :type input_dict: Dict[str, Any]

    :return: Returns a cleaned up dictionary containing only no empty values.
    :rtype: Union[Dict[Any, Any], None]
    """

    temp_dict = {}
    for key, value in input_dict.items():
        if value is not None and value != "" and value != []:
            if isinstance(value, dict):
                return_dict = return_non_empty(value)
                if return_dict:
                    temp_dict[key] = return_dict
            elif isinstance(value, list):
                return_value = [
                    return_non_empty(element) if isinstance(element, dict) else element
                    for element in value
                ]
                return_value = list(filter(None, return_value))
                if return_value:
                    temp_dict[key] = return_value
            else:
                temp_dict[key] = value
    return temp_dict


def convert_to_snake_case(input_string: str) -> str:
    """
    convert_to_snake_case. Convert input string Camel Case name to Snake Case.

    :param input_string: Input string in Camel case format.
    :type: str

    :return: Converted input value from Camel case to Snake case.
    :rtype: str
    """

    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", input_string).lower()


def convert_dict_to_snake_case(
    input_dict: Union[List[Dict[str, Any]], Dict[str, Any]]
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    convert_dict_to_snake_case. Recursively convert a dictionary or nested dictionary keys from Camel to Snake case.

    :param input_dict: Input dictionary for keys to be converted to Snake case.
    :type: Union[List[Dict[str, Any]], Dict[str, Any]]

    :return: Dictionary of all key names converted from Camel to Snake case.
    :rtype: Union[List[Dict[str, Any]], Dict[str, Any]]
    """

    if isinstance(input_dict, list):
        return [
            convert_dict_to_snake_case(element)
            if isinstance(element, (dict, list))
            else element
            for element in input_dict
        ]
    return {
        convert_to_snake_case(key): convert_dict_to_snake_case(value)
        if isinstance(value, (dict, list))
        else value
        for key, value in input_dict.items()
    }


def get_hashes_string(s):
    """Return a dictionary of hashes for a string."""
    s = s.encode("utf-8")
    hashes = {
        "md5": hashlib.md5(s).hexdigest(),
        "sha1": hashlib.sha1(s).hexdigest(),
        "sha256": hashlib.sha256(s).hexdigest(),
        "sha512": hashlib.sha512(s).hexdigest(),
    }
    return hashes


def convert_to_camel_case(provided_string: str) -> str:
    """
    to_camel_case. Convert a provided_string from Snake to Camel case.

    :param provided_string: Input string to be converted to Camel case.
    :type: str

    :return: String converted rom Snake to Camel case.
    :rtype: str
    """

    if re.match(CAMEL_CASE_REGEX, provided_string):
        return provided_string
    if re.match(PASCAL_CASE_REGEX, provided_string):
        return provided_string[0].lower() + provided_string[1:]
    if re.match(CAMEL_CASE_ACRONYM_REGEX, provided_string):
        words = re.split(
            r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z0-9])(?=[a-z])", provided_string
        )
        result = "".join([w.title() for w in words])
        return result[0].lower() + result[1:]
    init, *temp = provided_string.split("_")
    result = "".join([init.lower(), *map(str.title, temp)])
    return result


def convert_dict_to_camel_case(to_modify: Union[dict, list]) -> Union[dict, list]:
    """
    convert_dict_to_camel_case. Convert a provided_string from Snake to Camel case.

    :param to_modify: Input dict or list for keys/elements to be converted to Camel case.
    :type: Union[dict, list]

    :return: Dictionary or List with keys/elements converted from Snake to Camel case.
    :rtype: Union[dict, list]
    """

    case_method = convert_to_camel_case
    if isinstance(to_modify, list):
        return [convert_dict_to_camel_case(element) for element in to_modify]
    elif isinstance(to_modify, dict):
        output_dict = {}
        for key, value in to_modify.items():
            output_dict[case_method(key)] = convert_dict_to_camel_case(value)
        return output_dict
    else:
        return to_modify


def backoff_function(attempt: int) -> float:
    """backoff_function. Back-off function used in rate_limiting retry decorator.

    :param attempt: Current attempt value in retry function.
    :type attempt: int

    :returns: time sleep value for next connection attempt.
    :rtype: float
    """

    return 2 ** (attempt * 0.6)


def rate_limiting(
    max_tries: int, back_off_function: Callable = backoff_function
) -> Union[dict, None]:
    """rate_limiting. This decorator allows to work API call with rate limiting by using exponential backoff function.
    Decorator needs to have max_tries argument entered obligatory.

    :param max_tries: Maximum number of retries calling API function.
    :type max_tries: int

    :param back_off_function: Backoff function for time delay. Defaults to backoff_function.
    :type back_off_function: Callable

    :returns: API call function data or None.
    :rtype: Union[dict, None]
    """

    def _decorate(func: Callable):
        def _wrapper(self, *args, **kwargs):
            retry = True
            attempts_counter, delay = 0, 0
            while retry and attempts_counter < max_tries:
                if attempts_counter:
                    time.sleep(delay)
                try:
                    retry = False
                    return func(self, *args, **kwargs)
                except PluginException as error:
                    attempts_counter += 1
                    delay = back_off_function(attempts_counter)
                    if (
                        error.cause
                        == PluginException.causes[PluginException.Preset.RATE_LIMIT]
                    ):
                        logging.info(
                            f"Rate limiting error occurred. Retrying in {delay:.1f} seconds ({attempts_counter}/{max_tries})"
                        )
                        retry = True
            return func(self, *args, **kwargs)

        return _wrapper

    return _decorate


def get_time_now() -> datetime:
    """
    get_time_now. Returns the current time datetime object.

    :return: Datetime object containing current time.
    :rtype: datetime
    """

    return datetime.now()


def get_time_hours_ago(hours_ago: int = DEFAULTS_HOURS_AGO) -> datetime:
    """
    get_time_24_hours_ago. Retrieves the time x hours ago.

    :param hours_ago: Number of hours ago to return time. Defaults to DEFAULTS_HOURS_AGO.
    :type: int

    :return: Datetime object contains the time x hours ago.
    :rtype: datetime
    """

    return get_time_now() - timedelta(hours=hours_ago)


def check_hashes(src, checksum):
    """Return boolean on whether a hash matches a file or string."""

    if type(src) is str:
        hashes = get_hashes_string(src)
    else:
        logging.error("CheckHashes: Argument must be a string")
        raise Exception("CheckHashes")
    for alg in hashes:
        if hashes[alg] == checksum:
            return True
    logging.info("CheckHashes: No checksum match")
    return False


def check_cachefile(cache_file):
    """Return boolean on whether cachefile exists."""

    cache_dir = "/var/cache"
    if cache_dir not in cache_file:
        cache_file = cache_dir + "/" + cache_file
    if os.path.isdir(cache_dir):
        if os.path.isfile(cache_file):
            logging.info("CheckCacheFile: File %s exists", cache_file)
            return True
        logging.info("CheckCacheFile: File %s did not exist", cache_file)
    return False


def open_file(file_path):
    """Return file object if it exists."""

    dirname = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    if os.path.isdir(dirname):
        if os.path.isfile(file_path):
            f = open(file_path, "rb")
            if isinstance(f, IOBase):
                return f
            return None
        else:
            logging.info("OpenFile: File %s is not a file or does not exist ", filename)
    else:
        logging.error(
            "OpenFile: Directory %s is not a directory or does not exist", dirname
        )


def open_cachefile(cache_file, append=False):
    """Return file object if cachefile exists, create and return new cachefile if it doesn't exist."""

    cache_dir = "/var/cache"
    if cache_dir not in cache_file:
        cache_file = cache_dir + "/" + cache_file
    if os.path.isdir(cache_dir):
        if os.path.isfile(cache_file):
            f = open(cache_file, "a+" if append else "r+")
            logging.info("OpenCacheFile: %s exists, returning it", cache_file)
        else:
            if not os.path.isdir(os.path.dirname(cache_file)):
                os.makedirs(os.path.dirname(cache_file))
            f = open(cache_file, "w+")  # Open once to create the cache file
            f.close()
            logging.info("OpenCacheFile: %s created", cache_file)
            f = open(cache_file, "a+" if append else "r+")
        return f
    logging.error("OpenCacheFile: %s directory or does not exist", cache_dir)


def remove_cachefile(cache_file):
    """Returns boolean on whether cachefile was removed."""

    cache_dir = "/var/cache"
    if cache_dir not in cache_file:
        cache_file = cache_dir + "/" + cache_file
    if os.path.isdir(cache_dir):
        if os.path.isfile(cache_file):
            os.remove(cache_file)
            return True
        logging.info("RemoveCacheFile: Cache file %s did not exist", cache_file)
    return False


def lock_cache(lock_file):
    """Returns boolean on whether lock was created."""

    lock_dir = "/var/cache/lock"
    if not os.path.isdir(lock_dir):
        os.makedirs(lock_dir)
    if not lock_file.startswith("/"):
        lock_file = lock_dir + "/" + lock_file
    if os.path.isdir(lock_dir):
        while os.path.isfile(lock_file):
            pass
        if not os.path.isdir(os.path.dirname(lock_file)):
            os.makedirs(os.path.dirname(lock_file))
        f = open(lock_file, "w")
        f.close()
        logging.info("Cache lock %s created", lock_file)
        return True
    logging.info("Cache lock %s failed, lock not created", lock_file)
    return False


def unlock_cache(lock_file, wait_time):
    """
    Returns boolean on whether lock was released.

    Wait_time value used to wait before unlocking and is measured in seconds
    """

    lock_dir = "/var/cache/lock"
    if not lock_file.startswith("/"):
        lock_file = lock_dir + "/" + lock_file
    if os.path.isdir(lock_dir):
        if os.path.isfile(lock_file):
            time.sleep(wait_time)
            os.remove(lock_file)
            return True
        logging.info("Cache unlock %s failed, lock not released", lock_file)
    return False


def open_url(url, timeout=None, verify=True, **kwargs):
    """
    Returns a urllib.request object given a URL as a string.

    Optional parameters include
    * timeout - Timeout value for request as int
    * verify  - Certificate validation as boolean
    * headers - Add many headers as Header_Name='Val', Header_Name2='Val2'
    """

    req = request.Request(url)
    if type(kwargs) is dict:
        for key in kwargs.keys():
            header = key.replace("_", "-")
            req.add_header(header, kwargs[key])
    try:
        if verify:
            ctx = ssl.create_default_context(cafile=os.environ["SSL_CERT_FILE"])
            urlobj = request.urlopen(req, timeout=timeout, context=ctx)
        else:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            urlobj = request.urlopen(req, timeout=timeout, context=ctx)
        return urlobj
    except request.HTTPError as e:
        logging.error("HTTPError: %s for %s", str(e.code), url)
        if e.code == 304:
            return None
    except request.URLError as e:
        logging.error("URLError: %s for %s", str(e.reason), url)
    raise Exception("GetURL Failed")


def check_url(url):
    """
    Return boolean on whether we can access url successfully.

    We submit an HTTP HEAD request to check the status. This way we don't download the file for performance.
    If the server doesn't support HEAD we try a Range of bytes so we don't download the entire file.
    """

    resp = None
    try:
        # Try HEAD request first
        resp = requests.head(url)
        if 200 <= resp.status_code <= 399:
            return True

        # Try Range request as secondary option
        hrange = {"Range": "bytes=0-2"}
        req = request.Request(url, headers=hrange)
        ctx = ssl.create_default_context(cafile=os.environ["SSL_CERT_FILE"])
        resp = request.urlopen(req, context=ctx)
        if 200 <= resp.code <= 299:
            return True

    except requests.exceptions.HTTPError:
        logging.error(
            "Requests: HTTPError: status code %s for %s",
            str(resp.status_code) if resp else None,
            url,
        )
    except requests.exceptions.Timeout:
        logging.error("Requests: Timeout for %s", url)
    except requests.exceptions.TooManyRedirects:
        logging.error("Requests: TooManyRedirects for %s", url)
    except requests.ConnectionError:
        logging.error("Requests: ConnectionError for %s", url)
    return False


def exec_command(command):
    """Return dict with keys stdout, stderr, and return code of executed subprocess command."""

    try:
        p = subprocess.Popen(
            shlex.split(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        )
        stdout = p.stdout.read()
        stderr = p.stderr.read()
        rcode = p.poll()
        return {"stdout": stdout, "stderr": stderr, "rcode": rcode}
    except OSError as e:
        logging.error(
            "SubprocessError: %s %s: %s", str(e.filename), str(e.strerror), str(e.errno)
        )
    raise Exception("ExecCommand")


def encode_string(s):
    """Returns a base64 encoded string given a string."""

    if type(s) is str:
        _bytes = base64.b64encode(s.encode("utf-8"))
        return _bytes
    return None


def encode_file(file_path):
    """Return a string of base64 encoded file provided as an absolute file path."""

    f = None
    try:
        f = open_file(file_path)
        if isinstance(f, IOBase):
            efile = base64.b64encode(f.read())
            return efile
        return None
    except (IOError, OSError) as e:
        logging.error("EncodeFile: Failed to open file: %s", e.strerror)
        raise Exception("EncodeFile")
    finally:
        if isinstance(f, IOBase):
            f.close()


def check_url_modified(url):
    """
    Return boolean on whether the url has been modified.

    We submit an HTTP HEAD request to check the status. This way we don't download the file for performance.
    """

    resp = None
    try:
        resp = requests.head(url)
        resp.raise_for_status()
        if resp.status_code == 304:
            return False
        if resp.status_code == 200:
            return True
    except requests.exceptions.HTTPError:
        logging.error(
            "Requests: HTTPError: status code %s for %s",
            str(resp.status_code) if resp else None,
            url,
        )
    except requests.exceptions.Timeout:
        logging.error("Requests: Timeout for %s", url)
    except requests.exceptions.TooManyRedirects:
        logging.error("Requests: TooManyRedirects for %s", url)
    except requests.ConnectionError:
        logging.error("Requests: ConnectionError for %s", url)
    return False


def get_url_content_disposition(headers):
    """Return filename as string from content-disposition by supplying requests headers."""

    # Dict is case-insensitive
    for key, value in headers.items():
        if key.lower() == "content-disposition":
            filename = re.findall("filename=(.+)", value)
            return str(filename[0].strip('"'))
    return None


def get_url_path_filename(url):
    """Return filename from url as string if we have a file extension, otherwise return None."""

    if url.find("/", 9) == -1:
        return None
    name = os.path.basename(url)
    try:
        for n in range(-1, -5, -1):
            if name[n].endswith("."):
                return name
    except IndexError:
        logging.error("Range: IndexError: URL basename is short: %s of %s", name, url)
        return None
    return None


def get_url_filename(url):
    """Return filename as string from url by content-disposition or url path, or return None if not found."""

    resp = None
    try:
        resp = requests.head(url)
        resp.raise_for_status()
        name = get_url_content_disposition(resp.headers)
        if name is not None:
            return name
        name = get_url_path_filename(url)
        if name is not None:
            return name
        return None
    except requests.exceptions.MissingSchema:
        logging.error("Requests: MissingSchema: Requires ftp|http(s):// for %s", url)
    except requests.exceptions.HTTPError:
        logging.error(
            "Requests: HTTPError: status code %s for %s",
            str(resp.status_code) if resp else None,
            url,
        )
    except requests.exceptions.Timeout:
        logging.error("Requests: Timeout for %s", url)
    except requests.exceptions.TooManyRedirects:
        logging.error("Requests: TooManyRedirects for %s", url)
    except requests.ConnectionError:
        logging.error("Requests: ConnectionError for %s", url)
