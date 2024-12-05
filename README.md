# Ma Meilleure Ennemie (MME)

**Ma Meilleure Ennemie (MME)** é um projeto desenvolvido como parte da disciplina de **Lógica de Computação** do **Insper**. O objetivo inicial foi criar uma linguagem de programação que traduzisse os conceitos tradicionais de linguagens baseadas em inglês, como o C, para o francês. A ideia era tornar a programação mais acessível e educativa para falantes de francês, sejam crianças, adultos ou iniciantes.

A linguagem nasceu da base de um compilador em C que foi construído ao longo da disciplina e, posteriormente, adaptado para reconhecer e executar essa nova linguagem. A princípio, a intenção era criar uma linguagem funcional, com comandos e palavras-chave em francês, mas ainda faltava algo: uma identidade única.

Foi então que encontrei inspiração na música **"Ma Meilleure Ennemie"**, uma canção francesa que conheci através da animação da Netflix **Arcane**. A música aborda a dualidade dos sentimentos, como amor e ódio, e é a música tema de dois personagens **Ekko** e **Powder**, não irei dar mais detalhes para não dar _spoilers_. Inspirado então por essa temática e movido pelo desejo de criar uma linguagem poética e expressiva, decidi incorporar elementos da música na linguagem.

O resultado é uma linguagem que vai além da tradução literal. Ela carrega um toque de poesia e personalidade, com comandos que evocam sentimentos, relações e beleza. *Ma Meilleure Ennemie* não é apenas uma linguagem para programar, mas também uma forma de expressão, combinando funcionalidade com uma estética mais falada e fluida.

![](timebomb.png)

[Vídeo explicativo sobre a linguagem](https://drive.google.com/file/d/10YThpiDaOlq5b40yW7wbkWA9v_9WyZ_U/view?usp=sharing)

[Link da música no YouTube](https://www.youtube.com/watch?v=1F3OGIFnW1k)

[Link da letra da música](https://genius.com/Stromae-and-pomme-ma-meilleure-ennemie-lyrics)

[Link da tradução da letra da música](https://www.letras.mus.br/stromae/ma-meilleure-ennemie-feat-pomme/traducao.html)



## Funcionalidades e Destaques

### **Função Principal**

A função principal de um programa em *Ma Meilleure Ennemie* deve obrigatoriamente se chamar:

```
ma_meilleure_ennemie
```

Ela é o ponto de entrada para execução do código e deve ser definida como `rien`, ou seja, sem retorno de valor.

**Exemplo:**

```c
chanson ma_meilleure_ennemie(): rien {
    affiche("Bienvenue à Ma Meilleure Ennemie!");
}
```

#

### **Mensagens de Erro**

As mensagens de erro na linguagem seguem o tema francês, proporcionando um toque único. Por exemplo:

- **Erro de sintaxe:** `"Ce symbole est une malédiction, il ne devrait pas exister ici."`  
- **Identificador inválido:** `"Identifiant non valide trouvé dans le code."`  
- **Variável não declarada:** `"Cette variable n’a pas été déclarée."`  

Essas mensagens ajudam o desenvolvedor a depurar o código de forma clara e alinhada ao tema poético da linguagem.

#



### **Bloco `refrain`**

Permite repetições fixas, como um refrão de música. Similar ao `for`.

**Exemplo:**
```c
refrain 3 {
    affiche("Refrain...");
}
```

#

### **`sinon si` (elseif)**

Extensão do `choix`, permitindo condições intermediárias.  
**Exemplo:**
```c
choix (x superieur_a y) alors {
    affiche("x est superieur à y");
} sinon si (x egal y) alors {
    affiche("x est egal à y");
} sinon {
    affiche("x est moins que y");
}
```

#

### **`je_taime` (continue) e `je_te_hais` (break)**

Controle de fluxo para loops do tipo `tant_que`.  
**Exemplo:**
```c
tant_que x moins_que 10 {
    choix (x egal 5) alors {
        x prend x ajoute 1;
        je_taime;
    }
    affiche(x);
    x prend x ajoute 1;
}
```

#

### **Funções internas `meilleure` e `pire`**

Funções internas que retornam o maior ou menor valor entre dois números.  
**Exemplo:**
```c
entier max prend meilleure(10, 20);
entier min prend pire(5, 15);
```

#

### **Tipo Booleano**

Tipo `sentiment` com valores `amour` (verdadeiro) e `haine` (falso). Similares ao `true` e `false`. 

**Exemplo:**
```c
sentiment vrai prend amour;
sentiment faux prend haine;
```

#

### **Operadores Personalizados**

Substituem operadores tradicionais:
- Matemáticos: `ajoute` (`+`), `moins` (`-`), `fois` (`*`), `sur` (`/`).
- Comparação: `egal` (`==`), `superieur_a` (`>`), `moins_que` (`<`).
- Lógicos: `et` (`&&`), `ou` (`||`), `non` (`!`).
- Tipos : `paroles` (`str`), `entier` (`int`), `rien`, (void)

Essas e outras substituições personalizadas foram pensadas para dar mais sentido ao tema da linguagem. Consultar a lista de palavras reservadas no código [main.py](main.py) para mais detalhes.


#
## [EBNF](ebnf.md)

## [Exemplo de Código](test.md)
