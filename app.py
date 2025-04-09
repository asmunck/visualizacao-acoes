import streamlit as st
import pandas as pd
import datetime
from modulos.carrega_dados import load_ticker_data, load_available_tickers
from modulos.visualizacoes import plot_price_evolution, plot_returns_heatmap, plot_performance_chart
from modulos.analise import calculate_statistics, calculate_moving_averages, calculate_monthly_returns

# Configuração da página
st.set_page_config(
    page_title="Análise de Ações Brasileiras",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📊 Análise de Ações Brasileiras")
st.markdown(
    """
    Esta aplicação permite analisar a evolução histórica de preços de ações na bolsa brasileira.
    Selecione as ações e o período para visualizar diferentes análises e comparações.
    """
)

# Carregar dados disponíveis
tickers_df = load_available_tickers()
available_tickers = tickers_df["ticker"].tolist()
ticker_names = dict(zip(tickers_df["ticker"], tickers_df["name"]))

# Sidebar para seleção de parâmetros
st.sidebar.header("Configurações")

# Seleção de ações
selected_tickers = st.sidebar.multiselect(
    "Selecione as ações:",
    options=available_tickers,
    default=["PETR4.SA", "VALE3.SA"],
    format_func=lambda x: f"{x} - {ticker_names.get(x, x)}"
)

# Seleção de período
col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input("Data inicial:", datetime.date(2020, 1, 1))
end_date = col2.date_input("Data final:", datetime.date.today())

if start_date >= end_date:
    st.sidebar.error("A data final deve ser posterior à data inicial!")
    st.stop()

# Carregar dados
data = load_ticker_data(selected_tickers, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

if data is not None and not data.empty:
    # Abas para diferentes análises
    tab1, tab2, tab3 = st.tabs(["📈 Evolução de Preços", "📊 Estatísticas", "🔄 Comparações"])
    
    with tab1:
        st.subheader("Evolução dos Preços de Fechamento")
        
        view_option = st.radio(
            "Visualização:",
            options=["Preços Absolutos", "Preços Normalizados (Base 100)", "Retorno Acumulado (%)"],
            horizontal=True
        )
        
        if view_option == "Preços Absolutos":
            plot_price_evolution(data, normalize=False)
        elif view_option == "Preços Normalizados (Base 100)":
            plot_price_evolution(data, normalize=True)
        else:
            plot_performance_chart(data)
            
        # Exibir dados brutos se solicitado
        with st.expander("Ver dados brutos"):
            st.dataframe(data)
    
    with tab2:
        st.subheader("Estatísticas das Ações")
        
        stats = calculate_statistics(data)
        if stats is not None:
            st.dataframe(stats, use_container_width=True)
            
        st.subheader("Matriz de Correlação")
        plot_returns_heatmap(data)
    
    with tab3:
        st.subheader("Análise Comparativa")
        
        period_options = {
            "1 mês": 30,
            "3 meses": 90,
            "6 meses": 180,
            "1 ano": 365,
            "5 anos": 1825,
            "Desde o início": None
        }
        
        period = st.selectbox("Período de comparação:", options=list(period_options.keys()))
        
        if period != "Desde o início":
            days = period_options[period]
            compare_data = data.iloc[-min(days, len(data)):]
        else:
            compare_data = data
            
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Retorno no período")
            returns = ((compare_data.iloc[-1] / compare_data.iloc[0]) - 1) * 100
            returns = returns.sort_values(ascending=False)
            
            st.bar_chart(returns)
        
        with col2:
            st.subheader("Volatilidade no período")
            volatility = compare_data.pct_change().std() * 100
            volatility = volatility.sort_values(ascending=False)
            
            st.bar_chart(volatility)

else:
    if selected_tickers:
        st.warning("Nenhum dado disponível para as ações e período selecionados.")
    else:
        st.info("Selecione pelo menos uma ação para começar a análise.")

# Rodapé
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido usando Streamlit")
st.sidebar.markdown("Dados fornecidos por Yahoo Finance")