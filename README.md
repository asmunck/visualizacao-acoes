# Análise e Visualização de Ações Brasileiras

Esta aplicação web foi desenvolvida com Streamlit para criar visualizações interativas de dados de ações da bolsa brasileira (B3). O projeto proporciona uma ferramenta intuitiva para analisar as tendências históricas, correlações e estatísticas de ações selecionadas.

## Funcionalidades

- Visualização de preços históricos de ações brasileiras
- Comparação entre múltiplas ações em diferentes períodos
- Análise estatística de desempenho e volatilidade
- Visualização de correlações entre ativos
- Diferentes modos de visualização (preços absolutos, normalizados e retornos)

## Como executar

1. Clone este repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```
   streamlit run app.py
   ```

## Estrutura do projeto

```
visualizacao-acoes/
├── app.py                 # Ponto de entrada da aplicação
├── data/                  # Diretório para dados
│   └── tickers.csv        # Lista de tickers disponíveis com metadados
├── modules/               # Módulos da aplicação
│   ├── data_loader.py     # Funções para carregar dados
│   ├── visualizations.py  # Funções de visualização
│   └── analysis.py        # Funções de análise
├── README.md              # Documentação
└── requirements.txt       # Dependências
```

## Dados

Os dados históricos são obtidos em tempo real através da API do Yahoo Finance (via biblioteca yfinance), permitindo acesso a preços atualizados e informações financeiras de diversas empresas listadas na B3.