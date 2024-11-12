
from magelang.helpers import lookup_spec
from magelang.lang.treespec.ast import *
from magelang.lang.treespec.helpers import flatten_union, is_unit_type, make_unit, simplify_type

def is_ignored(ty: Type) -> bool:
    return all(isinstance(el_ty, NoneType) or is_unit_type(el_ty) for el_ty in flatten_union(ty))

def treespec_cst_to_ast(specs: Specs) -> Specs:

    def rewriter(ty: Type) -> Type:
        if isinstance(ty, TokenType):
            spec = lookup_spec(specs, ty.name)
            assert(isinstance(spec, TokenSpec))
            if spec.is_static:
                return make_unit()
            return ExternType(spec.field_type)
        return rewrite_each_child_type(ty, rewriter)

    def rewrite_spec(spec: Spec) -> Spec | None:
        if isinstance(spec, TokenSpec):
            return None
        if isinstance(spec, ConstEnumSpec):
            return spec
        if isinstance(spec, VariantSpec):
            new_members = []
            for name, ty in spec.members:
                new_members.append((name, rewriter(ty)))
            return VariantSpec(spec.name, new_members)
        if isinstance(spec, NodeSpec):
            new_fields = []
            for field in spec.fields:
                new_ty = simplify_type(rewriter(field.ty))
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

