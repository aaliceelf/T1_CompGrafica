# T1_CompGrafica

## Descrição

Este projeto implementa, em Python com OpenGL, um programa interativo para realizar testes de inclusão de um ponto em um conjunto de triângulos bidimensionais.

O usuário pode movimentar um ponto no cenário e o programa identifica quais triângulos contêm esse ponto, destacando-os visualmente. Para acelerar as consultas, foram implementadas diferentes etapas de filtragem, permitindo comparar o comportamento entre força bruta e estruturas de aceleração.

## Funcionalidades implementadas

O programa permite executar as seguintes configurações:

1. *Força bruta*  
   Aplica o teste detalhado em todos os triângulos.

2. *Envelopes AABB + teste detalhado*  
   Utiliza retângulos envolventes para descartar triângulos antes do teste detalhado.

3. *Subdivisão espacial (grade uniforme) + teste detalhado*  
   Consulta apenas os triângulos associados à célula da grade onde o ponto está.

4. *Subdivisão espacial + envelopes AABB + teste detalhado*  
   Combina as duas técnicas de aceleração antes do teste final.

Além disso, o programa permite:

- exibir ou ocultar a grade uniforme;
- exibir ou ocultar os envelopes AABB;
- exibir ou ocultar candidatos intermediários;
- alterar a resolução da grade;
- gerar cenários aleatórios reproduzíveis por semente;
- carregar triângulos a partir de arquivo CSV;
- exibir informações de desempenho no terminal.

---

## Organização da solução

A solução foi organizada separando os principais componentes do sistema:

### 1. Dados geométricos
Responsáveis por representar os elementos básicos do problema.

- geometry/geometria.py  
  Contém as classes:
  - Ponto
  - Envelope
  - Triangulo

### 2. Estruturas de aceleração
Responsáveis por reduzir o conjunto de candidatos antes do teste detalhado.

- grade.py  
  Implementa a *subdivisão espacial por grade uniforme*.

### 3. Algoritmos de teste
Responsáveis por executar os testes geométricos.

- algoritmos.py  
  Implementa o *teste detalhado de inclusão de ponto em triângulo*.

- consultas.py  
  Coordena a execução dos modos de consulta:
  - força bruta;
  - AABB;
  - grade;
  - grade + AABB.

### 4. Visualização
Responsável pela interface gráfica e interação do usuário.

- renderizacao.py  
  Implementa a visualização com OpenGL, o desenho dos triângulos, envelopes, grade e ponto de consulta.

### 5. Geração e carregamento de cenários
Responsável por criar os dados usados na execução.

- cenario.py  
  Gera triângulos aleatórios ou carrega triângulos de um arquivo CSV.

### 6. Execução principal
Responsável por iniciar o programa.

- main.py

### 7. Testes e experimentos
Responsáveis por validar a correção e medir desempenho.

- testes_validacao.py
- experimentos.py

---
## Estrutura de arquivos

```text
T1_CompGrafica/
├── geometry/
│   ├── _init_.py
│   └── geometria.py
├── algoritmos.py
├── cenario.py
├── consultas.py
├── experimentos.py
├── grade.py
├── main.py
├── renderizacao.py
├── testes_validacao.py
├── requirements.txt
├── resultados_experimentos.csv
├── resultados_construcao.csv
└── README.md

---

 ## Instalação e execução
 
 1.Clonar o repositório
    git clone https://github.com/aaliceelf/T1_CompGrafica.git
    cd T1_CompGrafica

 2. Criar e ativar o ambiente virtual 

    macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate

    Windows
    python -m venv .venv
    .venv\Scripts\activate

 3. Instalar as dependências
    python -m pip install -r requirements.txt

 4. Executar o programa
    python main.py

 ## Exemplos de execução

    Gerar 100 triângulos com semente 42
    python main.py --n 100 --semente 42

    Gerar 1000 triângulos
    python main.py --n 1000 --semente 42

    Gerar triângulos maiores
    python main.py --n 500 --semente 42 --min 60 --max 120

    Carregar triângulos de arquivo CSV
    python main.py --arquivo triangulos.csv


 ## Controles do programa

    Mouse

    * Move o ponto de consulta no cenário.

    Teclado

    * 1 → força bruta
    * 2 → envelopes AABB + teste detalhado
    * 3 → grade uniforme + teste detalhado
    * 4 → grade uniforme + AABB + teste detalhado
    * G → exibir/ocultar grade
    * E → exibir/ocultar envelopes
    * C → exibir/ocultar candidatos intermediários
    * + → aumentar a resolução da grade
    * - → diminuir a resolução da grade
    * Esc → encerrar o programa


 ## Informações exibidas

    Durante a execução, o terminal apresenta:

    * quantidade total de triângulos;
    * quantidade de candidatos da subdivisão espacial;
    * quantidade de candidatos aprovados pelo envelope;
    * quantidade de testes detalhados executados;
    * quantidade de triângulos que contêm o ponto;
    * tempo de consulta;
    * tempo de construção da grade;
    * número de referências armazenadas na grade.

    ⸻

 ## Validação

    Para executar os testes de validação:
    python testes_validacao.py



    Esse script verifica a consistência entre os quatro modos de consulta em diferentes cenários, incluindo:

    * pontos internos e externos;
    * pontos sobre arestas e vértices;
    * triângulos sobrepostos;
    * fronteiras da grade;
    * pontos aleatórios.

 ## Experimentos de desempenho

    Para executar os experimentos e gerar os arquivos CSV com os resultados:
    python experimentos.py

    Serão gerados:

    * resultados_experimentos.csv
    * resultados_construcao.csv

    Esses arquivos contêm os dados utilizados para a análise de desempenho no relatório.