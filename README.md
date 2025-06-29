# Simplex Solver
## Visão Geral
Este projeto é uma implementação computacional do método Simplex para resolver Problemas de Programação Linear (PPLs), desenvolvido como parte prática de uma disciplina de Pesquisa Operacional. O solver foi escrito em Python e construído do zero, sem dependência de bibliotecas externas de otimização matemática (como o linprog do SciPy).

A implementação utiliza o Método Simplex em Duas Fases, o que permite resolver problemas de maximização com uma combinação de restrições do tipo menor ou igual (<=), maior ou igual (>=) e igual (=). O código é modular e de fácil manutenção, com separação clara entre o parser de entrada, a padronização e a lógica principal do solver.

## Funcionalidades
- Resolve Problemas de Maximização: O algoritmo principal é voltado para problemas padrão de maximização.
- Suporte a Todos os Tipos de Restrição: Lida corretamente com restrições ≤, ≥ e = adicionando variáveis de folga, excesso e artificiais, conforme necessário.
- Método Simplex em Duas Fases: Detecta automaticamente quando uma base viável inicial não é evidente e executa a Fase I antes de prosseguir para a Fase II.
- Tratamento de Degenerescência: Inclui lógica para lidar com casos degenerados, nos quais uma variável artificial permanece na base com valor zero ao final da Fase I.
- Entrada via Arquivo: Os modelos de PPL são definidos em arquivos de texto simples e legíveis.
- Saída Detalhada: A solução final exibe um resumo completo com status, valor ótimo da função objetivo e os valores de todas as variáveis (decisão, folga, excesso e artificiais).

## Estrutura do Projeto
O projeto é organizado de forma modular, visando clareza de código e separação de responsabilidades.

```
simplex_project/
│
├── main.py                 # Ponto de entrada principal do solver.
│
├── core/
│   ├── __init__.py
│   ├── model_parser.py     # Faz o parser do arquivo de entrada.
│   ├── standardizer.py     # Converte o modelo para a forma padrão (normalização).
│   ├── tableau.py          # Classe que representa e opera sobre o tableau Simplex.
│   ├── pivoting.py         # Lógica de escolha das variáveis de entrada e saída.
│   └── solver.py           # Núcleo do algoritmo de resolução (método em duas fases).
│
├── examples/
│   ├── 001_simple-feasible.txt   # PPL simples que não requer Fase I.
│   └── 002_dual_phase.txt   # PPL mais complexo que requer o método em duas fases.
│   └── ...   # Outros PPL utilizados para testes
│
└── README.md               # Este arquivo de documentação.
```

## Requisitos
- Python 3.8 ou superior
- Biblioteca NumPy

## Instalação
1. Clone o repositório:

```bash
git clone <url-do-seu-repositório>
cd simplex_project
```

2. Crie e ative um ambiente virtual (recomendado):

- No macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

- No Windows:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install numpy
```

## Uso
O solver é executado via linha de comando, passando o caminho para o arquivo de entrada contendo o modelo de PPL.

- Comando

```bash
python main.py path/to/seu_arquivo_lpp.txt
```

## Formato do Arquivo de Entrada
O arquivo de entrada deve seguir um formato simples baseado em palavras-chave. Linhas em branco e comentários (iniciadas com #) são ignoradas.

As seções obrigatórias são:

- NUM_VARS: Número de variáveis de decisão (ex: x_1, x_2, ...).
- OBJECTIVE: Expressão da função objetivo, que será sempre de maximização.
- CONSTRAINTS: Lista de restrições, uma por linha.

#### Notação das Variáveis e Coeficientes
As variáveis devem ser escritas no formato x_1, x_2, etc.
Cada termo deve seguir a forma <coeficiente>x_<índice>, como 3x_2, 1x_1, etc.

- O coeficiente deve ser escrito antes da variável quando for diferente de 1. Exemplo correto: 4x_1 + 2x_2 <= 10
- Se o coeficiente for 1, ele pode ser omitido ou incluído:
    - Válido: x_1 + x_2 <= 10
    - Também válido: 1x_1 + 1x_2 <= 10

#### Exemplo Completo:

```makefile
# Problema de Programação Linear
# Maximize P = 2x_1 + 3x_2
# Sujeito a:
#   x_1 + x_2 >= 4
#   2x_1 + 5x_2 <= 15
#   4x_1 + 3x_2 = 18

NUM_VARS: 2

OBJECTIVE:
2x_1 + 3x_2

CONSTRAINTS:
1x_1 + 1x_2 >= 4
2x_1 + 5x_2 <= 15
4x_1 + 3x_2 = 18
```

## Saída Esperada

```
--- Solving LPP from file: examples/example_lpp_2.txt ---

--- Solution ---
Status: Optimal
Optimal Value: 11.5714

Variable Values (originals):
  x_1 = 3.2143
  x_2 = 1.7143

Slack / Surplus / Artificial Variables:
  e_1 = 0.9286
  s_1 = 0.0000

Basic Variables: ['e_1', 'x_1', 'x_2']
Non-Basic Variables: ['s_1']
```

## Limitações

- Critério de Desempate: A implementação atual não utiliza regras sofisticadas de desempate (como a Regra de Bland) para escolher variáveis de entrada/saída. Utiliza o comportamento padrão do argmin do NumPy, o que pode permitir ciclos em casos patológicos.
- Erros de Formato: O tratamento de erros para arquivos de entrada malformados é básico. Um formato muito incorreto pode gerar erros inesperados.
- Restrição Redundante com Artificial Inamovível: Em casos raros, uma restrição redundante pode fazer com que uma variável artificial permaneça na base ao fim da Fase I sem possibilidade de pivô para removê-la. Nestes casos, o programa lança um NotImplementedError.