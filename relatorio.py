import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard OCR", layout="wide")

# Título
st.title("📊 Análise de Resultados OCR")

# 1. Carregar dados
uploaded_file = st.file_uploader("Carregue seu arquivo CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # 2. Filtros interativos
    st.sidebar.header("Filtros")
    conjuntos = st.sidebar.multiselect(
        "Selecione os conjuntos",
        options=df['Conjunto'].unique(),
        default=df['Conjunto'].unique()
    )
    
    # 3. Aplicar filtros
    df_filtrado = df[df['Conjunto'].isin(conjuntos)]
    
    # 4. Métricas principais
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Testes", len(df_filtrado))
    with col2:
        corretos = sum(df_filtrado['Status'] == 'Correto')
        st.metric("Acertos", f"{corretos} ({corretos/len(df_filtrado):.1%})")
    with col3:
        erros = len(df_filtrado) - corretos
        st.metric("Erros", f"{erros} ({erros/len(df_filtrado):.1%})")
    
    # 5. Visualizações
    tab1, tab2 = st.tabs(["Distribuição", "Comparativo"])
    
    with tab1:
        fig = px.pie(df_filtrado, names='Status', title='Distribuição de Resultados')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig2 = px.bar(df_filtrado.groupby('Conjunto')['Status'].value_counts(normalize=True).unstack()*100,
                     title="Desempenho por Conjunto (%)")
        st.plotly_chart(fig2, use_container_width=True)
    
    # 6. Tabela detalhada
    st.subheader("Dados Completos")
    st.dataframe(df_filtrado)
