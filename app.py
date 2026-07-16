import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Wallison Lucas | Intelligence & Finance",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO PARA DESIGN PREMIUM ---
st.markdown(
    """
    <style>
        /* Suavização de fontes globais e fundos */
        html, body, [data-testid="stSidebar"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Estilização dos blocos de métricas (Cards) */
        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
            font-weight: 700 !important;
            color: #a3e635 !important;
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 12px !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #9ca3af !important;
        }
        
        div[data-testid="metric-container"] {
            background-color: #1f2937;
            border: 1px solid #374151;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        /* Deixar os inputs da barra lateral mais elegantes */
        div[data-testid="stSidebar"] .stNumberInput input {
            background-color: #111827 !important;
            border: 1px solid #374151 !important;
            color: #f3f4f6 !important;
            border-radius: 8px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- LOGO PERSONALIZADA NA BARRA LATERAL ---
st.sidebar.markdown(
    """
    <div style="text-align: center; margin-bottom: 25px; padding: 20px 15px; border-radius: 12px; background-color: #1f2937; border: 1px solid #374151; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
        <span style="font-size: 21px; font-weight: 800; letter-spacing: 3px; color: #ffffff; text-transform: uppercase;">
            Wallison <span style="color: #a3e635;">Lucas</span>
        </span>
        <br>
        <span style="font-size: 9px; font-weight: 500; letter-spacing: 4px; color: #9ca3af; text-transform: uppercase;">
            Intelligence & Finance
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# --- BARRA LATERAL DE ENTRADAS ---
st.sidebar.markdown("### ⚙️ Parâmetros do Modelo")

valor_investimento = st.sidebar.number_input(
    "Valor do Investimento (R$)", 
    min_value=1000.0, 
    value=1000000.0, 
    step=50000.0,
    format="%.2f"
)

taxa_compromissada_pct = st.sidebar.number_input(
    "Taxa Compromissada (% do CDI)", 
    min_value=1.0, 
    max_value=200.0, 
    value=77.0, 
    step=1.0
)

taxa_cdb_pct = st.sidebar.number_input(
    "Taxa CDB (% do CDI)", 
    min_value=1.0, 
    max_value=200.0, 
    value=100.0, 
    step=1.0
)

selic_atual = st.sidebar.number_input(
    "Taxa Selic Atual (% a.a.)", 
    min_value=1.0, 
    max_value=30.0, 
    value=14.10, 
    step=0.25
)

# Cálculos do CDI
cdi_anual = (selic_atual - 0.1) / 100
cdi_diario = (1 + cdi_anual) ** (1/252) - 1

# --- CONTEÚDO PRINCIPAL ---

# Cabeçalho refinado
st.markdown(
    """
    <div style="margin-bottom: 35px;">
        <h1 style="font-weight: 800; font-size: 32px; margin-bottom: 5px;">📊 Simulador de Ativos de Curto Prazo</h1>
        <p style="color: #9ca3af; font-size: 16px; margin-top: 0;">Análise comparativa de rentabilidade líquida diária: Compromissada vs. CDB Tradicional.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Seção de Cards (Métricas Rápidas)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Investimento Inicial", f"R$ {valor_investimento:,.2f}")
with col2:
    st.metric("Compromissada", f"{taxa_compromissada_pct:.1f}% do CDI")
with col3:
    st.metric("CDB Alvo", f"{taxa_cdb_pct:.1f}% do CDI")
with col4:
    st.metric("Taxa CDI Anual", f"{cdi_anual*100:.2f}% a.a.")

st.markdown("<br>", unsafe_allow_html=True)

# --- TABELAS AUXILIARES (Tributação e Dias Úteis) ---
dias_uteis_map = {
    1:1, 2:2, 3:3, 4:4, 5:5, 6:5, 7:5, 8:6, 9:7, 10:8,
    11:9, 12:10, 13:10, 14:10, 15:11, 16:12, 17:13, 18:14, 19:15, 20:15,
    21:15, 22:16, 23:17, 24:18, 25:19, 26:20, 27:20, 28:20, 29:21, 30:22
}

iof_map = {
    1: 0.96, 2: 0.93, 3: 0.90, 4: 0.86, 5: 0.83, 6: 0.80, 7: 0.76, 8: 0.73, 9: 0.70, 10: 0.66,
    11: 0.63, 12: 0.60, 13: 0.56, 14: 0.53, 15: 0.50, 16: 0.46, 17: 0.43, 18: 0.40, 19: 0.36, 20: 0.33,
    21: 0.30, 22: 0.26, 23: 0.23, 24: 0.20, 25: 0.16, 26: 0.13, 27: 0.10, 28: 0.06, 29: 0.03, 30: 0.00
}

ir_aliquota = 0.225

# --- PROCESSAMENTO ---
dados_simulacao = []
taxa_cdb_ano = cdi_anual * (taxa_cdb_pct / 100)
taxa_oc_ano = cdi_anual * (taxa_compromissada_pct / 100)

cdb_diario_efetivo = (1 + taxa_cdb_ano) ** (1/252) - 1
oc_diario_efetivo = (1 + taxa_oc_ano) ** (1/252) - 1

for corr in range(1, 31):
    uteis = dias_uteis_map[corr]
    iof_pct = iof_map[corr]
    
    cdb_bruto = valor_investimento * ((1 + cdb_diario_efetivo) ** uteis - 1)
    cdb_iof = cdb_bruto * iof_pct
    cdb_liquido = (cdb_bruto - cdb_iof) * (1 - ir_aliquota)
    
    oc_bruto = valor_investimento * ((1 + oc_diario_efetivo) ** uteis - 1)
    oc_liquido = oc_bruto * (1 - ir_aliquota)
    
    beneficio = oc_liquido - cdb_liquido
    fator_imposto = (1 - iof_pct) * (1 - ir_aliquota)
    
    if fator_imposto > 0:
        cdb_bruto_necessario = oc_liquido / fator_imposto
        taxa_diaria_necessaria = (cdb_bruto_necessario / valor_investimento + 1) ** (1 / uteis) - 1
        taxa_anual_necessaria = (1 + taxa_diaria_necessaria) ** 252 - 1
        equivalencia_cdb = (taxa_anual_necessaria / cdi_anual) * 100
    else:
        equivalencia_cdb = np.nan
        
    dados_simulacao.append({
        "Dias Corridos": corr,
        "Dias Úteis": uteis,
        "IOF": f"{iof_pct * 100:.0f}%",
        "IR": f"{ir_aliquota * 100:.1f}%",
        "Líquido CDB": cdb_liquido,
        "Líquido OC": oc_liquido,
        "Benefício (OC - CDB)": beneficio,
        "CDB Equiv. (% do CDI)": equivalencia_cdb
    })

df = pd.DataFrame(dados_simulacao)

# --- CONFIGURAÇÃO VISUAL DA TABELA ---
df_formatado = df.copy()
df_formatado["Líquido CDB"] = df_formatado["Líquido CDB"].map("R$ {:,.2f}".format)
df_formatado["Líquido OC"] = df_formatado["Líquido OC"].map("R$ {:,.2f}".format)
df_formatado["Benefício (OC - CDB)"] = df_formatado["Benefício (OC - CDB)"].map("R$ {:,.2f}".format)
df_formatado["CDB Equiv. (% do CDI)"] = df_formatado["CDB Equiv. (% do CDI)"].map("{:,.2f}%".format)

# Estilização de Alto Padrão para a coluna de Benefício
def style_beneficio(val):
    val_limpo = float(val.replace("R$ ", "").replace(".", "").replace(",", "."))
    if val_limpo >= 0:
        return "background-color: #064e3b; color: #34d399; font-weight: bold; border-left: 4px solid #34d399;"
    else:
        return "background-color: #7f1d1d; color: #f87171; font-weight: bold; border-left: 4px solid #f87171;"

# Renderização
st.markdown("### 📊 Tabela de Evolução Temporal")
st.dataframe(
    df_formatado.style.map(style_beneficio, subset=["Benefício (OC - CDB)"]),
    height=800,
    use_container_width=True
)

# Rodapé profissional
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #6b7280; font-size: 12px; margin-top: 20px;">
        Desenvolvido por 💻 <strong>Wallison Lucas Intelligence & Finance</strong> | Todos os cálculos consideram d.u. base 252 e IOF/IR regressivos.
    </div>
    """,
    unsafe_allow_html=True
)
