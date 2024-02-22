import insightconnect_plugin_runtime
import json


class ThrowExceptionInput(insightconnect_plugin_runtime.Input):
    schema = json.loads(
        """
   {
  "type": "object",
  "title": "Variables",
  "properties": {
    "bad_request": {
      "type": "boolean",
      "title": "Bad Request",
      "description": "Throw a bad request Plugin Exception if true",
      "default": false,
      "order": 2
    },
    "name": {
      "type": "string",
      "title": "Name",
      "description": "The Name",
      "order": 1
    }
  },
  "required": [
    "name"
  ]
}
    """
    )

    def __init__(self):
        super(self.__class__, self).__init__(self.schema)


class ThrowExceptionOutput(insightconnect_plugin_runtime.Output):
    schema = json.loads(
        """
   {
  "type": "object",
  "title": "Variables",
  "properties": {
    "message": {
      "type": "string",
      "title": "Message",
      "description": "The greeting",
      "order": 1
    }
  },
  "required": [
    "message"
  ]
}
    """
    )

    def __init__(self):
        super(self.__class__, self).__init__(self.schema)
