
from magelang.helpers import lookup_spec
from magelang.lang.mage.constants import integer_rule_type
from magelang.lang.treespec.ast import *
from magelang.lang.treespec.helpers import flatten_union, is_unit_type, make_unit, normalize_type


def is_ignored(ty: Type) -> bool:
    return all(isinstance(el_ty, NoneType) or is_unit_type(el_ty) for el_ty in flatten_union(ty))


def treespec_cst_to_ast(specs: Specs) -> Specs:

    def reduce_type(ty: Type) -> Type:

        def rewrite(ty: Type) -> Type:
            if isinstance(ty, TokenType):
                spec = lookup_spec(specs, ty.name)
                assert(isinstance(spec, TokenSpec))
                if spec.is_static:
                    return make_unit()
                return ExternType(spec.field_type)
            if isinstance(ty, NoneType) \
                or isinstance(ty, NeverType) \
                or isinstance(ty, NodeType) \
                or isinstance(ty, ExternType) \
                or isinstance(ty, AnyType) \
                or isinstance(ty, VariantType):
                return ty
            if isinstance(ty, ListType):
                new_element_type = reduce_type(ty.element_type)
                if is_unit_type(new_element_type):
                    return ExternType(integer_rule_type)
                return ty.derive(element_type=new_element_type)
            if isinstance(ty, TupleType):
                new_element_types = []
                for ty_2 in ty.element_types:
                    new_ty_2 = reduce_type(ty_2)
                    if not is_unit_type(new_ty_2):
                        new_element_types.append(new_ty_2)
                if len(new_element_types) == 1:
                    return new_element_types[0]
                return ty.derive(element_types=new_element_types)
            if isinstance(ty, PunctType):
                new_element_type = reduce_type(ty.element_type)
                new_separator_type = reduce_type(ty.separator_type)
                if is_unit_type(new_element_type) and is_unit_type(new_separator_type):
                    return ExternType(integer_rule_type)
                if is_unit_type(new_element_type):
                    return ListType(new_separator_type, ty.required)
                if is_unit_type(new_separator_type):
                    return ListType(new_separator_type, False) # FIXME `required` is incorrectly set
                return ty.derive(
                    element_type=new_element_type,
                    separator_type=new_separator_type,
                )
            if isinstance(ty, UnionType):
                return rewrite_each_child_type(ty, reduce_type)
            assert_never(ty)

        return normalize_type(rewrite(ty))


    def rewrite_spec(spec: Spec) -> Spec | None:
        if isinstance(spec, TokenSpec):
            return None
        if isinstance(spec, ConstEnumSpec):
            return spec
        if isinstance(spec, VariantSpec):
            new_members = []
            for name, ty in spec.members:
                new_members.append((name, reduce_type(ty)))
            return VariantSpec(spec.name, new_members)
        if isinstance(spec, NodeSpec):
            new_fields = []
            for field in spec.fields:
                new_ty = reduce_type(field.ty)
                if is_ignored(new_ty):
                    continue
                new_fields.append(Field(field.name, new_ty))
            return NodeSpec(spec.name, new_fields)
        assert_never(spec)

    toplevel = []

    for spec in specs.elements:
        new_spec = rewrite_spec(spec)
        if new_spec is None:
            continue
        toplevel.append(new_spec)

    return Specs(toplevel)

