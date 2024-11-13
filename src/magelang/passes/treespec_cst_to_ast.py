
from .mage_insert_magic_rules import any_token_rule_name, any_syntax_rule_name
from magelang.helpers import lookup_spec
from magelang.lang.mage.constants import integer_rule_type
from magelang.lang.treespec.ast import *
from magelang.lang.treespec.helpers import flatten_union, is_static_type, is_unit_type, make_unit, normalize_type


def is_ignored(ty: Type) -> bool:
    return all(isinstance(el_ty, NoneType) or is_unit_type(el_ty) for el_ty in flatten_union(ty))


def treespec_cst_to_ast(specs: Specs) -> Specs:

    def rewrite_type(ty: Type) -> Type:

        def rewrite(ty: Type) -> Type:
            if isinstance(ty, SpecType):
                spec = lookup_spec(specs, ty.name)
                if isinstance(spec, TokenSpec):
                    return make_unit() if spec.is_static else ExternType(spec.field_type)
                return ty
            if isinstance(ty, NoneType) \
                or isinstance(ty, NeverType) \
                or isinstance(ty, ExternType) \
                or isinstance(ty, AnyType):
                return ty
            if isinstance(ty, ListType):
                new_element_type = rewrite(ty.element_type)
                if is_unit_type(new_element_type):
                    return ExternType(integer_rule_type)
                return ty.derive(element_type=new_element_type)
            if isinstance(ty, TupleType):
                new_element_types = []
                for ty_2 in ty.element_types:
                    new_ty_2 = rewrite(ty_2)
                    if not is_unit_type(new_ty_2):
                        new_element_types.append(new_ty_2)
                if len(new_element_types) == 1:
                    return new_element_types[0]
                return ty.derive(element_types=new_element_types)
            if isinstance(ty, PunctType):
                new_element_type = rewrite(ty.element_type)
                new_separator_type = rewrite(ty.separator_type)
                if is_unit_type(new_element_type) and is_unit_type(new_separator_type):
                    return ExternType(integer_rule_type)
                if is_unit_type(new_element_type):
                    return ListType(new_separator_type, ty.required)
                if is_unit_type(new_separator_type):
                    return ListType(new_element_type, False) # FIXME `required` is incorrectly set
                return ty.derive(
                    element_type=new_element_type,
                    separator_type=new_separator_type,
                )
            if isinstance(ty, UnionType):
                new_types = []
                for ty_2 in ty.types:
                    new_ty_2 = rewrite(ty_2)
                    if not is_unit_type(new_ty_2):
                        new_types.append(new_ty_2)
                return ty.derive(types=new_types)
            assert_never(ty)

        return normalize_type(rewrite(ty))

    def rewrite_spec(spec: Spec) -> Spec | None:
        if isinstance(spec, TokenSpec):
            return None
        if isinstance(spec, ConstEnumSpec):
            return spec
        if isinstance(spec, TypeSpec):
            return TypeSpec(spec.name, rewrite_type(spec.ty))
        if isinstance(spec, VariantSpec):
            if all(is_static_type(mem_ty, specs=specs) for _, mem_ty in spec.members):
                return ConstEnumSpec(spec.name, list((name, i) for i, (name, _) in enumerate(spec.members)))
            new_members = []
            for name, ty in spec.members:
                new_members.append((name, rewrite_type(ty)))
            return VariantSpec(spec.name, new_members)
        if isinstance(spec, NodeSpec):
            new_fields = []
            for field in spec.fields:
                new_ty = rewrite_type(field.ty)
                if is_ignored(new_ty):
                    continue
                new_fields.append(Field(field.name, new_ty))
            return NodeSpec(spec.name, new_fields)
        assert_never(spec)

    toplevel = []

    for spec in specs.elements:
        if spec.name in [ any_token_rule_name, any_syntax_rule_name ]:
            continue
        new_spec = rewrite_spec(spec)
        if not new_spec is None:
            toplevel.append(new_spec)

    return Specs(toplevel)

