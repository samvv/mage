
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Iterable, Iterator, assert_never, cast

from .util import NameGenerator, plural, to_snake_case
from .ast import *


# def cst_to_ast(specs: Specs) -> Specs:

#     def rewriter(ty: Type) -> Type:
#         # if is_static_type(ty, specs=specs):
#         #     return make_unit()
#         if isinstance(ty, TokenType):
#             spec = specs.lookup(ty.name)
#             assert(isinstance(spec, TokenSpec))
#             return ExternType(spec.field_type)
#         # if isinstance(ty, VariantType):
#         #     spec = specs.lookup(ty.name)
#         #     assert(isinstance(spec, VariantSpec))
#         #     only_tokens = True
#         #     for _, member in spec.members:
#         #         if not isinstance(member, TokenType):
#         #             only_tokens = False
#         #             break
#         #     if only_tokens:
#         #         print(spec.name)
#         #         return None
#         # if isinstance(ty, TupleType):
#         #     new_element_types = []
#         #     for el_ty in ty.element_types:
#         #         new_el_ty = rewrite_each_type(el_ty, rewrite)
#         #         if new_el_ty is None:
#         #             continue
#         #         new_element_types.append(new_el_ty)
#         #     return TupleType(new_element_types)
#         return rewrite_each_child_type(ty, rewriter)

#     def rewrite_spec(spec: Spec) -> Spec | None:
#         if isinstance(spec, TokenSpec):
#             return None
#         if isinstance(spec, ConstEnumSpec):
#             return spec
#         if isinstance(spec, VariantSpec):
#             new_members = []
#             for name, ty in spec.members:
#                 new_members.append((name, rewriter(ty)))
#             return VariantSpec(spec.name, new_members)
#         if isinstance(spec, NodeSpec):
#             new_fields = []
#             for field in spec.fields:
#                 new_ty = rewriter(field.ty)
#                 if new_ty is None:
#                     continue
#                 new_fields.append(Field(field.name, new_ty, field.expr))
#             return NodeSpec(spec.name, new_fields)
#         assert_never(spec)

#     new_specs = Specs()

#     for spec in specs:
#         new_spec = rewrite_spec(spec)
#         if new_spec is None:
#             continue
#         new_specs.add(new_spec)

#     return new_specs
