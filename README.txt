Projeto para cálculo de Prazo e Frete, dado parâmetros como custo, rota e peso.


=============== AMBIENTE =======================
Para execução deste projeto utilizamos as seguintes estruturas

VirtualEnv
https://virtualenv.pypa.io/en/stable/installation/ (para trabalhar num ambiente isolado com as respectivas bibliotecas)

Uma vez instalado executar o seguinte comando para criação do enviroment :

virtualenv NOME_ENV

Instalação de pacotes (uma vez instalado e criado o VirtualEnv específico e estando dentro dele) :

pip install -r requirements.txt


=============== EXECUÇÃO DO SISTEMA =======================

meli.py saopaulo florianopolis 50 130

Exemplo de Saída

=============================
TABELA | PRAZO | VALOR
tabela |  1    | 1393.09
=============================
=============================
TABELA  | PRAZO | VALOR
tabela2 |  -    | -
=============================


=============== EXECUÇÃO DOS TESTES =======================

Estando no raiz do projeto basta executar:

make tests