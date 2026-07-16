import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Configuração da página do Streamlit (com ícone financeiro na aba do navegador)
st.set_page_config(
    page_title="RENDA FIXA | Intelligence & Finance",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS CUSTOMIZADO DE ALTA TECNOLOGIA (DESIGN SAAS PREMIUM) ---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700;800&family=JetBrains+Mono:wght=400;700&display=swap');

        /* Reset e Fontes */
        html, body, [data-testid="stSidebar"], .stApp {
            font-family: 'Inter', -apple-system, sans-serif !important;
            background-color: #0b0f19 !important;
            color: #f3f4f6 !important;
        }

        /* Esconder cabeçalho padrão do Streamlit para parecer um app nativo */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Sidebar Customizada */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #1e293b !important;
            padding-top: 10px;
        }

        /* Estilização dos Inputs na Sidebar */
        div[data-testid="stSidebar"] .stNumberInput input {
            background-color: #020617 !important;
            border: 1px solid #334155 !important;
            color: #f8fafc !important;
            border-radius: 10px !important;
            font-size: 14px !important;
            padding: 10px !important;
            transition: all 0.3s ease;
        }
        
        div[data-testid="stSidebar"] .stNumberInput input:focus {
            border-color: #10b981 !important;
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important;
        }

        /* Cards de Métricas Premium com Fundo Branco Texturizado e Bordas Ativas */
        .premium-card {
            background-color: #ffffff !important;
            /* Textura moderna sutil de grade pontilhada */
            background-image: radial-gradient(#e2e8f0 1.5px, transparent 1.5px) !important;
            background-size: 12px 12px !important;
            
            border: 1px solid #cbd5e1 !important;
            border-radius: 16px;
            padding: 24px 20px;
            text-align: center; /* Centraliza todo o texto do card */
            
            /* Sombra suave e elegante para efeito de profundidade */
            box-shadow: 0 10px 20px -3px rgba(0, 0, 0, 0.2), 0 4px 8px -4px rgba(0, 0, 0, 0.15);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        /* Efeito Hover moderno nos cards (Brilho ativo com borda de destaque) */
        .premium-card:hover {
            transform: translateY(-4px);
            border-color: #10b981 !important;
            box-shadow: 0 20px 25px -5px rgba(16, 185, 129, 0.15), 0 10px 10px -5px rgba(16, 185, 129, 0.1);
        }

        .premium-label {
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: #64748b !important; /* Cinza de boa legibilidade sobre fundo branco */
            margin-bottom: 10px;
            text-align: center;
        }

        .premium-value {
            font-size: 24px;
            font-weight: 800;
            color: #0f172a !important; /* Azul escuro quase preto de altíssimo contraste */
            font-family: 'JetBrains Mono', monospace;
            text-align: center;
        }

        .premium-highlight {
            color: #059669 !important; /* Verde focado na legibilidade */
        }

        /* Customização da Tabela de Dados */
        .stDataFrame div {
            border-radius: 12px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- LOGO PERSONALIZADA NA BARRA LATERAL ---
st.sidebar.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px; padding: 25px 15px; border-radius: 16px; background: linear-gradient(185deg, #1e293b 0%, #090d16 100%); border: 1px solid #334155; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);">
        <span style="font-size: 20px; font-weight: 900; letter-spacing: 4px; color: #ffffff; text-shadow: 0 0 12px rgba(16, 185, 129, 0.3);">
            RENDA <span style="color: #10b981;">FIXA</span>
        </span>
        <br>
        <span style="font-size: 9px; font-weight: 600; letter-spacing: 5px; color: #64748b; text-transform: uppercase; margin-top: 5px; display: inline-block;">
            INTELLIGENCE & FINANCE
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# --- BARRA LATERAL DE ENTRADAS ---
st.sidebar.markdown("<p style='font-size: 12px; font-weight: 700; color: #10b981; text-transform: uppercase; letter-spacing: 1px;'>⚙️ Painel de Controle</p>", unsafe_allow_html=True)

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

# Cálculos internos do CDI
cdi_anual = (selic_atual - 0.1) / 100
cdi_diario = (1 + cdi_anual) ** (1/252) - 1

# --- CONTEÚDO PRINCIPAL ---

# Header refinado com Badge tecnológico e Ícone de Alta Financeira SVG integrado ao título com brilho neon
st.markdown(
    """
    <div style="margin-bottom: 35px; border-bottom: 1px solid #1e293b; padding-bottom: 20px;">
        <span style="background-color: rgba(16, 185, 129, 0.1); color: #10b981; font-size: 10px; font-weight: 700; padding: 5px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 1.5px; border: 1px solid rgba(16, 185, 129, 0.2);">
            SaaS Terminal v2.3
        </span>
        <h1 style="font-weight: 800; font-size: 36px; margin-top: 15px; margin-bottom: 5px; letter-spacing: -0.5px; color: #ffffff; display: flex; align-items: center; gap: 12px;">
            <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.5));">
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
                <polyline points="17 6 23 6 23 12"></polyline>
            </svg>
            Simulador Quantitativo de Ativos
        </h1>
        <p style="color: #64748b; font-size: 15px; margin-top: 5px;">
            Algoritmo de cálculo de curva de juros diária com compensação regressiva de IOF e IR (Compromissadas vs. CDBs).
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Grid de Layout usando Columns para hospedar os Cards de Métricas Premium (Fundo Branco com Textura)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="premium-label">Investimento Alocado</div>
            <div class="premium-value">R$ {valor_investimento:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="premium-label">Taxa Compromissada</div>
            <div class="premium-value premium-highlight">{taxa_compromissada_pct:.1f}% <span style="font-size: 14px; color: #64748b;">CDI</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="premium-label">Taxa CDB Alvo</div>
            <div class="premium-value" style="color: #2563eb !important;">{taxa_cdb_pct:.1f}% <span style="font-size: 14px; color: #64748b;">CDI</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="premium-card">
            <div class="premium-label">Taxa CDI de Referência</div>
            <div class="premium-value" style="font-size: 21px;">{cdi_anual*100:.2f}% <span style="font-size: 14px; color: #64748b;">a.a.</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

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

# --- PROCESSAMENTO DOS DADOS ---
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

# --- GRÁFICO DE EVOLUÇÃO (PLOTLY PREMIUM) ---
st.markdown("<p style='font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 5px;'>📈 Curva de Evolução Patrimonial Líquida</p>", unsafe_allow_html=True)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Dias Corridos"],
    y=df["Líquido OC"],
    mode='lines+markers',
    name='Operação Compromissada (Líquida)',
    line=dict(color='#10b981', width=3),
    marker=dict(size=6),
    hovertext=df["Líquido OC"].map("R$ {:,.2f}".format),
    hovertemplate="<b>Dia %{x}</b><br>Compromissada: %{hovertext}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=df["Dias Corridos"],
    y=df["Líquido CDB"],
    mode='lines+markers',
    name='CDB Alvo (Líquido)',
    line=dict(color='#60a5fa', width=3),
    marker=dict(size=6),
    hovertext=df["Líquido CDB"].map("R$ {:,.2f}".format),
    hovertemplate="<b>Dia %{x}</b><br>CDB Alvo: %{hovertext}<extra></extra>"
))

fig.update_layout(
    paper_bgcolor='#0b0f19',
    plot_bgcolor='#0f172a',
    margin=dict(l=40, r=40, t=10, b=40),
    height=380,
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(color="#94a3b8", size=11)
    ),
    xaxis=dict(
        title="Dias Corridos",
        title_font=dict(color="#64748b", size=12),
        tickfont=dict(color="#94a3b8"),
        gridcolor="#1e293b",
        zeroline=False
    ),
    yaxis=dict(
        title="Rendimento Líquido (R$)",
        title_font=dict(color="#64748b", size=12),
        tickfont=dict(color="#94a3b8"),
        gridcolor="#1e293b",
        zeroline=False,
        tickformat="$,.2f"
    )
)

st.plotly_chart(fig, use_container_width=True)

# --- FORMATANDO OS DADOS PARA EXIBIÇÃO NA TABELA ---
df_formatado = df.copy()
df_formatado["Líquido CDB"] = df_formatado["Líquido CDB"].map("R$ {:,.2f}".format)
df_formatado["Líquido OC"] = df_formatado["Líquido OC"].map("R$ {:,.2f}".format)
df_formatado["Benefício (OC - CDB)"] = df_formatado["Benefício (OC - CDB)"].map("R$ {:,.2f}".format)
df_formatado["CDB Equiv. (% do CDI)"] = df_formatado["CDB Equiv. (% do CDI)"].map("{:,.2f}%".format)

# Estilização das Células da Tabela com FONTES ESCURAS e alto contraste de leitura
def style_beneficio(val):
    val_limpo = float(val.replace("R$ ", "").replace(".", "").replace(",", "."))
    if val_limpo >= 0:
        # Fundo verde claro pastel, fonte verde escuro (Negrito)
        return "background-color: #d1fae5; color: #065f46; font-weight: bold; font-family: 'JetBrains Mono', monospace;"
    else:
        # Fundo vermelho claro pastel, fonte vermelha escura (Negrito)
        return "background-color: #fee2e2; color: #991b1b; font-weight: bold; font-family: 'JetBrains Mono', monospace;"

# Renderização do Bloco de Tabela
st.markdown("<p style='font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 15px;'>📊 Matriz de Evolução Diária</p>", unsafe_allow_html=True)

st.dataframe(
    df_formatado.style.map(style_beneficio, subset=["Benefício (OC - CDB)"]),
    height=600,
    use_container_width=True
)

# Rodapé profissional
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #475569; font-size: 11px; margin-top: 25px; font-weight: 500;">
        SISTEMA DE ANÁLISE QUANTITATIVA • DESENVOLVIDO POR <strong>ESTER SOUSA INTELLIGENCE & FINANCE</strong><br>
        Curva de juros calibrada com base 252 d.u./ano. Os valores informados são simulações brutas deduzidas de encargos legais (IOF/IR) vigentes.
    </div>
    """,
    unsafe_allow_html=True
)
