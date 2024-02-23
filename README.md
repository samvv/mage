Mage: Text Analysis Made Easy
=============================

Mage is tool for performing text analysis. It does so by generating a _lexer_,
_parser_ and _parse tree_ for you. Whether it is a piece of programming code or
some tabular data in a fringe format, Mage has got you covered!

 - 🚀 Full support for Python typings. Avoid runtime errors while building your language!
 - ➕ Add your own languages through the use of a powerful template engine!

👀 Mage is written in itself. Check out the [generated code][1] of our Python generator!

Here is the status of the various languages supported by Mage:

**Python**

| Name   | Description | Status |
|--------|-------------|--------|
| CST    | Create a parse tree from a grammar | ✅ |
| AST    | Create an AST that is derived from a CST | ⏳ |
| Lexer  | Create a fully functioning lexer from a grammar | ⏳ |
| Parser | Create a fully functioning parser from a grammmar | ⏳ |

[1]: https://github.com/samvv/mage/blob/main/src/magelang/lang/python/cst.py

## Installation

```
$ pip3 install --user -U magelang
```

## Usage

### `mage generate <filename>`

Generate a parser for the given grammar in a language that you specify.

**Example**
```
mage generate foo.mage python --prefix foo --out-dir src/foolang
```

### `mage test <filename..>`

**🚧 This command is under construction.**

Run all tests inside the documentation of the given grammar.

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
This usually means that the rule references another rule that is `pub`.

```
pub token float_expression
  = digits? '.' digits
```

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

## Contributing

Run the following command in a terminal to link the `mage` command to your checkout:

```
pip3 install -e '.[dev]'
```

## License

This code is generously licensed under the MIT license.

