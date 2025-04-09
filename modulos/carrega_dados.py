import pandas as pd
import yfinance as yf
import streamlit as st
import os
import time

@st.cache_data
def load_ticker_data(tickers, start_date="2010-01-01", end_date="2024-08-01", interval="1d"):
    """Carrega dados históricos para os tickers especificados com tratamento de erros aprimorado"""
    if not tickers:
        return None
    
    # Para cada ticker, tente carregar individualmente para maior confiabilidade
    result_data = pd.DataFrame()
    
    for ticker in tickers:
        try:
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(start=start_date, end=end_date, interval=interval)
            
            if not hist.empty:
                # Adiciona os dados ao DataFrame resultante
                result_data[ticker] = hist["Close"]
            else:
                st.warning(f"Nenhum dado encontrado para {ticker}")
            
            # Pequena pausa para evitar limitação de requisições
            time.sleep(0.5)
        except Exception as e:
            st.warning(f"Erro ao carregar dados para {ticker}: {str(e)}")
    
    return result_data if not result_data.empty else None

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