import sys

import pytest
from conftest import run_validator_for_test_file


def test_fails():
    errors = run_validator_for_test_file('long_expressions.py', max_expression_complexity=3)
    assert len(errors) == 5


@pytest.mark.skipif(sys.version_info < (3, 8), reason='runs only for python 3.8+')
def test_walrus():
    errors = run_validator_for_test_file('walrus.py', max_expression_complexity=1)
    assert len(errors) == 1


@pytest.mark.skipif(sys.version_info < (3, 10), reason='runs only for python 3.10+')
def test_match():
    errors = run_validator_for_test_file('match.py', max_expression_complexity=1)
    assert len(errors) == 1
