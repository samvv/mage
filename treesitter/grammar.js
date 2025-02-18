/// <reference types="tree-sitter-cli/dsl" />
// @ts-check

module.exports = grammar({
  name: 'mage',
  conflicts: $ => [
    [ $._prim_expr ]
  ],
  rules: {
    grammar: $ => repeat($.module_element),
    module_element: $ => choice(
      $.rule,
      $.module,
    ),
    module: $ => seq(
      'mod',
      field('name', $.identifier),
      '{',
      repeat($.module_element),
      '}'
    ),
    identifier: _ => /[a-zA-Z_][a-zA-Z0-9_]*/,
    integer: _ => /[0-9]+/,
    rule: $ => seq(
      optional('pub'),
      optional('token'),
      field('name', $.identifier),
      '=',
      $.expr,
    ),
    _prim_expr: $ => seq(
      field('label', optional(seq($.identifier, ':'))),
      choice(
        $.lit_expr,
        $.ref_expr,
        $.opt_expr,
        $.many_expr,
        $.some_expr,
        $.repeat_expr,
        $.nest_expr,
      )
    ),
    choice_expr: $ => prec.left(4, seq(
      $.expr,
      '|',
      $.expr,
    )),
    expr: $ => choice(
      $.choice_expr,
      $.seq_expr,
      $._prim_expr,
    ),
    escape_sequence: _ => token(prec(1, seq(
      '\\',
      choice(
        /u[a-fA-F\d]{4}/,
        /U[a-fA-F\d]{8}/,
        /x[a-fA-F\d]{2}/,
        /\d{1,3}/,
        /\r?\n/,
        /['"abfrntv\\]/,
        /N\{[^}]+\}/,
      ),
    ))),
    lit_expr: $ => seq(
      '"',
      repeat(choice(
        token.immediate(prec(1, /[^\\"\n]+/)),
        $.escape_sequence
      )),
      '"'
    ),
    ref_expr: $ => $.identifier,
    seq_expr: $ => prec.left(5, seq($._prim_expr, $._prim_expr)),
    opt_expr: $ => seq($._prim_expr, '?'),
    some_expr: $ => seq($._prim_expr, '+'),
    many_expr: $ => seq($._prim_expr, '*'),
    repeat_expr: $ => seq(
      $._prim_expr,
      '{',
      $.integer,
      optional(seq(',', optional($.integer))),
      '}'
    ),
    nest_expr: $ => seq(
      '(',
      $.expr,
      ')',
    )
  }
})
