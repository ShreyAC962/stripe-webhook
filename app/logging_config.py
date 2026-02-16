import logging

import json


class JsonFormatter(logging.Formatter):


    def format(self, record):

        log_record = {

            "level": record.levelname,

            "message": record.msg,

            "event_id": getattr(record, "event_id", None)

        }

        return json.dumps(log_record)


logger = logging.getLogger() # Get the root logger

handler = logging.StreamHandler() # Create a stream handler to output logs to the console

handler.setFormatter(JsonFormatter()) # Set the custom JSON formatter for the handler

logger.addHandler(handler) # Add the handler to the logger

logger.setLevel(logging.INFO) # Set the logging level to INFO (you can adjust this as needed)
