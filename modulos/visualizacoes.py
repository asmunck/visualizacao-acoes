import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def plot_price_evolution(data, normalize=False):
    """
    Renderiza gráfico de evolução de preços
    normalize: se True, normaliza os preços para base 100
    """
    if data is None or data.empty:
        st.warning("Nenhum dado disponível para exibir")
        return
    
    # Detectar o tema atual
    theme = st.session_state.get('theme', 'Escuro')
    plotly_template = "plotly_white" if theme == "Claro" else "plotly_dark"
    
    fig = None
    
    if normalize:
        # Normaliza para base 100
        normalized_data = data.copy()
        for col in normalized_data.columns:
            normalized_data[col] = 100 * normalized_data[col] / normalized_data[col].iloc[0]
        
        fig = px.line(
            normalized_data, 
            title="Evolução Normalizada de Preços (Base 100)",
            labels={"value": "Preço Normalizado", "variable": "Ação", "date": "Data"},
            template=plotly_template
        )
    else:
        fig = px.line(
            data,
            title="Evolução de Preços de Fechamento",
            labels={"value": "Preço (R$)", "variable": "Ação", "date": "Data"},
            template=plotly_template
        )
    
    # Cor de fundo transparente
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        legend_title="Ações",
        hovermode="x unified",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_returns_heatmap(data):
    """Gera um heatmap de correlação entre retornos diários"""
    if data is None or data.empty:
        st.warning("Nenhum dado disponível para exibir")
        return
    
    # Detectar o tema atual
    theme = st.session_state.get('theme', 'Escuro')
    plotly_template = "plotly_white" if theme == "Claro" else "plotly_dark"
    
    # Calcular retornos diários
    returns = data.pct_change().dropna()
    
    # Calcular matriz de correlação
    corr_matrix = returns.corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        title="Correlação entre Retornos Diários",
        template=plotly_template
    )
    
    # Cor de fundo transparente
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_performance_chart(data):
    """Mostra gráfico de desempenho acumulado"""
    if data is None or data.empty:
        st.warning("Nenhum dado disponível para exibir")
        return
    
    # Detectar o tema atual
    theme = st.session_state.get('theme', 'Escuro')
    plotly_template = "plotly_white" if theme == "Claro" else "plotly_dark"
    
    # Calcular retorno percentual cumulativo
    returns = (1 + data.pct_change().fillna(0)).cumprod() - 1
    
    fig = px.line(
        returns * 100,
        title="Retorno Acumulado (%)",
        labels={"value": "Retorno (%)", "variable": "Ação", "date": "Data"},
        template=plotly_template
    )
    
    # Cor de fundo transparente
    fig.update_layout(
        hovermode="x unified",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)