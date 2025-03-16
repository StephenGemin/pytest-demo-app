Example pytest application. This repo is for future reference, because re-inventing the wheel is a waste of time and creativity.

Key points for this application include:
* **LOGGING, LOGGING, LOGGING!**
  * Refer to [Logging](#logging) section for more details
* Poetry as the package manager
  * Mostly to force myself to learn and use Poetry
  * Used Poetry 1.8
* Pytest hooks in separate file so conftest.py isn't cluttered
* Monolithic style app where everything is bundled in one repo
  * supporting API included in toolkit package

## Logging
Out of the box, pytest excels at small-scale and straightforward testing. However, it quickly shows its limitations when it comes to more robust and complex testing solutions.
Specifically, pytest struggles with collecting and managing file logs in intricate test scenarios.

Shoutout to the [Slash test framework](https://github.com/getslash/slash) for superior built-in logging mechanisms and many other features!

- Output logs to multiple log files 🤯
  - Logs are stored in the .logs directory at the project root by default.
  - Unique directory for each pytest session
    - Each test in the pytest session has it's own subdirectory Unique directory for each test in the pytest session
    - Folder names to sort alphabetical, prefixed with test iteration index
  - Session log -> session.log
    - Some may find it easier to parse through a single file than looking through each individual test file
- Stacktraces and assert errors are output to log files!!! 🤯
- Html report using pytest-html
  - Future implementation to have the report go into each session directory
- Maintain pytest's framework for CLI/ file logging level configuration.

## PyInstaller
Run tests from PyInstaller generated executable
`poetry run pyinstaller main.spec`
`dist/main.exe`

## Commands
Some commands below are missing options due to defaults in pyproject.toml

- `pytest --tb=no -o log_cli=false` - absolute bare bones output, no file logs
- `pytest --tb=no` - minimal console, with file logs
- `pytest` - only tests with errors / failures to console, with file logs
- `pytest --tb=long -l -o log_cli_level=DEBUG` - full blast to console, show locals in TB, full trace back
- `pytest --html=report.html --self-contained-html`

## Tips
Run `pytest --debug` for detailed info on fixtures / hooks
