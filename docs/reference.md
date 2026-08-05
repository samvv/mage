# Mage Language Reference

Mage is a parser generator that is loosely based on PEGs.

In what follows, anything between two angle brackets is a metavariable. The
remaining text should be taken literally.

## Trivia

Trivia are in this context fragments of text that are mostly uninteresting to
the generator, like whitespace and comments.

### Whitespace

Whitespace consists just of the usual set of empty space (`' '`), tab (`'\t'`), newline
(`'\n'`) and carriage return (`'\r'`). Any of these characters will be skipped
in the source code.

### Line comments

The simplest form of comments are line comments. They can be started with the
hashtag symbol (`#`) and continue till the end of the line.

### Doc-comments

Doc-comments are a special kind of comment that contain additional information
about a rule; useful for documentation and testing.

**Example Usage**
```mage
## This is a rule called 'foo'.
##
## With this doc-comment you can specify tests that operate on this rule:
##
## {accept}
## helloworld
## {/accept}
##
## {reject}
## nothelloworld
## {/reject}
##
## {reject}
## helloworlddanglingtext
## {/reject}
pub foo = 'helloworld'
```

## Rules

### `pub <name> = <expr>`

Define a new node or token that must be parsed according the given expression.

You can use both inline rules and other node rules inside `expr`. When
referring to another node, that node will become a field in the node that
referred to it. Nodes that have no fields are converted to a special token type
that is more efficient to represent.

**Example Usage**
```mage
pub var_decl = 'var' name:ident '=' type_expr
```

### `<name> = <expr>`

Define a new inline rule that can be used inside other rules.

As the name suggests, this type of rule is merely syntactic sugar and gets
inlined whenever it is referred to inside another rule.

**Example Usage**
```mage
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

**Example Usage**
```mage
pub token float
  = digits? '.' digits
```

### `pub token <name> -> <type_expr> = <expr>`

Like `pub token <name> = <expr>` but forces the value inside the token to be of
the specific type defined by `<type_expr>`.

**Example Usage**
```mage
pub token int -> Integer
  = digits
