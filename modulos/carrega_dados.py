import pandas as pd
import yfinance as yf
import streamlit as st
import os

@st.cache_data
def load_ticker_data(tickers, start_date="2010-01-01", end_date="2024-08-01", interval="1d"):
    """Carrega dados históricos para os tickers especificados"""
    if not tickers:
        return None
    
    data = yf.download(tickers, start=start_date, end=end_date, interval=interval)
    
    # Se apenas um ticker for solicitado, o yfinance retorna um DataFrame diferente
    if len(tickers) == 1:
        data = data.rename(columns={"Close": tickers[0]})
        return pd.DataFrame(data["Close"])
    
    return data["Close"]

@st.cache_data
def load_available_tickers():
    """Carrega a lista de tickers disponíveis do arquivo CSV"""
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "tickers.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame(columns=["ticker", "name", "sector"])

def get_ticker_info(ticker):
    """Obtém informações detalhadas sobre um ticker específico"""
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        return info
    except:
        return None