test:
	syntax-cli -g ax-lang-grammar.bnf.g -m LALR1 -p "42" --tokenize # check number
	syntax-cli -g ax-lang-grammar.bnf.g -m LALR1 -p "\"Hello\"" --tokenize # check string
	syntax-cli -g ax-lang-grammar.bnf.g -m LALR1 -p "foo" --tokenize # check symbol
	syntax-cli -g ax-lang-grammar.bnf.g -m LALR1 -p "(+ 5 foo)" --tokenize # check list
	syntax-cli -g ax-lang-grammar.bnf.g -m LALR1 -p "(begin (var x 10)(var y 20)(+ x y))" # check complex
