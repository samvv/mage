Mage: Text Analysis Made Easy
=============================

Mage is an experimental tool for performing text analysis. It does so by
generating a _lexer_, _parser_ and _parse tree_ for you. Whether it is a piece
of programming code or some tabular data in a fringe format, Mage has got you
covered!

**Features**

 - ✅ A simple yet expressive DSL to write your grammars in
 - ✅ Full support for Python typings. Avoid runtime errors while building your language!
 - 🚧 Lots of unit tests to enure your code does what you expect it to do
 - 🚧 An intermediate language to very easily add support to any other programming language

👀 Mage is written in itself. Check out the [generated code][1] of part of our Python generator!

**Implementation Status**

| Feature | Python  | Rust | C  | C++ | JavaScript |
|---------|---------|------|----|-----|------------|
| CST     | ✅      | ⏳   | ⏳ | ⏳  | ⏳         |
| AST     | ⏳      | ⏳   | ⏳ | ⏳  | ⏳         |
| Lexer   | 🚧      | ⏳   | ⏳ | ⏳  | ⏳         |
| Parser  | ⏳      | ⏳   | ⏳ | ⏳  | ⏳         |
| Emitter | ⏳      | ⏳   | ⏳ | ⏳  | ⏳         |

[1]: https://github.com/samvv/mage/blob/main/src/magelang/lang/python/cst.py

## Installation

```
$ pip3 install --user -U magelang
```

## Usage

Currently requires at least Python version 3.12 to run.

### `mage generate <lang> <filename>`

Generate a parser for the given grammar in a language that you specify.

**Example**

```
mage generate python foo.mage --prefix foo --out-dir src/foolang
```

### 🚧 `mage test <filename..>`

> [!WARNING]
>
> This command is under construction.

Run all tests inside the documentation of the given grammar.

### `mage fuzz [filename]`

Fuzz the given grammar using a pseudorandom number generator for replayable results.

```
mage fuzz grammars/magedown.mage
```

> [!WARNING]
>
> If you let `mage fuzz --all` run, Mage may write a lot of data to disk.
>
> We recommend creating a temporary file system. A size of 64M should be more
> than enough. For example:
>
> ```sh
> mkdir -p output/fuzz
> sudo mount -t tmpfs tmpfs -o size=64m output/fuzz
> mage fuzz --all
> ```
>
> When you're done run `sudo umount output/fuzz` to unmount it.

## Grammar

### `pub <name> = <expr>`

Define a new node or token that must be parsed according the given expression.

You can use both inline rules and other node rules inside `expr`. When
referring to another node, that node will become a field in the node that
referred to it. Nodes that have no fields are converted to a special token type
that is more efficient to represent.

```
pub var_decl = 'var' name:ident '=' type_expr
```

### `<name> = <expr>`

Define a new inline rule that can be used inside other rules.

As the name suggests, this type of rule is merely syntactic sugar and gets
inlined whenever it is referred to inside another rule.

```
digits = [0-9]+
```

### `extern <name>`

Defines a new parsing rule that is defined somewhere else, possibly in a different language.

### `extern token <name>`

Defines a new lexing rule that is defined somewhere else, possibly in a different language.

### `pub token <name> = <expr>`

Like `pub <name> = <expr>` but forces the rule to be a token.

Mage will show an error when the rule could not be converted to a token rule.
This usually means that the rule references another rule that is only `pub`.

```
pub token float
  = digits? '.' digits
```

### `pub token <name> -> <type_expr> = <expr>`

Like `pub token <name> = <expr>` but forces the value inside the token to be of
the specific type defined by `type_expr`.

```
pub token int -> Integer
  = digits
```

The conversion from the value to the type depends on which type is actually used.
For example, the following table is used when targeting Python:

| Mage Type | Python Type | Code           |
|-----------|-------------|----------------|
| Integer   | `int`       | `int(value)`   |
| Float     | `float`     | `float(value)` |

### `expr1 expr2`

First parse `expr1` and continue to parse `expr2` immediately after it.

```
pub two_column_csv_line
  = text ',' text '\n'
```

### `expr1 | expr2`

First try to parse `expr1`. If that fails, try to parse `expr2`. If none of the
expressions matched, the parser fails.

```
pub declaration
  = function_declaration
  | let_declaration
  | const_declaration
```

### `expr?`

Parse or skip the given expression, depending on whether the expression can be
parsed.

```
pub singleton_or_pair
  = value (',' value)?
```

### `expr*`

Parse the given expression as much as possible.

```
skip = (multiline_comment | whitespace)*
```

### `expr+`

Parse the given expression one or more times.

For example, in Python, there must always be at least one statement in the body of a class or function:

```
body = stmt+
```

### `\expr`

Escape an expression by making it hidden. The expression will be parsed, but
not be visible in the resulting CST/AST.

### `expr{n,m}`

Parse the expression at least `n` times and at most `m` times.