```

The conversion from the value to the type depends on which type is actually used.
For example, the following table is used when targeting Python:

| Mage Type | Python Type | Python Code   |
|-----------|-------------|---------------|
| Integer   | `int`       | `int(text)`   |
| Float     | `float`     | `float(text)` |

## Expressions

A postfix expression binds tighter than a prefix expression, which has a higher
precedence than a label expression, which has a higher precedence than a
sequence expression, which has a higher precedence than the choice expression.

Therefore, the following would be equal:

 - `try foo bar` as `(try foo) bar`
 - `foo bar | bax` as `(foo bar) | bax`
 - `!foo+` as `!(foo+)`.
 - `name:foo?` as `name:(foo?)`

### Character set expressions

A character set expression is started with `[` and ended with `]`. In between,
there are two possible elements that may be repeated: a single character or a
character range given by two characters separated by a hyphen (`-`).

Optionally, the letter `i` after the final `]` may indicate that the character
set is case-insensitive. The conversion algorithm is defined by the Unicode
standard for Unicode grammars.

Optionally, the elements may be preceded by a single caret (`^`), to indicate
that the parser should take the complement of the given character set. Should a
real caret be desired, the user may simply escape the caret with a backslash.

**Example Usage**
```mage
digit = [0-9]
letter = [a-z]i
identifier = [a-zA-Z_] [a-zA-Z0-9_]*
string = '"' [^"]* '"'
```

### Literal expressions

Literal expressions start with `"` for string literals and `'` for single
characters. They end with the same quotation mark as they start with.

**Example Usage**

```mage
pub helloworld
  = "Hello, world!"
```

```mage
pub alpha = 'α'
pub beta  = 'β'
pub gamma = 'γ'
```

### Reference expressions

A reference expression is written with a single identifier `<name>` that names
a rule defined within the grammar. Upon encountering a reference expression,
the parser will continue parsing the corresponding rule.

**Examples**
```mage
pub abc
  = alpha beta gamma
```

### `try <expr>`

Try to parse the given expression `<expr>`. On failure, the try-expression will
backtrack to right before `<expr>` was parsed.

This is useful in conjunction with a choice expression.

**Example Usage**
```mage
pub keyword_or_identifier
  = try "class"
  | try "struct"
  | identifier
```

### `<expr1> <expr2>`

First parse `<expr1>` and continue to parse `<expr2>` immediately after it.

**Example Usage**
```mage
pub two_column_csv_line
  = text ',' text '\n'
```

### `<expr1> | <expr2>`

First try to parse expression `<expr1>`. If that fails, try to parse expression
`<expr2>`. If none of the expressions matched, the parser fails locally.

**Example Usage**
```mage
pub declaration
  = function_declaration
  | let_declaration
  | const_declaration
```

### `<expr>?`

Parse or skip the given expression, depending on whether the expression can be
parsed.

**Example Usage**
```mage
pub singleton_or_pair
  = value (',' value)?
```

### `<expr>*`

Parse the given expression as much as possible.

**Example Usage**
```mage
skip = (multiline_comment | whitespace)*
```

### `<expr>+`

Parse the given expression one or more times.

**Example Usage**

In Python, there must always be at least one statement in the body of a class or function:

```mage
body = stmt+
```

### `<expr1> % <expr2>`

Denotes a list-expression, where a repetition of `<expr1>` is interspersed with
`<expr2>`.

Repeating the `%` symbol will result in the list requiring at least the amount
of `%` being typed minus one of occurrences of `<expr1>`. For instance, `'foo'
%%% '.'` parses `foo.foo` (two repetitions) but not `foo` (one repetition).

**Example Usage**
```mage
pub call_expr
  = expr '(' args:(expr % ',')* ')'
```

### `&<expr>`

Positive lookahead expression.

Peek into the future of the stream and determine whether `<expr>` matches. If
it does, rewind the stream and continue. If it doesn't, reject the input.

### `!<expr>`

Negative lookahead expression.

Peek into the future of the stream and determine whether `<expr>` matches. If
it does, reject the input. If it doesn't, rewind and continue.

**Example Usage**
```mage
pub line_comment = '#' (!'\n' any_char)* '\n'
```

### `\<expr>`

Mark an expression as being trivia. The expression will be parsed, but not be
visible in the resulting AST.

Lookahead expressions are automatically hidden.

### `<name>:<expr>`

Label the expression `<expr>` with the identifier `<name>`.

The label will be used to generate the correct field name for
the expression in the AST, among other things.

In most cases you don't need to specify the label as it will be inferred from
the expression. For example, if your expression is simply `type_annotation`,
the field will be called `type_annotation` as long as it doesn't conflict with
other fields.

**Example Usage**
```mage
pub struct_field = name:identifier ':' type_expr
```

### `<expr>{n,m}`

Parse the expression at least `n` times and at most `m` times.

`n` may be omitted. In this case, `n` defaults to 0. Likewise, if `m` is
omitted it defaults to infinity.

`,` may be omitted, in which case `n` will be equal to `m`. The value must be
supplied by the user.

**Example Usage**
```mage
unicode_char = 'U+' hex_digit{4}
```

## Decorators

Decorators have the form `@<name>` where `<name>` is a plain identifier.

### `@keyword`

Treat the given rule as being a potential source for keywords.

String literals matching this rule will get the special `_keyword`-suffix
during transformation. The lexer will also take into account that the rule
conflicts with keywords and generate code accordingly.

**Example Usage**
```mage
@keyword
pub token ident
  = [a-zA-Z_] [a-zA-Z_0-9]*
```

### `@trivia`

Register the chosen rule as a special rule that the lexer uses to lex trivia.

The rule will still be available in other rules, e.g. for when `@raw` was added.

**Example Usage**
```mage
@trivia
whitespace = [\n\r\t ]*
```

### 🚧 `@raw`

> [!WARNING]
>
> This decorator is under construction.

Disable automatic injection of the rule defined with `@trivia` for the chosen rule.

The injection will only be skipped for this rule and not any rule that is referenced by it.

This can be useful for e.g. parsing indentation in a context where whitespace
is normally discarded.

**Example Usage**
```mage
@trivia
__ = [\n\r\t ]*

@raw
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

**Example Usage**
```mage
@wrap
pub lit_expr
   = literal:(string | integer | boolean)
```

## Special Rules

The following rules are automatically injected by Mage at runtime.

### `any_char`

Matches a single character in the stream, without performing any checks on it.

### `eof`

The inverse of `any_char`. It represents the end of the stream, where no characters are present.

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

**Example Usage**
```mage
pub macro_call
  = name:ident '{' token* '}'
```

### `node`

A special rule that matches **any parseable node in the grammar**, excluding tokens.

### `syntax`

A special rule that matches **any rule in the grammar**, including tokens.

