from datetime import datetime, timezone
import os
import traceback
from typing import Optional, Dict, Any
import requests


class Client:
    """Client for communicating with the PyMon API."""

    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            timeout: int = 5,
    ):
        # Read from environment variables if not passed explicitly
        self.api_key = api_key or os.environ.get("PYMON_API_KEY")
        self.base_url = base_url or os.environ.get("PYMON_API_BASE_URL", "http://localhost:8080/api/v1")
        self.timeout = timeout

        if not self.api_key:
            raise ValueError(
                "PyMon API Key is required."
                "Set the PYMON_API_KEY environment variable or pass api_key"
            )

    def _get_headers(self) -> Dict[str, str]:
            return {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "pymon-python/0.1.0",
            }

    def ping_success(self, duration_ms: int) -> bool:
            """Send a success ping tp the backend"""
            try:
                url = f"{self.base_url}/ping/{self.api_key}"
                payload = {"durationMs" : duration_ms}

                response = requests.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return True
            except requests.RequestException as e:
                print(f"DEBUG: Ping failed -> {e}")  # ADD THIS
                return False

    def report_failure(self, error: Exception) -> bool:
            """Report a failure with the full stack trace"""
            try:
                url = f"{self.base_url}/ping/{self.api_key}/fail"

                payload = {
                    "errorType": type(error).__name__,
                    "errorMessage": str(error),
                    "stackTrace": traceback.format_exc(),
                    "occurredAt": datetime.now(timezone.utc).isoformat()
                }

                response = requests.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return True
            except requests.RequestException as e:
                print(f"DEBUG: Failure report failed -> {e}") # ADD THIS
                return False