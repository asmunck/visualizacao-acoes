# importar as bibliotecas
import streamlit as st
import pandas as pd 
import yfinance as yf

#criar funcoes
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(empresas)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-08-01")
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "BBDC4.SA", "LREN3.SA", "BBAS3.SA"]
dados = carregar_dados(acoes)

#preparar visualizacoes
lista_acoes = st.multiselect("Escolha as ações:", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})
    

#criar a interface
st.write("""# Preço de Ações
O gráfico abaixo representa a evolução do preço das ações ao longo dos anos""") #markdown

st.line_chart(dados) #grafico de linha
