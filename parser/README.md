[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/TrocbgRE)
# IF688 - Teoria e Implementação de Linguagens Computacionais

## Atividade 2 - LL(1) parsing

Este exercício visa trabalhar os conceitos de análise sintática *top-down* vistos em sala de aula. A ideia é implementar um gerador de parsers LL(1) para gramáticas livres de contexto, usando as funções `FIRST` e `FOLLOW`.

Para simplificar o processo de desenvolvimento, é fornecido aqui um esqueleto de código disponível em `ll1parser.py` como ponto de partida para implementar o analisador, bem como alguns testes para verificar a corretude da sua implementação usando a biblioteca `pytest` (se não tiver a biblioteca instalada, rode `pip3 install pytest`). 

**O seu repositório será avaliado automaticamente pelo Github Classroom, rodando os testes por meio de uma Github Action. Esta ferramenta só avalia commits enviados até a data limite, portanto tenha em mente isso.**

O único arquivo que deve ser enviado **também** no Google Classroom é a sua versão de `ll1parser.py`, e o nome do arquivo deve ser o seu login. Então, no meu caso seria `lmt.py`.

## Instruções

A sua resolução precisa implementar as funções a seguir. O código já existente em cada uma destas funções **não precisa, nem deve** ser modificado.

- `buildFirstSets`
  - A versão inicial da função já inicializa os conjuntos `FIRST` de cada um dos terminais da gramática e dos símbolos especiais (ε e $) como sendo o próprio símbolo, além de definir um conjunto vazio para cada um dos não-terminais. 
  - Como resultado da execução da função, os conjuntos `FIRST` de cada um dos não-terminais devem ser corretamente populados com os seus respectivos símbolos terminais ou ε.
- `buildFollowSets`
  - A versão inicial da função já inicializa os conjuntos `FOLLOW` de cada um dos não-terminais da gramática com o conjunto vazio, com exceção do símbolo inicial, que já recebe $ (EOF) como parte do conjunto. 
  - Como resultado da execução da função, os conjuntos `FOLLOW` de cada um dos não-terminais devem ser corretamente populados com os seus respectivos símbolos terminais ou $.
- `generateParsingTable`
  - A versão inicial da função já fornece uma estrutura para a tabela de parsing, onde cada índice de `parsingTable` é um símbolo (objeto) não-terminal, que aponta para um dicionário onde as chaves são as strings dos terminais + EOF ($).
  - Como resultado da execução da função, a tabela de parsing deve ser populada com o lado direito da produção associada com a combinação Não-terminal + Terminal.
- `checkIfLL1`
  - A versão inicial da função sempre retorna `True`, o que nem sempre está correto.


## ATENÇÃO!

Você _não precisa_, *nem deve*, alterar nada do esqueleto de projeto dado além do arquivo `ll1parser.py` com a sua implementação.

### Testando o Projeto
- Faça o download deste projeto;
- Caso ainda não tenha `pytest` instalada, rode `pip3 install pytest`
- Na linha de comando, rode `pytest` e veja que a maioria dos testes não estão passando; 
- Implemente as funções descritas acima em `ll1parser.py`, usando apenas a parte dedicada do arquivo para tanto;
- Use o arquivo `main.py` se quiser rodar algo no console e observar o *output*.