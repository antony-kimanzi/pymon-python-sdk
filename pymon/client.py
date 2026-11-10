import logging
import os
import traceback
from datetime import datetime, timezone
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Client:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        load_dotenv()  # <-- Loads .env if it exists

        def _env(name: str) -> Optional[str]:
            v = os.environ.get(name)
            return v.strip() if v and v.strip() else None

        self.api_key = (api_key or _env("PYMON_API_KEY") or "").strip() or None
        self.base_url = (
            base_url
            or _env("PYMON_API_BASE_URL")
            or "http://localhost:8080/api/v1"
        ).rstrip("/")

        env_timeout = _env("PYMON_TIMEOUT")
        self.timeout = timeout or (int(env_timeout) if env_timeout else None) or 5

        if not self.api_key:
            raise ValueError(
                "PyMon API Key is required. "
                "Set the PYMON_API_KEY environment variable or pass api_key."
            )

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "pymon-python/0.1.0",
        }

    def ping_success(self, monitor_name: str, duration_ms: int) -> bool:
        """Send a success ping to the backend."""
        url = f"{self.base_url}/ping/{monitor_name}"
        payload = {"monitorName": monitor_name, "durationMs": duration_ms}

        try:
            resp = requests.post(
                url, json=payload, headers=self._get_headers(), timeout=self.timeout
            )
            resp.raise_for_status()
            return True
        except requests.HTTPError as e:
            err_resp = e.response
            if err_resp is not None:
                logger.warning("Ping rejected (%s): %s", err_resp.status_code, err_resp.text[:500])
            else:
                logger.warning("Ping rejected: %s", e)
        except requests.RequestException as e:
            logger.warning("Ping failed: %s", e)
        return False

    def report_failure(self, monitor_name: str, error: Exception) -> bool:
        """Report a failure with the full stack trace."""
        url = f"{self.base_url}/ping/{monitor_name}/fail"
        stack = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        payload = {
            "monitorName": monitor_name,
            "errorType": type(error).__name__,
            "errorMessage": str(error),
            "stackTrace": stack,
            "occurredAt": datetime.now(timezone.utc).isoformat(),
        }

        try:
            resp = requests.post(
                url, json=payload, headers=self._get_headers(), timeout=self.timeout
            )
            resp.raise_for_status()
            return True
        except requests.HTTPError as e:
            err_resp = e.response
            if err_resp is not None:
                logger.warning("Failure rejected (%s): %s", err_resp.status_code, err_resp.text[:500])
            else:
                logger.warning("Failure rejected: %s", e)
        except requests.RequestException as e:
            logger.warning("Failure report failed: %s", e)
        return False
