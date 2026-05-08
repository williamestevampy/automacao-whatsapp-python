import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestão Newpen - William", layout="wide", page_icon="🎨")

# Custom CSS para deixar o visual mais moderno
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 Dashboard de Vendas Newpen - Onda 2")
st.markdown("Monitorização em tempo real da campanha de lançamentos.")

def carregar_dados():
    conn = sqlite3.connect('banco_newpen.db')
    df = pd.read_sql("SELECT * FROM clientes", conn)
    conn.close()
    return df

try:
    df = carregar_dados()
    
    # --- PROCESSAMENTO DE DADOS ---
    total_base = len(df)
    
    # Filtra quem recebeu a Onda 2 (O robô carimba como 'Sucesso')
    envios_onda2 = len(df[df['status_onda2'] == 'Sucesso']) if 'status_onda2' in df.columns else 0
    
    # Filtra quem respondeu "Sim" (Interesse no catálogo)
    interessados = len(df[df['retorno'].astype(str).str.lower().str.strip() == 'sim'])
    
    taxa_conversao = (interessados / envios_onda2 * 100) if envios_onda2 > 0 else 0

    # --- LINHA 1: MÉTRICAS PRINCIPAIS ---
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total na Base", total_base)
    col2.metric("Mensagens Enviadas", envios_onda2, help="Contatos que o robô já processou na Onda 2")
    col3.metric("Solicitaram Catálogo", interessados, delta=f"{interessados} Clientes", delta_color="normal")
    col4.metric("Taxa de Conversão", f"{taxa_conversao:.1f}%")

    st.markdown("---")

    # --- LINHA 2: GRÁFICOS E TABELAS ---
    col_grafico, col_tabela = st.columns([2, 1])

    with col_grafico:
        st.subheader("📈 Funil de Performance")
        fig, ax = plt.subplots(figsize=(8, 5))
        cores = ['#34495e', '#3498db', '#2ecc71']
        labels = ['Total Base', 'Enviados (Onda 2)', 'Interessados (Sim)']
        valores = [total_base, envios_onda2, interessados]
        
        bars = ax.bar(labels, valores, color=cores)
        ax.bar_label(bars, padding=3, fontweight='bold')
        ax.set_frame_on(False)
        ax.axes.get_yaxis().set_visible(False)
        st.pyplot(fig)

    with col_tabela:
        st.subheader("📋 Lista de Interesse")
        # Mostra apenas quem quer o catálogo para você ligar/chamar
        df_interessados = df[df['retorno'].astype(str).str.lower().str.strip() == 'sim']
        if not df_interessados.empty:
            st.dataframe(df_interessados[['nome', 'telefone']], use_container_width=True, hide_index=True)
        else:
            st.info("A aguardar os primeiros 'Sim' da Onda 2...")

except Exception as e:
    st.error(f"Erro ao carregar Dashboard: {e}")
    st.info("Dica: Certifique-se de que rodou a migração SQL e o robô da Onda 2.")