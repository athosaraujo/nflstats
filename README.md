# Dashboard 
Trabalho da matéria de Estatística e Probablidiade do 4 semestre de Engenharia da Computação, consistindo na montagem de um Dashboard a partir de um banco de dados obtidos no Kaggle.

## Montagem
Para a montagem desse Dashboard se foi utilizado um banco de dados obtidos no seguinte link: https://www.kaggle.com/datasets/kendallgillies/nflstatistics
Tal banco de dados consiste em informações sobre jogadores que já passaram e jogam atualmente na NFL, como idade, numero da camisa, time, experiencia, cidade natal e faculdade de escolha.

## Tratamento de dados
No arquivo dataTreat.py é extraido as informações do arquivo "Basic_Stats.csv", obtido no repositório do Kaggle, transcrevendo as mesmas para um arquivo "processedData.csv", onde se é retirado todos os jogadores aposentados e com informações incompletas.

## Ferramentas utilizadas
Neste trabalho foi-se utilizado as bibliotecas **plotly**, **dash**, e **pandas** do Python, tendo as duas primeiras como ferramentas de plotagem de gráficos e a implementação de tais gráficos em uma aplicação no localhost::1251.

O pandas em si é uma biblioteca voltada ao manuseio e montagem de DataFrames que podem ser manipulados e visualizados pelo usuário.

## Gráficos e Tabela
O projeto do Dashboard consiste em 3 partes principais.

A primeira sendo onde o usuário pode ver um gráfico de linha da idade de cada jogador em dado time, onde os times são selecionados através de um menu dropdown.

A segunda parte consiste em dois gráficos circulares mostrando as dez cidades com mais jogadores nativos e as dez universidades que mais deram início a carreira dos jogadores.

A terceira parte consiste em um outro menu dropdown onde o usuário seleciona apenas um time para ver a tabela com informações mais detalhadas de cada jogador presente.
