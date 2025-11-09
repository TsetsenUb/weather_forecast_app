import time
from fastapi import Request

from app.core.logger import logger


async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(f"Request started: {request.method} {request.url}")

    try:
        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(
            f"Request completed: {request.method} {request.url} - "
            f"Status: {response.status_code} - "
            f"Duration: {process_time:.3f}s"
        )
        return response

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {request.url} - "
            f"Error: {type(e).__name__}: {str(e)} - "
            f"Duration: {process_time:.3f}s"
        )
        raise
