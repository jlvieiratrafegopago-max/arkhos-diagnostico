import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime
import time

# --- 1. CONFIGURAÇÕES DE PÁGINA E ESTILO CLEAN PREMIUM ---
st.set_page_config(
    page_title="Arkhos Intelligence | Diagnóstico Estratégico",
    page_icon="💎",
    layout="wide"
)

# CSS PARA CENTRALIZAÇÃO E AJUSTE DE FONTE
st.markdown("""
    <style>
    /* 1. Fundo Geral e Fonte */
    .stApp {
        background-color: #FFFFFF;
        color: #1E1E1E;
    }
    
    /* 2. CENTRALIZAÇÃO E TAMANHO DO CABEÇALHO */
    .main-header {
        text-align: center;
        padding-top: 20px;
        padding-bottom: 20px;
    }
    .main-header h1 {
        font-size: 2.2rem !important; /* Tamanho reduzido para elegância */
        font-weight: 800 !important;
        color: #1E1E1E !important;
        margin-bottom: 5px !important;
    }
    .main-header p {
        font-size: 1.1rem !important;
        color: #6C757D !important;
    }

    /* 3. TEXTOS ACIMA DAS CAIXAS (LABELS) */
    label, [data-testid="stWidgetLabel"] p {
        color: #1E1E1E !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }

    /* 4. Abas Estilo Pílula Centralizadas */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        justify-content: center; /* Centraliza as abas */
        background-color: #F8F9FA;
        border-radius: 12px;
        padding: 5px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #6C757D !important;
        font-weight: 600;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #00D26A !important;
        border-radius: 8px !important;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    }

    /* 5. Inputs e Áreas de Digitação */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select {
        border-radius: 8px !important;
        border: 1px solid #E9ECEF !important;
    }

    /* 6. Botão Arkhos */
    div.stButton > button:first-child {
        background: #1E1E1E;
        color: white !important;
        border-radius: 8px;
        width: 100%;
        height: 3.5em;
        font-weight: 700;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background: #00D26A;
        transform: translateY(-1px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FUNÇÕES DO BANCO DE DADOS ---
def init_db():
    conn = sqlite3.connect('arkhos_leads.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS diagnosticos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_envio TEXT, empresa TEXT, setor TEXT, time_size INTEGER,
            faturamento REAL, meta REAL, stack TEXT, processos TEXT,
            objetivo TEXT, investimento TEXT, dor_principal TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_dados(dados):
    conn = sqlite3.connect('arkhos_leads.db')
    c = conn.cursor()
    c.execute('INSERT INTO diagnosticos (data_envio, empresa, setor, time_size, faturamento, meta, stack, processos, objetivo, investimento, dor_principal) VALUES (?,?,?,?,?,?,?,?,?,?,?)', dados)
    conn.commit()
    conn.close()

init_db()

# --- 3. INTERFACE DO USUÁRIO (CENTRALIZADA) ---
st.markdown("""
    <div class="main-header">
        <h1>💎 Arkhos | Diagnóstico Estratégico</h1>
        <p>Mapeamento de viabilidade e inteligência de negócios para operações de alto padrão.</p>
    </div>
    """, unsafe_allow_html=True)

tab_identidade, tab_perf, tab_eco, tab_escala = st.tabs([
    "🏢 Identidade", "📈 Performance", "⚙️ Ecossistema", "🚀 Escalabilidade"
])

with tab_identidade:
    col1, col2 = st.columns(2)
    with col1:
        empresa = st.text_input("Nome da Organização", placeholder="Ex: Grupo Hospitalar Prime")
        setor = st.selectbox("Segmento de Mercado", ["Varejo de Luxo", "Saúde Premium", "Direito Corporativo", "Tecnologia & Software", "Indústria 4.0", "Outros"])
    with col2:
        time_size = st.number_input("Tamanho do Time (Colaboradores)", min_value=1, step=1)
        canal_origem = st.multiselect("Como conheceu a Arkhos?", ["LinkedIn", "Indicação Direta", "Busca Orgânica", "Mídia Paga"])

with tab_perf:
    col_a, col_b = st.columns(2)
    with col_a:
        faturamento = st.number_input("Faturamento Mensal Atual (R$)", min_value=0.0, format="%.2f")
    with col_b:
        meta = st.number_input("Meta de Faturamento (Próximos 12 meses) (R$)", min_value=0.0, format="%.2f")
    
    if faturamento > 0 and meta > 0:
        gap_anual = (meta - faturamento) * 12
        st.info(f"💡 Potencial de Expansão Anual: **R$ {gap_anual:,.2f}**")

with tab_eco:
    stack = st.text_area("Infraestrutura Tecnológica (Sistemas, CRMs, Automações)")
    processos = st.select_slider(
        "Nível de dependência de processos manuais:",
        options=["Otimizado", "Moderado", "Alto", "Crítico"]
    )

with tab_escala:
    objetivo = st.radio(
        "Prioridade Estratégica Imediata:", 
        ["Qualidade e Aquisição de Leads", "Automação de Processos Internos", "Aumento da Margem de Ticket Alto", "Retenção de Clientes (LTV)"]
    )
    investimento = st.select_slider(
        "Orçamento planejado para Consultoria/Tecnologia:",
        options=["R$ 10k-25k", "R$ 25k-50k", "R$ 50k-100k", "Acima de R$ 100k"]
    )
    dor_principal = st.text_area("Ponto de Inflexão (O que trava seu crescimento hoje?)")

    if st.button("SOLICITAR PARECER ESTRATÉGICO"):
        if empresa and faturamento > 0 and dor_principal:
            data_envio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            dados_lead = (data_envio, empresa, setor, int(time_size), float(faturamento), float(meta), stack, processos, objetivo, investimento, dor_principal)
            salvar_dados(dados_lead)

            with st.status("Processando Inteligência...", expanded=False) as status:
                time.sleep(1.2)
                status.update(label="Análise Concluída!", state="complete")

            st.success(f"Dados enviados com sucesso, {empresa}!")
            st.balloons()
            
            # --- DASHBOARD ---
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                gap_m = meta - faturamento if meta > faturamento else 0
                df = pd.DataFrame({"Cat": ["Atual", "Meta"], "Val": [faturamento, gap_m]})
                fig = px.bar(df, x="Cat", y="Val", text_auto='.2s', title="Cenário de Expansão",
                             color="Cat", color_discrete_map={"Atual": "#CED4DA", "Meta": "#00D26A"})
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

            with c2:
                r_map = {"Otimizado": 10, "Moderado": 40, "Alto": 70, "Crítico": 95}
                score = r_map.get(processos, 50)
                fig_p = px.pie(values=[score, 100-score], names=["Risco Manual", "Eficiência"],
                                hole=0.7, title="Risco Operacional",
                                color_discrete_sequence=["#FF4B4B", "#E9ECEF"])
                fig_p.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_p, use_container_width=True)

            st.markdown(f"### 🩺 Parecer: A **Equipe Arkhos** entrará em contato em breve.")
        else:
            st.error("Por favor, preencha os campos obrigatórios.")

# --- 4. ÁREA ADMINISTRATIVA (BARRA LATERAL) ---
with st.sidebar:
    st.title("🛡️ Painel Admin")
    if st.checkbox("Acessar Base de Leads"):
        chave = st.text_input("Chave", type="password")
        if chave == "arkhos2026":
            conn = sqlite3.connect('arkhos_leads.db')
            df_adm = pd.read_sql_query("SELECT * FROM diagnosticos ORDER BY id DESC", conn)
            st.dataframe(df_adm)
            csv = df_adm.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Exportar CSV", csv, "leads_arkhos.csv", "text/csv")
            conn.close()