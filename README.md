Mage: Text Analysis Made Easy
=============================

Mage is tool for performing text analysis. It does so by generating a _lexer_,
_parser_ and _parse tree_ for you. Whether it is a piece of programming code or
some tabular data in a fringe format, Mage has got you covered!

### Installation

```
$ pip3 install --user -U magelang
```

## Usage

### `mage generate <filename>`

Generate a parser for the given grammar in a language that you specify.

### `mage test <filename..>`

Run all tests inside the documentation of the given grammar.

## Grammar

### `rule = expr`

Define a new inline rule that can be used inside other rules.

As the name suggests, this type of rule is merely syntactic sugar and gets
inlined whenever it is referred to inside another rule.

```
digits = [0-9]+
```

### `pub rule = expr`

Define a new node that must be parsed according the given expression.

You can use both inline rules and other node rules inside `expr`. When
referring to another node, that node will become a field in the node that
referred to it. Nodes that have no fields are converted to a special token type
that is more efficient to represent.

```
pub float-expression
  = digits? '.' digits
```

### `expr1 expr2`

First parse `expr1` and continue to parse `expr2` immediately after it.

```
pub two-column-csv-line
  = text ',' text '\n'
```

### `expr1 | expr2`

First try to parse `expr1`. If that fails, try to parse `expr2`. If none of the
expressions matched, the parser fails.

```
pub declaration
  = function-declaration
  | let-declaration
  | const-declaration
```

### `expr?`

Parse or skip the given expression, depending on whether the expression can be
parsed.

```
pub singleton-or-pair
  = value (',' value)?
```

### `expr*`

Parse the given expression as much as possible.

```
skip = (multiline-comment | whitespace)*
```

### `expr+`

Parse the given expression one or more times.



### `expr{n,m}`

Parse the expression at least `n` times and at most `m` times.

```
unicode-char = 'U+' hex-digit{4,4}
```

## Contributing

Run the following command in a terminal to link the `mage` command to your checkout:

```
pip3 install -e '.[dev]'
```

## License

This code is generously licensed under the MIT license.

