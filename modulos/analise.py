import pandas as pd
import numpy as np
import streamlit as st

def calculate_statistics(data):
    """Calcula estatísticas dos preços das ações"""
    if data is None or data.empty:
        return None
    
    # Retornos diários
    returns = data.pct_change().dropna()
    
    stats = pd.DataFrame()
    
    # Estatísticas de preço
    stats['Preço Atual'] = data.iloc[-1]
    stats['Preço Mínimo'] = data.min()
    stats['Preço Máximo'] = data.max()
    stats['Preço Médio'] = data.mean()
    
    # Estatísticas de retorno
    stats['Retorno Anualizado (%)'] = returns.mean() * 252 * 100
    stats['Volatilidade Anual (%)'] = returns.std() * np.sqrt(252) * 100
    stats['Sharpe Ratio'] = (returns.mean() * 252) / (returns.std() * np.sqrt(252))
    
    # Retorno acumulado no período
    stats['Retorno Total (%)'] = ((data.iloc[-1] / data.iloc[0]) - 1) * 100
    
    return stats.T

def calculate_moving_averages(data, window_short=50, window_long=200):
    """Calcula médias móveis dos preços"""
    if data is None or data.empty:
        return None
    
    result = pd.DataFrame(index=data.index)
    
    for ticker in data.columns:
        result[f"{ticker}"] = data[ticker]
        result[f"{ticker}_MA{window_short}"] = data[ticker].rolling(window=window_short).mean()
        result[f"{ticker}_MA{window_long}"] = data[ticker].rolling(window=window_long).mean()
    
    return result

def calculate_monthly_returns(data):
    """Calcula retornos mensais para as ações"""
    if data is None or data.empty:
        return None
    
    monthly_data = data.resample('M').last()
    
    monthly_returns = monthly_data.pct_change().dropna()
    
    return monthly_returns