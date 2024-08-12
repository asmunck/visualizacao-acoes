# importar as bibliotecas
import streamlit as st
import pandas as pd 
import yfinance as yf

#criar funcoes
@st.cache_data
def carregar_dados(empresa):
    dados_acao = yf.Ticker(empresa)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-08-01")
    cotacoes_acao = cotacoes_acao[["Close"]]
    return cotacoes_acao

#preparar visualizacoes
dados = carregar_dados("PETR4.SA")
#criar a interface
st.write("""# Preço de Ações
O gráfico abaixo representa a evolução do preço das ações da Petrobrás(PETR4) ao longo dos anos""") #markdown

st.line_chart(dados) #grafico de linha
