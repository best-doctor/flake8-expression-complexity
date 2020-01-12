from conftest import run_validator_for_test_file


def test_fails():
    errors = run_validator_for_test_file('long_expressions.py', max_expression_compexity=3)
    assert len(errors) == 4
