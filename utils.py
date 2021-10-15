import asyncio
import random

import fastapi.logger as logger
from starlette.requests import Request

'''
Get status as an event generator
'''
status_stream_delay = 5  # second
status_stream_retry_timeout = 30000  # milisecond

logger = logger.logger


async def compute_status(param1: str):
    number = random.randint(0, 100)
    if number < 96:
        return dict(number=number, param=param1)
    else:
        return dict(some_end_condition=True, param=param1)


async def status_event_generator(request: Request, param1: str):
    previous_status = None
    while True:
        if await request.is_disconnected():
            logger.debug('Request disconnected')
            break

        if previous_status and 'some_end_condition' in previous_status and previous_status['some_end_condition']:
            logger.debug('Request completed. Disconnecting now')
            yield {
                "event": "end",
                "data": ''
            }
            break

        current_status = await compute_status(param1)
        if previous_status != current_status:
            yield {
                "event": "update",
                "retry": status_stream_retry_timeout,
                "data": current_status
            }
            previous_status = current_status
            logger.debug('Current status :%s', current_status)
        else:
            logger.debug('No change in status...')

        await asyncio.sleep(status_stream_delay)
