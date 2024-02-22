# -*- coding: utf-8 -*-
import structlog
logger = structlog.get_logger("plugin")


class ClientException(Exception):
    """
    An exception which marks an error made by the plugin invoker.

    Some examples of when to use this are:
    - Malformed/Incorrect input data
    - External HTTP server throws a 400 level error

    """

    pass


class ServerException(Exception):
    """
    An Exception which marks an error made by an external server.

    Some examples of when to use this are:
    - External server throws a 500 Error

    """

    pass


class LoggedException(Exception):
    """
    An Exception which holds the step output dictionary.
    """

    def __init__(self, ex, output):
        super(LoggedException, self).__init__(ex)
        self.ex = ex
        self.output = output


class ConnectionTestException(Exception):
    """
    An Exception which marks an error that occurred during a connection test.

    This Exception provides a method for consistent and well-handled error messaging.
    """

    class Preset(object):
        """
        Constants available for use as preset arguments to the initializer
        """

        API_KEY = "api_key"
        UNAUTHORIZED = "unauthorized"
        RATE_LIMIT = "rate_limit"
        USERNAME_PASSWORD = "username_password"
        NOT_FOUND = "not_found"
        SERVER_ERROR = "server_error"
        SERVICE_UNAVAILABLE = "service_unavailable"
        INVALID_JSON = "invalid_json"
        UNKNOWN = "unknown"
        BASE64_ENCODE = "base64_encode"
        BASE64_DECODE = "base64_decode"
        TIMEOUT = "timeout"
        BAD_REQUEST = "bad_request"
        INVALID_CREDENTIALS = "invalid_credentials"

    # Dictionary of cause messages
    causes = {
        Preset.API_KEY: "Invalid API key provided.",
        Preset.UNAUTHORIZED: "The account configured in your connection is unauthorized to access this service.",
        Preset.RATE_LIMIT: "The account configured in your plugin connection is currently rate-limited.",
        Preset.USERNAME_PASSWORD: "Invalid username or password provided.",
        Preset.NOT_FOUND: "Invalid or unreachable endpoint provided.",
        Preset.SERVER_ERROR: "Server error occurred",
        Preset.SERVICE_UNAVAILABLE: "The service is currently unavailable.",
        Preset.INVALID_JSON: "Received an unexpected response from the server.",
        Preset.UNKNOWN: "Something unexpected occurred.",
        Preset.BASE64_ENCODE: "Unable to base64 encode content due to incorrect padding length.",
        Preset.BASE64_DECODE: "Unable to base64 decode content due to incorrect padding length.",
        Preset.TIMEOUT: "The connection timed out.",
        Preset.BAD_REQUEST: "The server is unable to process the request.",
        Preset.INVALID_CREDENTIALS: "Authentication failed: invalid credentials.",
    }

    # Dictionary of assistance/remediation messages
    assistances = {
        Preset.API_KEY: "Verify your API key configured in your connection is correct.",
        Preset.UNAUTHORIZED: "Verify the permissions for your account and try again.",
        Preset.RATE_LIMIT: "Adjust the time between requests if possible.",
        Preset.USERNAME_PASSWORD: "Verify your username and password are correct.",
        Preset.NOT_FOUND: "Verify the URLs or endpoints in your configuration are correct.",
        Preset.SERVER_ERROR: "Verify your plugin connection inputs are correct and not malformed and try again. "
        "If the issue persists, please contact support.",
        Preset.SERVICE_UNAVAILABLE: "Try again later. If the issue persists, please contact support.",
        Preset.INVALID_JSON: "(non-JSON or no response was received).",
        Preset.UNKNOWN: "Check the logs and if the issue persists please contact support.",
        Preset.BASE64_ENCODE: "This is likely a programming error, if the issue persists please contact support.",
        Preset.BASE64_DECODE: "This is likely a programming error, if the issue persists please contact support.",
        Preset.TIMEOUT: "This is likely a network error. "
        "Verify the network activity. If the issue persists, please contact support.",
        Preset.BAD_REQUEST: "Verify your plugin input is correct and not malformed and try again. "
        "If the issue persists, please contact support.",
        Preset.INVALID_CREDENTIALS: "Please verify the credentials for your account and try again.",
    }

    def __init__(self, cause=None, assistance=None, data=None, preset=None):
        """
        Initializes a new ConnectionTestException. User must supply all punctuation/grammar.
        :param cause: Cause of the error. Leave empty if using preset.
        :param assistance: Possible remediation steps for the error. Leave empty if using preset.
        :param data: Possible response data related to the error.
        :param preset: Preset error and remediation steps to use.
        """

        self.preset = preset

        if preset:
            self.cause, self.assistance = self.causes[preset], self.assistances[preset]
        else:
            self.cause = cause if cause else ""
            self.assistance = assistance if assistance else ""

        self.data = str(data) if data else ""

        # Safeguard to ensure the exception is logged across all plugins even if the plugin
        # itself does not call `self.logger.error(<error info>)`
        params = ["cause", "assistance", "data", "preset"]
        info_log = ", ".join([f"{atr}='{getattr(self, atr)}'" for atr in params if getattr(self, atr)])
        logger.error(f"Plugin exception instantiated. {info_log}")

    def __str__(self):
        if self.data:
            return "Connection test failed!\n\n{cause} {assistance} Response was: {data}".format(
                cause=self.cause, assistance=self.assistance, data=self.data
            )
        else:
            return "Connection test failed!\n\n{cause} {assistance}".format(
                cause=self.cause, assistance=self.assistance
            )


class PluginException(ConnectionTestException):
    def __str__(self):
        if self.data:
            return "An error occurred during plugin execution!\n\n{cause} {assistance} Response was: {data}".format(
                cause=self.cause, assistance=self.assistance, data=self.data
            )
        else:
            return "An error occurred during plugin execution!\n\n{cause} {assistance}".format(
                cause=self.cause, assistance=self.assistance
            )
