import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Simulador: Compromissada vs CDB",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Simulador Financeiro: Operação Compromissada vs CDB")
st.markdown("Compare o rendimento líquido diário de ambos os ativos considerando IOF e IR regressivos.")

# --- BARRA LATERAL DE ENTRADAS ---
st.sidebar.header("Configurações do Investimento")

# Inputs principais
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
    value=14.75, 
    step=0.25
)

# Cálculo automático do CDI diário/anual
# Regra fornecida: CDI = Selic - 0.1%
cdi_anual = (selic_atual - 0.1) / 100
cdi_diario = (1 + cdi_anual) ** (1/252) - 1

# Exibição dos parâmetros calculados
st.sidebar.markdown("---")
st.sidebar.write(f"**CDI Anual Considerado:** {cdi_anual*100:.2f}%")

# --- TABELAS AUXILIARES (Tributação e Dias Úteis) ---
# Mapeamento exato de Dias Corridos para Dias Úteis baseado no print do Excel
dias_uteis_map = {
    1:1, 2:2, 3:3, 4:4, 5:5, 6:5, 7:5, 8:6, 9:7, 10:8,
    11:9, 12:10, 13:10, 14:10, 15:11, 16:12, 17:13, 18:14, 19:15, 20:15,
    21:15, 22:16, 23:17, 24:18, 25:19, 26:20, 27:20, 28:20, 29:21, 30:22
}

# Tabela regressiva de IOF para os 30 dias
iof_map = {
    1: 0.96, 2: 0.93, 3: 0.90, 4: 0.86, 5: 0.83, 6: 0.80, 7: 0.76, 8: 0.73, 9: 0.70, 10: 0.66,
    11: 0.63, 12: 0.60, 13: 0.56, 14: 0.53, 15: 0.50, 16: 0.46, 17: 0.43, 18: 0.40, 19: 0.36, 20: 0.33,
    21: 0.30, 22: 0.26, 23: 0.23, 24: 0.20, 25: 0.16, 26: 0.13, 27: 0.10, 28: 0.06, 29: 0.03, 30: 0.00
}

ir_aliquota = 0.225 # 22.5% para prazos abaixo de 180 dias

# --- PROCESSAMENTO DOS DADOS ---
dados_simulacao = []

# Taxas efetivas dos ativos ao ano
taxa_cdb_ano = cdi_anual * (taxa_cdb_pct / 100)
taxa_oc_ano = cdi_anual * (taxa_compromissada_pct / 100)

# Taxas efetivas diárias (252 d.u.)
cdb_diario_efetivo = (1 + taxa_cdb_ano) ** (1/252) - 1
oc_diario_efetivo = (1 + taxa_oc_ano) ** (1/252) - 1

for corr in range(1, 31):
    uteis = dias_uteis_map[corr]
    iof_pct = iof_map[corr]
    
    # 1. CDB Cálculo
    cdb_bruto = valor_investimento * ((1 + cdb_diario_efetivo) ** uteis - 1)
    cdb_iof = cdb_bruto * iof_pct
    cdb_liquido = (cdb_bruto - cdb_iof) * (1 - ir_aliquota)
    
    # 2. Compromissada (OC) Cálculo (Isenta de IOF no modelo)
    oc_bruto = valor_investimento * ((1 + oc_diario_efetivo) ** uteis - 1)
    oc_liquido = oc_bruto * (1 - ir_aliquota)
    
    # 3. Benefício (Diferença)
    beneficio = oc_liquido - cdb_liquido
    
    # 4. Equivalência de CDB (% do CDI)
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
        "IOF (%)": f"{iof_pct * 100:.0f}%",
        "IR (%)": f"{ir_aliquota * 100:.1f}%",
        "Rentabilidade Líquida - CDB": cdb_liquido,
        "Rentabilidade Líquida - OC": oc_liquido,
        "Benefício (OC - CDB)": beneficio,
        "Performance (CDB Equiv. % CDI)": equivalencia_cdb
    })

df = pd.DataFrame(dados_simulacao)

# --- APRESENTAÇÃO DOS RESULTADOS ---
st.subheader("Tabela Comparativa de Rendimentos (Prazo de 1 a 30 dias)")

# Formatação visual das colunas de dinheiro e porcentagem para exibição
df_formatado = df.copy()
df_formatado["Rentabilidade Líquida - CDB"] = df_formatado["Rentabilidade Líquida - CDB"].map("R$ {:,.2f}".format)
df_formatado["Rentabilidade Líquida - OC"] = df_formatado["Rentabilidade Líquida - OC"].map("R$ {:,.2f}".format)
df_formatado["Benefício (OC - CDB)"] = df_formatado["Benefício (OC - CDB)"].map("R$ {:,.2f}".format)
df_formatado["Performance (CDB Equiv. % CDI)"] = df_formatado["Performance (CDB Equiv. % CDI)"].map("{:,.2f}%".format)

# Estilização Soft / Pastel para Tema Escuro
# Usando cores menos saturadas para não cansar as vistas
def destacar_beneficio_dark(val):
    val_limpo = float(val.replace("R$ ", "").replace(".", "").replace(",", "."))
    # Verde pastel suave e Vermelho/Laranja pastel suave que funcionam muito bem no tema escuro
    if val_limpo >= 0:
        color = "background-color: #1a3322; color: #a3e635;"  # Fundo verde escuro sutil com texto verde-limão claro
    else:
        color = "background-color: #3b1e1e; color: #f87171;"  # Fundo vermelho escuro sutil com texto vermelho claro
    return color

# Exibindo a tabela formatada no Streamlit
st.dataframe(
    df_formatado.style.map(destacar_beneficio_dark, subset=["Benefício (OC - CDB)"]),
    height=1000,
    use_container_width=True
)

st.info("💡 **Nota:** A coluna 'Benefício' destaca em verde quando a Compromissada rende mais que o CDB.")
