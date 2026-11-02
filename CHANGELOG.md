# Changelog

All notable changes to the PyMon Python SDK will be documented in this file.

## [0.1.0] - 2024-05-24

### Added
- Initial release of the PyMon SDK.
- `@monitor` decorator for synchronous functions.
- `@monitor_async` decorator for asynchronous functions.
- Automatic failure reporting with full Python stack traces.
- `Client` class for manual pinging.
- Environment variable support (`PYMON_API_KEY`, `PYMON_URL`).