# Changelog

All notable changes to the PyMon Python SDK will be documented in this file.
## [0.1.1] - 2024-05-25

### Fixed
- Fixed an issue where the default `PYMON_URL` would resolve to `None`, causing pings to fail.
- Set the default API URL to `http://localhost:8080` for local development.


## [0.1.0] - 2024-05-24

### Added
- Initial release of the PyMon SDK.
- `@monitor` decorator for synchronous functions.
- `@monitor_async` decorator for asynchronous functions.
- Automatic failure reporting with full Python stack traces.
- `Client` class for manual pinging.
- Environment variable support (`PYMON_API_KEY`, `PYMON_URL`).