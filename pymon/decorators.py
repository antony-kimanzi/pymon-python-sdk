import functools
import time
from typing import Optional, Callable, Any

from pymon.client import Client


def monitor(check_name: str, client: Optional[Client] = None):
    """
    Decorator to monitor a synchronous function.

    Usage:
        @monitor("nightly-backup")
        def backup():
            ...
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            _client = client or Client()
            start_time = time.time()

            try:
                # Run the user's function
                result = func(*args, **kwargs)

                # If iy succeeds, calculate time and send success ping
                duration_ms = int((time.time() - start_time) * 1000)
                _client.ping_success(duration_ms)
                return result

            except Exception as e:
                # If it fails, report the failure, then re-raise the error
                _client.report_failure(e)
                raise e

        return wrapper
    return decorator

def monitor_async(check_name: str, client: Optional[Client] = None):
    """
       Decorator to monitor an asynchronous function.

       Usage:
           @monitor_async("daily-report")
           async def generate_report():
               ...
       """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            _client = client or Client()
            start_time = time.time()

            try:
                # Run the user's async function
                result = await func(*args, **kwargs)

                # Send success ping
                duration_ms = int((time.time() - start_time) * 1000)
                _client.ping_success(duration_ms)

                return result

            except Exception as e:
                # Report failure, then re-raise
                _client.report_failure(e)
                raise e

        return wrapper
    return decorator