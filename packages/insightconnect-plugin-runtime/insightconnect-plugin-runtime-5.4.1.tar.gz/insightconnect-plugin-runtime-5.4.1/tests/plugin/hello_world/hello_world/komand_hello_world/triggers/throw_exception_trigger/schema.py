# GENERATED BY KOMAND SDK - DO NOT EDIT
import insightconnect_plugin_runtime
import json


class ThrowExceptionTriggerInput(insightconnect_plugin_runtime.Input):
    schema = json.loads(
        """
   {
  "type": "object",
  "title": "Variables",
  "properties": {
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


class ThrowExceptionTriggerOutput(insightconnect_plugin_runtime.Output):
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
