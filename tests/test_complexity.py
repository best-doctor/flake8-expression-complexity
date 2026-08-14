import ast
import sys

import pytest
from conftest import run_validator_for_test_file

from flake8_expression_complexity.utils.ast import iterate_over_expressions
from flake8_expression_complexity.utils.complexity import get_expression_complexity


def test_fails():
    errors = run_validator_for_test_file('long_expressions.py', max_expression_complexity=3)
    assert len(errors) == 5


def test_walrus():
    errors = run_validator_for_test_file('walrus.py', max_expression_complexity=1)
    assert len(errors) == 1


def test_match():
    errors = run_validator_for_test_file('match.py', max_expression_complexity=1)
    assert len(errors) == 3


def test_async_expressions():
    errors = run_validator_for_test_file('async_expressions.py', max_expression_complexity=1)
    assert len(errors) == 3


@pytest.mark.skipif(sys.version_info < (3, 12), reason='runs only for python 3.12+')
def test_type_alias():
    errors = run_validator_for_test_file('type_alias.py', max_expression_complexity=1)
    assert len(errors) == 1


@pytest.mark.parametrize(
    ('source', 'expected_complexity'),
    [
        pytest.param('async def f():\n    return await get_value()', 1.0, id='await'),
        pytest.param(
            'async def f():\n    async for x in y():\n        pass', 0.5, id='async_for',
        ),
        pytest.param(
            'async def f():\n    async with a() as x:\n        pass', 0.5, id='async_with',
        ),
    ],
)
def test_get_expression_complexity_for_async_constructs(source, expected_complexity):
    tree = ast.parse(source)
    expressions = list(iterate_over_expressions(tree))

    complexities = [get_expression_complexity(expression) for expression in expressions]

    assert max(complexities) == expected_complexity


@pytest.mark.parametrize(
    ('source', 'expected_complexity'),
    [
        pytest.param('match a.b.c():\n    case _:\n        pass', 2.5, id='complex_subject'),
        pytest.param('match x:\n    case n if n > 0:\n        pass', 1, id='guard'),
        pytest.param('match x:\n    case 1:\n        y = a and b and c', 2, id='complex_case_body'),
    ],
)
def test_get_expression_complexity_for_match_constructs(source, expected_complexity):
    # Regression test: the match subject and each case's guard/body must be walked
    # independently instead of collapsing the whole `match` statement into a flat score
    # that ignored how complex the subject or branches actually were.
    tree = ast.parse(source)
    expressions = list(iterate_over_expressions(tree))

    complexities = [get_expression_complexity(expression) for expression in expressions]

    assert max(complexities) == expected_complexity


@pytest.mark.skipif(sys.version_info < (3, 12), reason='runs only for python 3.12+')
@pytest.mark.parametrize(
    ('source', 'expected_complexity'),
    [
        pytest.param('type Integer = int', 1, id='simple'),
        pytest.param('type Alias = list[dict[str, int]]', 4, id='complex_value'),
        pytest.param('type Alias[T: (a and b)] = list[T]', 2, id='bound'),
    ],
)
def test_get_expression_complexity_for_type_alias_constructs(source, expected_complexity):
    # Regression test for https://github.com/best-doctor/flake8-expression-complexity/pull/24:
    # the `type X = ...` statement (PEP 695, Python 3.12+) used to crash the checker outright
    # (AssertionError: should always get node type) because ast.TypeAlias wasn't recognized
    # at all. Now the aliased value and any bound on a generic type parameter are scored.
    tree = ast.parse(source)
    expressions = list(iterate_over_expressions(tree))

    complexities = [get_expression_complexity(expression) for expression in expressions]

    assert max(complexities) == expected_complexity


@pytest.mark.parametrize(
    'source',
    [
        pytest.param('x = "a string"', id='str'),
        pytest.param('x = 1', id='int'),
        pytest.param('x = 1.5', id='float'),
        pytest.param('x = None', id='none'),
        pytest.param('x = b"bytes"', id='bytes'),
        pytest.param('x = ...', id='ellipsis'),
    ],
)
def test_get_expression_complexity_for_constants(source):
    # Regression test: every ast.Constant literal kind must resolve to the
    # 'simple_type' bucket without relying on the ast.Str/Num/NameConstant/Bytes/Ellipsis
    # aliases, which are removed in Python 3.14.
    tree = ast.parse(source)
    expressions = list(iterate_over_expressions(tree))

    complexities = [get_expression_complexity(expression) for expression in expressions]

    assert complexities == [1]
