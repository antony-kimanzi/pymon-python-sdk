# Changelog

All notable changes to the PyMon Python SDK will be documented in this file.

## [0.1.5] - 2026-11-10

### Fixed
- Fixed the pyproject.toml to use modern SPDX format for the license


## [0.1.4] - 2026-11-10

### Fixed
- Set the decorator and client to return the check name for the purpose of the API URL
- Fix init to accept dotenv variables
- Deleted the test-script.py


## [0.1.1] - 2026-11-02

### Fixed
- Fixed an issue where the default `PYMON_URL` would resolve to `None`, causing pings to fail.
- Set the default API URL to `http://localhost:8080` for local development.


## [0.1.0] - 2026-11-02

### Added
- Initial release of the PyMon SDK.
- `@monitor` decorator for synchronous functions.
- `@monitor_async` decorator for asynchronous functions.
- Automatic failure reporting with full Python stack traces.
- `Client` class for manual pinging.
- Environment variable support (`PYMON_API_KEY`, `PYMON_URL`).