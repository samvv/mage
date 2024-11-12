
from magelang.lang.treespec.ast import *
from magelang.lang.treespec.helpers import is_unit_type, make_unit, simplify_type

def treespec_cst_to_ast(specs: Specs) -> Specs:

    def rewriter(ty: Type) -> Type:
        if isinstance(ty, TokenType):
            spec = specs.lookup(ty.name)
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
                if is_unit_type(new_ty):
                    continue
                new_fields.append(Field(field.name, new_ty))
            return NodeSpec(spec.name, new_fields)
        assert_never(spec)

    toplevel = []

    for spec in specs:
        new_spec = rewrite_spec(spec)
        if new_spec is None:
            continue
        toplevel.append(new_spec)

    return Specs(toplevel)

