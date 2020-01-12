from typing import Generator, Tuple


from flake8_expression_complexity import __version__ as version
from flake8_expression_complexity.utils.ast import iterate_over_expressions
from flake8_expression_complexity.utils.complexity import get_expression_complexity
from flake8_expression_complexity.utils.django import is_django_orm_query


class ExpressionComplexityChecker:
    DEFAULT_MAX_EXPRESSION_COMPLEXITY = 7

    name = 'flake8-expression-complexity'
    version = version

    max_expression_complexity = DEFAULT_MAX_EXPRESSION_COMPLEXITY
    ignore_django_orm_queries = False

    def __init__(self, tree, filename: str):
        self.filename = filename
        self.tree = tree

    @classmethod
    def add_options(cls, parser) -> None:
        parser.add_option(
            '--max-expression-complexity',
            type=int,
            default=cls.DEFAULT_MAX_EXPRESSION_COMPLEXITY,
            parse_from_config=True,
        )
        parser.add_option(
            '--ignore-django-orm-queries-complexity',
            action='store_true',
            parse_from_config=True,
        )

    @classmethod
    def parse_options(cls, options) -> None:
        cls.max_expression_complexity = int(options.max_expression_complexity)
        cls.ignore_django_orm_queries = bool(options.ignore_django_orm_queries_complexity)

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        for expression in iterate_over_expressions(self.tree):
            if self.ignore_django_orm_queries and is_django_orm_query(expression):
                continue
            complexity = get_expression_complexity(expression)
            if complexity > self.max_expression_complexity:
                yield (
                    expression.lineno,
                    expression.col_offset,
                    f'ECE001 Expression is too complex '
                    f'({complexity} > {self.max_expression_complexity})',
                    type(self),
                )
