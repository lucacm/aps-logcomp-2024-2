
## EBNF

```ebnf
<programa> ::= { <funcao> } <chamada_funcao_principal>

<funcao> ::= "chanson" <identificador> "(" [ <declaracao_parametros> ] ")" ":" <tipo> "{" <bloco_comandos> "}"
<declaracao_parametros> ::= <tipo> <identificador> { "," <tipo> <identificador> }
<tipo> ::= "entier" | "paroles" | "sentiment" | "rien"

<bloco_comandos> ::= { <comando> }

<comando> ::= <declaracao_variavel> ";"
            | <atribuicao> ";"
            | <condicional>
            | <loop>
            | <refrain>
            | "affiche" "(" <expressao> ")" ";"
            | "demande" "(" <identificador> ")" ";"
            | "retourne" <expressao> ";"
            | <chamada_funcao> ";"

<declaracao_variavel> ::= <tipo> <identificador> [ "prend" <expressao> ] { "," <identificador> [ "prend" <expressao> ] }
<atribuicao> ::= <identificador> "prend" <expressao>

<condicional> ::= "choix" "(" <relative_expression> ")" "alors" "{" <bloco_comandos> "}" 
                [ "sinon si" "(" <relative_expression> ")" "alors" "{" <bloco_comandos> "}" ] 
                [ "sinon" "{" <bloco_comandos> "}" ]

<loop> ::= <tant_que>
<tant_que> ::= "tant_que" <relative_expression> "{" <bloco_comandos_loop> "}"
<bloco_comandos_loop> ::= { <comando> | "je_taime" ";" | "je_te_hais" ";" }

<refrain> ::= "refrain" <numero> "{" <bloco_comandos> "}"

<chamada_funcao_principal> ::= <chamada_funcao> ";"
<chamada_funcao> ::= <identificador> "(" [ <lista_argumentos> ] ")"
<lista_argumentos> ::= <expressao> { "," <expressao> }

<relative_expression> ::= <expression> ("egal" | "superieur_a" | "moins_que") <expression>
<expression> ::= <termo> { ("ajoute" | "moins" | "ou") <termo> }
<termo> ::= <fator> { ("fois" | "sur" | "et") <fator> }
<fator> ::= <numero>
          | <string>
          | <booleano>
          | <identificador>
          | <chamada_funcao>
          | "non" <fator>
          | "(" <expression> ")"
          | "meilleure" "(" <expression> "," <expression> ")"
          | "pire" "(" <expression> "," <expression> ")"

<booleano> ::= "amour" | "haine"
<numero> ::= <digito> { <digito> }
<string> ::= '"' { <caractere> } '"'
<identificador> ::= <letra> { <letra> | <digito> | "_" }
<caractere> ::= qualquer símbolo ASCII, exceto aspas duplas (")
<digito> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<letra> ::= qualquer letra (a-z ou A-Z)

```
