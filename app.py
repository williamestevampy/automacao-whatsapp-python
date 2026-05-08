import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Newpen Smart Dashboard",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. DESIGN CUSTOMIZADO (CSS) - Versão "Visibilidade Total"
st.markdown("""
    <style>
    /* Fundo Geral */
    .main { background-color: #f0f2f6; }
    
    /* Cartões de Métrica */
    [data-testid="stMetric"] {
        background: white !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    
    /* Cores das Métricas Principal */
    [data-testid="stMetricValue"] > div { color: #1a202c !important; }
    [data-testid="stMetricLabel"] > div { color: #4a5568 !important; }

    /* Barra Lateral Branca */
    [data-testid="stSidebar"] { background-color: #ffffff !important; }
    
    /* Títulos da Barra Lateral */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #2d3748 !important;
    }

    /* 🔥 CORREÇÃO DEFINITIVA DO BOTÃO ATUALIZAR 🔥 */
    /* Alvo: O botão dentro da div de classe stButton na sidebar */
    .stSidebar .stButton > button {
        background-color: #0056b3 !important; /* Azul Forte */
        color: #ffffff !important;           /* Branco Puro */
        width: 100% !important;
        height: 3em !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
        font-size: 18px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }

    /* Forçar a cor do texto do parágrafo dentro do botão */
    .stSidebar .stButton > button p {
        color: #ffffff !important;
        font-weight: bold !important;
    }

    /* Efeito ao passar o mouse */
    .stSidebar .stButton > button:hover {
        background-color: #004494 !important;
        border: 1px solid #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. FUNÇÕES DE DADOS
def carregar_dados():
    try:
        conn = sqlite3.connect('banco_newpen.db')
        df = pd.read_sql("SELECT * FROM clientes", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/000000/stationery.png")
    st.title("Configurações")
    st.markdown("---")
    
    # Mensagem de ajuda mais nítida
    st.success("ℹ️ O Dashboard atualiza conforme o robô trabalha.")
    
    if st.button("🔄 Atualizar Dados"):
        st.rerun()

# --- CONTEÚDO PRINCIPAL ---
df = carregar_dados()

if not df.empty:
    st.title("📊 Newpen | Inteligência Comercial")
    st.caption("Campanha: Onda 2 - Lançamentos 2026")
    
    # Cálculos
    total_base = len(df)
    envios = len(df[df['status_onda2'] == 'Sucesso']) if 'status_onda2' in df.columns else 0
    interessados = len(df[df['retorno'].astype(str).str.lower().str.strip() == 'sim'])
    taxa = (interessados / envios * 100) if envios > 0 else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Clientes na Base", total_base)
    m2.metric("Impactados", envios)
    m3.metric("Interessados (Sim)", interessados)
    m4.metric("Taxa de Conversão", f"{taxa:.1f}%")

    st.markdown("---")

    c1, c2 = st.columns([1.5, 1])

    with c1:
        st.subheader("🎯 Funil de Conversão")
        fig_data = pd.DataFrame({
            'Etapa': ['Base', 'Enviados', 'Interesse'],
            'Quantidade': [total_base, envios, interessados]
        })
        fig = px.bar(fig_data, x='Etapa', y='Quantidade', color='Etapa',
                     color_discrete_map={'Base': '#cbd5e0', 'Enviados': '#4299e1', 'Interesse': '#48bb78'},
                     text_auto=True)
        fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("🔥 Leads Quentes")
        lista_quente = df[df['retorno'].astype(str).str.lower().str.strip() == 'sim']
        if not lista_quente.empty:
            st.dataframe(lista_quente[['nome', 'telefone']], hide_index=True, use_container_width=True)
        else:
            st.info("Nenhum retorno ainda.")
else:
    st.error("Banco de dados não encontrado.")