import ast


def is_django_orm_query(node: ast.AST) -> bool:
    django_orm_typical_methods = {
        'objects',
        'filter',
        'annotate',
        'select_related',
        'prefetch_related',
        'distinct',
    }
    total_points_to_be_threated_as_django_orm_query = 0
    points_required_to_be_threated_as_django_orm_query = 2
    for attribute_node in [n for n in ast.walk(node) if isinstance(n, ast.Attribute)]:
        if attribute_node.attr in django_orm_typical_methods:
            total_points_to_be_threated_as_django_orm_query += 1
    return (
        total_points_to_be_threated_as_django_orm_query
        >= points_required_to_be_threated_as_django_orm_query
    )
