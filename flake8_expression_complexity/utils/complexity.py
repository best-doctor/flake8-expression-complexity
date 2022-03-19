import ast
import sys
import itertools
from typing import Mapping, Any, List

from astpretty import pprint

from flake8_expression_complexity.utils.iterables import max_with_default

TYPES_MAP = [
    (ast.UnaryOp, 'unary_op'),
    (
        (
            ast.Expr, ast.Return, ast.Starred, ast.Index,
            ast.Yield, ast.YieldFrom, ast.FormattedValue,
        ),
        'item_with_value',
    ),
    (ast.Assert, 'assert'),
    (ast.Delete, 'delete'),
    (ast.Assign, 'assign'),
    ((ast.AugAssign, ast.AnnAssign), 'featured_assign'),
    (ast.Call, 'call'),
    (ast.Await, 'await'),
    ((ast.List, ast.Set, ast.Tuple), 'sized'),
    (ast.Dict, 'dict'),
    (ast.DictComp, 'dict_comprehension'),
    ((ast.ListComp, ast.GeneratorExp, ast.SetComp), 'simple_comprehensions'),
    (ast.comprehension, 'base_comprehension'),
    (ast.Compare, 'compare'),
    (ast.Subscript, 'subscript'),
    (ast.Slice, 'slice'),
    (ast.ExtSlice, 'ext_slice'),
    (ast.BinOp, 'binary_op'),
    (ast.Lambda, 'lambda'),
    (ast.IfExp, 'if_expr'),
    (ast.BoolOp, 'bool_op'),
    (ast.Attribute, 'attribute'),
    (ast.JoinedStr, 'fstring'),
    (ast.ClassDef, 'classdef'),
    (
        (
            ast.Name, ast.Import, ast.Str, ast.Num, ast.NameConstant, ast.Bytes, ast.Nonlocal,
            ast.ImportFrom, ast.Pass, ast.Raise, ast.Break, ast.Continue, type(None),
            ast.Ellipsis, ast.Global,
        ),
        'simple_type',
    ),
]

if sys.version_info >= (3, 8):
    TYPES_MAP.append(
        (ast.NamedExpr, 'walrus'),
    )

if sys.version_info >= (3, 10):
    TYPES_MAP.extend(
        [
            (ast.Match, 'match'),
            (ast.match_case, 'case'),
        ]
    )


def get_expression_complexity(node: ast.AST) -> float:
    info = get_expression_part_info(node)
    score_addon = get_complexity_increase_for_node_type(info['type'])
    if not info['subnodes']:
        return score_addon
    return max_with_default(get_expression_complexity(n) for n in info['subnodes']) + score_addon


def get_complexity_increase_for_node_type(node_type_sid: str) -> float:
    nodes_scores_map = {
        'unary_op': 1,
        'item_with_value': 0,
        'assert': 1,
        'delete': 1,
        'assign': 1,
        'featured_assign': 1,
        'call': .5,
        'await': .5,
        'sized': 1,
        'dict': 1,
        'dict_comprehension': 1,
        'simple_comprehensions': 1,
        'base_comprehension': 0,
        'compare': 1,
        'subscript': 1,
        'slice': 1,
        'ext_slice': 1,
        'binary_op': 1,
        'lambda': 1,
        'if_expr': 1,
        'bool_op': 1,
        'attribute': 1,
        'simple_type': 0,
        'fstring': 2,
        'walrus': 2,
        'match': 1,
        'case': 1,
    }
    return nodes_scores_map[node_type_sid]


def get_expression_part_info(node: ast.AST) -> Mapping[str, Any]:
    node_type_sid = None
    for types, node_type_name in TYPES_MAP:
        if isinstance(node, types):  # type: ignore
            node_type_sid = node_type_name
            break
    else:
        pprint(node)  # noqa
        raise AssertionError('should always get node type')

    return {
        'type': node_type_sid,
        'subnodes': _get_sub_nodes(node, node_type_sid),
    }


def _get_sub_nodes(node: Any, node_type_sid: str) -> List[ast.AST]:
    subnodes_map = {
        'unary_op': lambda n: [n.operand],
        'item_with_value': lambda n: [n.value],
        'assert': lambda n: [n.test],
        'delete': lambda n: node.targets,
        'assign': lambda n: node.targets + [node.value],
        'featured_assign': lambda n: [n.target, n.value],
        'call': lambda n: node.args + [n.func],
        'await': lambda n: [node.value],
        'sized': lambda n: node.elts,
        'dict': lambda n: itertools.chain(node.keys, node.values),
        'dict_comprehension': lambda n: node.generators + [n.key, n.value],
        'simple_comprehensions': lambda n: node.generators + [n.elt],
        'base_comprehension': lambda n: node.ifs + [n.target, n.iter],
        'compare': lambda n: node.comparators + [n.left],
        'subscript': lambda n: [n.value, n.slice],
        'slice': lambda n: [n.lower, n.upper, n.step],
        'ext_slice': lambda n: n.dims,
        'binary_op': lambda n: [n.left, n.right],
        'lambda': lambda n: [n.body],
        'if_expr': lambda n: [n.test, n.body, n.orelse],
        'bool_op': lambda n: n.values,
        'fstring': lambda n: n.values,
        'attribute': lambda n: [n.value],
        'simple_type': lambda n: [],
        'walrus': lambda n: [n.target, n.value],
        'match': lambda n: n.cases,
        'case': lambda n: [],
    }
    return subnodes_map[node_type_sid](node)
