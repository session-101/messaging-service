# from typing import Union
import uvicorn
import uuid
import sys
import enum
import json
import logging
import time
import dramatiq
from fastapi import FastAPI, Request, Response

from fastapi import FastAPI
from app.routers import messages

class LogType(enum.Enum):
    REQUEST_REPORT = 'REQUEST_REPORT'
    TRACE = 'TRACE'
    COMMAND_REPORT = 'COMMAND_REPORT'
    EVENT_REPORT = 'EVENT_REPORT'

class LogLevelIntegers(enum.Enum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0


logging_config: dict = {
    'version': 1,
    'disable_existing_loggers': False,
}

logging.config.dictConfig(logging_config)

default_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s %(lineno)d: %(message)s')
default_handler = logging.StreamHandler(stream=sys.stdout)
default_handler.setLevel('DEBUG')
default_handler.setFormatter(default_formatter)

api_logger = logging.getLogger(__name__)
api_logger.setLevel(logging.DEBUG)
api_logger.addHandler(default_handler)
api_logger.disabled = False

app = FastAPI()
app.include_router(messages.router)

app.dramatiq_broker = dramatiq.get_broker()

# Logging
@app.middleware('http')
async def request_logger(request: Request, call_next):
    # Request ID should be set at the ingress, but for now we will set it.
    request.state.__setattr__('request_id', str(uuid.uuid4()))
    start_time = time.time()
    request.state.__setattr__('start_time', start_time)

    response = await call_next(request)

    await log_request(request=request, response=response, duration=time.time() - start_time)
    return response

async def log_request(request: Request, response: Response, duration: float):
    log_data = {
        'request_id': request.state.request_id,
        'timestamp': time.time(),
        'log_type': LogType.REQUEST_REPORT.value,
        # TODO: Figure out this field. Where will it come from?
        'caller_identifier': '',
        'endpoint': request.url.path,
        'http_method': request.method,
        'request': {
            'path_params': request.path_params,
            'query_params': dict(request.query_params)
        },
        'client_ip': request.headers.get('x_forwarded_for', ''),
        'call_duration': duration,
        'call_status': response.status_code,
        'trace_id': request.state.__dict__.get('trace_id')
    }
    api_logger.info(json.dumps(log_data))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
