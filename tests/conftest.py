import ast
import os

from flake8_expression_complexity.checker import ExpressionComplexityChecker


def run_validator_for_test_file(
    filename: str,
    max_expression_compexity: int = None,
    ignore_django_orm_queries: bool = True,
):
    test_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_files',
        filename,
    )
    with open(test_file_path, 'r') as file_handler:
        raw_content = file_handler.read()
    tree = ast.parse(raw_content)
    checker = ExpressionComplexityChecker(tree=tree, filename=filename)
    if max_expression_compexity:
        checker.max_expression_compexity = max_expression_compexity
    if ignore_django_orm_queries:
        checker.ignore_django_orm_queries = ignore_django_orm_queries

    return list(checker.run())
