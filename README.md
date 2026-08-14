# flake8-expression-complexity

[![Build Status](https://github.com/best-doctor/flake8-expression-complexity/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/best-doctor/flake8-expression-complexity/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/flake8-expression-complexity.svg?)](https://badge.fury.io/py/flake8-expression-complexity)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-expression-complexity)

An extension for flake8 that validates expression complexity.

Splits code into expression and scores each according to how much one is complicated.
Fires an error on each expression more complex than theshold.

Default complexity is 7, can be configured via `--max-expression-complexity` option.

Since Django ORM queries can produce long and readable expressions,
checker can skip them. To enable this behaviour,
use `--ignore-django-orm-queries-complexity` option.

## Installation

```terminal
pip install flake8-expression-complexity
```

Requires Python 3.10 to 3.14.

## Example

```python
if (
    (user and user.is_authorized)
    and user.subscriptions.filter(start_date__lt=today, end_date__gt=today).exists()
    and (
        user.total_credits_added
        - Check.objects.filter(user=user).aggregate(Sum('price'))['check__sum']
    )
    and UserAction.objects.filter(user=user).last().datetime > today - datetime.timedelta(days=10)
):
    ...
```

Usage:

```terminal
$ flake8 --max-expression-complexity=3 test.py
text.py:2:5: ECE001 Expression is too complex (7.0 > 3)
```

## Error codes

| Error code |                     Description   |
|:----------:|:---------------------------------:|
|   ECE001   | Expression is too complex (X > Y) |

## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have.
   Wait for approve from maintainer.
1. Create a pull request. Make sure all checks are green.
1. Fix review comments if any.
1. Be awesome.

Here are useful tips:

- This project uses [uv](https://docs.astral.sh/uv/) for dependency management.
  Run `make install` to set up a local environment.
- You can run all checks and tests with `make check`.
  Please do it before CI does.
- Install the [pre-commit](https://pre-commit.com/) hooks with
  `uv run pre-commit install` to catch issues before you commit.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.