```
unicode_char = 'U+' hex_digit{4,4}
```

### `@keyword`

Treat the given rule as being a potential source for keywords.

String literals matching this rule will get the special `_keyword`-suffix
during transformation. The lexer will also take into account that the rule
conflicts with keywords and generate code accordingly.

```
@keyword
pub token ident
  = [a-zA-Z_] [a-zA-Z_0-9]*
```

### `@skip`

Register the chosen rule as a special rule that the lexer uses to lex 'gibberish'.

The rule will still be available in other rules, e.g. when `@noskip` was added.

```
@skip
whitespace = [\n\r\t ]*
```

### 🚧 `@noskip`

> [!WARNING]
>
> This decorator is under construction.

Disable automatic injection of the `@skip` rule for the chosen rule.

This can be useful for e.g. parsing indentation in a context where whitespace
is normally discarded.

```
@skip
__ = [\n\r\t ]*

@noskip
pub body
  = ':' __ stmt
  | ':' \indent stmt* \dedent
```

### `@wrap`

Adding this decorator to a rule ensures that a real CST node is emitted for
that rule, instead of possibly a variant.

This decorator makes the CST heavier, but this might be warranted in the name
of robustness and forward compatibility. Use this decorator if you plan to add
more fields to the rule.

```
@wrap
pub lit_expr
   = literal:(string | integer | boolean)
```

### `keyword`

A special rule that matches **any keyword present in the grammar**.

The generated CST will contain predicates to check for a keyword:

```py
print_bold = False
if is_py_keyword(token):
    print_bold = True
```

### `token`

A rule that matches **any token in the grammar**.

```
pub macro_call
  = name:ident '{' token* '}'
```

### `node`

A special rule that matches **any parseable node in the grammar**, excluding tokens.

### `syntax`

A special rule that matches **any rule in the grammar**, including tokens.

## Python API

This section documents the API that is generated by taking a Mage grammar as
input and specifying `python` as the output language.

In what follows, `Node` is the name of an arbitrary CST node (such as
`PyReturnStmt` or `MageRepeatExpr`) and `foo` and `bar` are the name of fields
of such a node. Examples of field names are `expr`, `return_keyword`, `min`,
`max,`, and so on.

### `Node(...)`

Construct a node with the fields specified in the `...` part of the expression.

First go all elements that are required, i.e. they weren't suffixed with `?` or
`*` in the grammar or something similar. They may be specified as positional
arguments or as keyword.

Next are all optional arguments. They **must** be specified as keyword
arguments. When omitted, the corresponding fields are either set to `None` or a
new empty token/node is created.

#### Examples

**Creating a new CST node by providing positional arguments for required fields:**
```py
PyInfixExpr(
    PyNamedExpr('value'),
    PyIsKeyword(),
    PyNamedExpr('None')
)
```

**The same example but now with keyword arguments:**
```py
PyInfixExpr(
    left=PyNamedExpr('value'),
    op=PyIsKeyword(),
    right=PyNamedExpr('None')
)
```

**Omitting fields that are trivial to construct:**
```py
# Note that `return_keyword` is not specified
stmt = PyReturnStmt(expr=PyConstExpr(42))

# stmt.return_keyword was automatically created
assert(isinstance(stmt.return_keyword, ReturnKeyword()))
```

### `Node.count_foos() -> int`

This member is generated when there was a repetition in field `foo` such
as the Mage expression `'.'+`

It returns the amount of elements that are actually present in the CST node.

## FAQ

### What is a CST, AST, visitor, and so on?

A **CST** is a collection of structures and enumerations that completely
represent the source code that needs to be parsed/emitted.

An **AST** is an abstract representation of the CST. Mage can automatically
derive a good AST from a CST.

A **visitor** is (usually) a function that traverses the AST/CST in a
particular way. It is useful for various things, such as code analysis and
evaluation.

A **rewriter** is similar to a visitor in that it traverses that AST/CST but
also creates new nodes during this traversal.

A **lexer** or scanner is at it core a program that splits the input stream
into separate _tokens_ that are easy to digest by the parser.

A **parser** converts a stream of tokens in AST/CST nodes. What parts of the
input stream are converted to which nodes usually depends on how the parser is invoked.

### How do I assign a list of nodes to another node in Python without type errors?

This is probably due to [this feature](https://mypy.readthedocs.io/en/stable/common_issues.html#invariance-vs-covariance)
in the Python type checker, which prevents subclasses from being assigned to a more general type.

For small lists, we recommend making a copy of the list, like so:

```py
defn = PyFuncDef(body=list([ ... ]))
```

See also [this issue](https://github.com/microsoft/pyright/issues/130) in the Pyright repository.

## Contributing

Run the following command in a terminal to link the `mage` command to your checkout:

```
pip3 install -e '.[dev]'
```

## License

This code is generously licensed under the MIT license.

