# flake8-expression-complexity


[![Build Status](https://travis-ci.org/best-doctor/flake8-expression-complexity.svg?branch=master)](https://travis-ci.org/best-doctor/flake8-expression-complexity)
[![Maintainability](https://api.codeclimate.com/v1/badges/f85c1fd2ad4af63d93b6/maintainability)](https://codeclimate.com/github/best-doctor/flake8-expression-complexity/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f85c1fd2ad4af63d93b6/test_coverage)](https://codeclimate.com/github/best-doctor/flake8-expression-complexity/test_coverage)
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

    pip install flake8-expression-complexity


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

Tested on Python 3.6, 3.7 and flake8 3.7.8.


## Error codes

| Error code |                     Description   |
|:----------:|:---------------------------------:|
|   ECE001   | Expression is too complex (X > Y) |


## Contributing

We would love you to contribute to our project. It's simple:

1. Create an issue with bug you found or proposal you have. Wait for approve from maintainer.
2. Create a pull request. Make sure all checks are green.
3. Fix review comments if any.
4. Be awesome.

Here are useful tips:

- You can run all checks and tests with `make check`. Please do it before TravisCI does.
- We use [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/python_styleguide.md). Sorry, styleguide is available only in Russian for now.
- We respect [Django CoC](https://www.djangoproject.com/conduct/). Make soft, not bullshit.
