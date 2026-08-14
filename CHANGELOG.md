# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-14

### Changed

- Raised minimum supported Python version to 3.10 and added support for Python 3.11, 3.12,
  3.13 and 3.14.
- Migrated packaging to `pyproject.toml` (build backend: hatchling), replacing
  `setup.py`/`setup.cfg`/`requirements_dev.txt`.
- `flake8` configuration now lives in `pyproject.toml` under `[tool.flake8]`, loaded via the
  `Flake8-pyproject` plugin.
- Switched dependency and environment management to [uv](https://docs.astral.sh/uv/); the
  `Makefile` and CI workflows now run everything through `uv run`/`uv sync`.
- CI workflows now use `astral-sh/setup-uv` and test against Python 3.10-3.14.
- Replaced `safety` with `pip-audit` for dependency vulnerability scanning.
- Replaced the Ruby-based `mdl` markdown linter (`.mdlrc`, `.mdlrc.rb`) with
  `markdownlint-cli2`, configured via `.markdownlint.jsonc` and available both as a
  pre-commit hook and a `make readme` target.
- `publish.yml` now builds with `uv build` and publishes with `uv publish` using a
  `PYPI_TOKEN` secret, instead of `twine` with username/password secrets.

### Added

- `.pre-commit-config.yaml` with hygiene hooks, `flake8`, `mypy`, and `markdownlint-cli2`.
- This changelog.

### Removed

- Code Climate integration (`.codeclimate.yml`, CI coverage upload, README badges) — the
  service was unused as a legacy carry-over from the original project template.
- `.flake_master`, a leftover config file for an unrelated internal preset-sync tool that
  wasn't referenced anywhere in the build.
- The `astpretty` runtime dependency, `flake8-polyfill`, and `flake8-typing-imports` dev
  dependencies (dead/obsolete now that the minimum supported Python is 3.10).

### Fixed

- `ExpressionComplexityChecker` no longer relies on the deprecated `ast.Str`, `ast.Num`,
  `ast.NameConstant`, `ast.Bytes`, `ast.Ellipsis`, `ast.Index`, and `ast.ExtSlice` aliases,
  which are scheduled for removal in Python 3.14 and would have broken the checker on that
  version. Constant literals are now matched via `ast.Constant`, and the dead `Index`/`ExtSlice`
  branches (unreachable since Python 3.9's grammar change) were removed.
- `match`/`case` statements now have their subject expression and each case's guard/body
  walked individually, the same way `if`/`for`/`while`/`with` already were. Previously the
  whole `match` statement collapsed into a flat complexity score of `2`, so a complex
  subject expression or a deeply nested case body was invisible to the checker regardless
  of how complex it actually was.

## [0.0.11] - 2022-03-19

### Added

- Support for `match`/`case` pattern matching statements (Python 3.10).

### Changed

- Dropped `setuptools` from `install_requires`.

## [0.0.10] - 2022-02-24

### Added

- Support for Python 3.10.
- Support for `async for`.
- Code Climate coverage/maintainability reporting.

### Removed

- Support for Python 3.6.

### Changed

- Switched CI from Travis CI to GitHub Actions.

## [0.0.9] - 2021-01-14

### Added

- Support for Python 3.9.

## [0.0.8] - 2020-06-22

### Added

- Support for the walrus operator (`:=`).

## [0.0.7] - 2020-03-15

### Added

- Support for the `global` keyword.
- Support for Python 3.8.

## [0.0.6] - 2020-01-12

### Added

- Support for `async with` and `with`-statement variable nodes.

## [0.0.5] - 2020-01-09

### Added

- Support for `await`.

### Fixed

- Missing `astpretty` runtime dependency.

## [0.0.4] - 2019-11-13

### Added

- Support for `async def`.
- Support for extended slices.
- Support for Python 3.6.

## [0.0.1] - 2019-10-30

### Added

- Initial release of the `ECE001` expression complexity check.

[Unreleased]: https://github.com/best-doctor/flake8-expression-complexity/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/best-doctor/flake8-expression-complexity/compare/v0.0.11...v0.1.0
[0.0.11]: https://github.com/best-doctor/flake8-expression-complexity/compare/v0.0.10...v0.0.11
[0.0.10]: https://github.com/best-doctor/flake8-expression-complexity/compare/v0.0.9...v0.0.10
[0.0.9]: https://github.com/best-doctor/flake8-expression-complexity/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/best-doctor/flake8-expression-complexity/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/best-doctor/flake8-expression-complexity/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/best-doctor/flake8-expression-complexity/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/best-doctor/flake8-expression-complexity/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/best-doctor/flake8-expression-complexity/compare/v0.0.1...v0.0.4
[0.0.1]: https://github.com/best-doctor/flake8-expression-complexity/releases/tag/v0.0.1
