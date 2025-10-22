import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import locale

# --- Configurações da Página ---
st.set_page_config(
    page_title=" Indicadores Kaptha",
    page_icon="📊",
    layout="wide"
)

# Define o locale para português para nomes de meses
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    st.warning("Locale 'pt_BR.UTF-8' não encontrado. Nomes dos meses podem aparecer em inglês.")

# --- 1. GERAÇÃO DE DADOS HISTÓRICOS (NOVA FUNÇÃO) ---
@st.cache_data # Armazena os dados para não recarregar a cada interação
def gerar_dados_historicos():
    df_historico = pd.DataFrame()
    today = date.today()
    
    for i in range(12, -1, -1): # Gera 13 meses para garantir sempre um anterior
        mes_referencia = today - relativedelta(months=i)
        mes_str = mes_referencia.strftime("%Y-%m")
        nome_mes = mes_referencia.strftime("%B/%Y").capitalize()
        
        mrr_realizado = 100000 + (i * random.randint(-2000, 1000))
        leads = 1000 + (i * random.randint(-50, 20))
        contratos_qtd = 35 + (i * random.randint(-3, 1))
        
        mes_data = {
            "Mês": mes_str,
            "Nome Mês": nome_mes,
            "Data": mes_referencia.replace(day=15),
            "mrr_orcado": 98000, "mrr_realizado": mrr_realizado,
            "fat_orcado": 102000, "fat_realizado": mrr_realizado + random.randint(3000, 8000),
            "clientes_essencial_orcado": 80, "clientes_essencial_realizado": 80 + random.randint(-5, 5),
            "clientes_controle_orcado": 50, "clientes_controle_realizado": 50 + random.randint(-3, 3),
            "clientes_avancado_orcado": 25, "clientes_avancado_realizado": 25 + random.randint(-2, 2),
            "leads": leads,
            "propostas_qtd": int(leads * random.uniform(0.08, 0.12)),
            "propostas_rs": int(leads * random.uniform(0.08, 0.12)) * random.randint(1200, 1800),
            "contratos_qtd": contratos_qtd, "contratos_rs": contratos_qtd * random.randint(2500, 3500), "meta_rs": 115000,
            "oportunidades_qtd": int(leads * random.uniform(0.2, 0.3)), "ars_feitos": random.randint(40, 60),
            "velocidade_implantacao_dias": random.randint(5, 12) + random.uniform(-1, 1),
            "ctr_percent": random.uniform(0.01, 0.05), "cpr_rs": random.uniform(15.0, 25.0), "verba_gerenciada_rs": random.randint(18000, 25000)
        }
        df_historico = pd.concat([df_historico, pd.DataFrame([mes_data])], ignore_index=True)
    
    df_historico['Data'] = pd.to_datetime(df_historico['Data'])
    return df_historico

df_completo = gerar_dados_historicos()

# --- 2. SIDEBAR DE FILTROS ---
st.sidebar.header("Filtros do Dashboard")

# Filtro por Mês (para finanças, comercial e funil)
lista_nomes_meses = df_completo["Nome Mês"].unique().tolist()
meses_selecionados_nomes = st.sidebar.multiselect(
    "Selecione o(s) Mês(es)",
    options=lista_nomes_meses,
    default=[lista_nomes_meses[-1]]
)

# Filtro por Período de Data (APENAS para Operacional)
st.sidebar.markdown("---")
periodo_operacional = st.sidebar.date_input(
    "Selecione o Período Operacional",
    value=(df_completo["Data"].min().date(), df_completo["Data"].max().date()),
    min_value=df_completo["Data"].min().date(),
    max_value=df_completo["Data"].max().date()
)

# --- 3. LÓGICA DE FILTRAGEM DOS DADOS ---
if not meses_selecionados_nomes:
    st.warning("Por favor, selecione pelo menos um mês na barra lateral.")
    st.stop()

# Filtra dados para as primeiras seções
df_filtrado_mes = df_completo[df_completo["Nome Mês"].isin(meses_selecionados_nomes)]
primeiro_mes_selecionado = df_filtrado_mes["Mês"].min()
idx_primeiro_mes = df_completo["Mês"].tolist().index(primeiro_mes_selecionado)
mes_anterior_str = df_completo["Mês"].tolist()[idx_primeiro_mes - 1] if idx_primeiro_mes > 0 else None
df_anterior = df_completo[df_completo["Mês"] == mes_anterior_str] if mes_anterior_str else pd.DataFrame()

# Filtra dados para a seção operacional
if len(periodo_operacional) == 2:
    data_inicio_op, data_fim_op = periodo_operacional
    df_filtrado_op = df_completo[(df_completo["Data"].dt.date >= data_inicio_op) & (df_completo["Data"].dt.date <= data_fim_op)]
    # Define período anterior para comparação
    delta_dias = data_fim_op - data_inicio_op
    data_inicio_op_ant = data_inicio_op - delta_dias - timedelta(days=1)
    df_anterior_op = df_completo[(df_completo["Data"].dt.date >= data_inicio_op_ant) & (df_completo["Data"].dt.date < data_inicio_op)]
else:
    st.sidebar.warning("Por favor, selecione um período de início e fim.")
    st.stop()


# --- INÍCIO DO LAYOUT DO DASHBOARD ---
st.title("Indicadores Kaptha 💹")
st.markdown("---")

# --- Bloco de MRR ---
st.subheader(f"MRR ({', '.join(meses_selecionados_nomes)})")
# ... (código dos blocos adaptado para usar os dataframes filtrados)
mrr_orc, mrr_real, mrr_dif = st.columns(3); orcado_atual = df_filtrado_mes["mrr_orcado"].sum(); realizado_atual = df_filtrado_mes["mrr_realizado"].sum(); orcado_anterior = df_anterior["mrr_orcado"].sum() if not df_anterior.empty else 0; realizado_anterior = df_anterior["mrr_realizado"].sum() if not df_anterior.empty else 0
mrr_orc.metric("Orçado", f"R$ {orcado_atual:,.2f}", f"R$ {orcado_atual - orcado_anterior:,.2f}"); mrr_real.metric("Realizado", f"R$ {realizado_atual:,.2f}", f"R$ {realizado_atual - realizado_anterior:,.2f}"); diferenca_atual = realizado_atual - orcado_atual; diferenca_anterior = realizado_anterior - orcado_anterior; mrr_dif.metric("Diferença (Real vs Orçado)", f"R$ {diferenca_atual:,.2f}", f"R$ {diferenca_atual - diferenca_anterior:,.2f}"); st.markdown("---")

# --- SEÇÃO DE ANÁLISE DE PLANOS ---
st.subheader(f"Análise Comercial ({', '.join(meses_selecionados_nomes)})")
col1, col2, col3, col4 = st.columns(4); planos = ["Essencial", "Controle", "Avancado"]; colunas = [col1, col2, col3]
def exibir_metricas_plano_dinamico(nome_plano, df_atual, df_ant):
    st.markdown(f"##### {nome_plano.capitalize()}"); plano_key = nome_plano.lower(); orcado_atual = df_atual[f"clientes_{plano_key}_orcado"].sum(); realizado_atual = df_atual[f"clientes_{plano_key}_realizado"].sum(); orcado_anterior = df_ant[f"clientes_{plano_key}_orcado"].sum() if not df_ant.empty else 0; realizado_anterior = df_ant[f"clientes_{plano_key}_realizado"].sum() if not df_ant.empty else 0
    st.metric("Orçado", f"{orcado_atual} clientes", f"{orcado_atual - orcado_anterior}"); st.metric("Realizado", f"{realizado_atual} clientes", f"{realizado_atual - realizado_anterior}"); diferenca_atual = realizado_atual - orcado_atual; diferenca_anterior = realizado_anterior - orcado_anterior; st.metric("Diferença", f"{diferenca_atual} clientes", f"{diferenca_atual - diferenca_anterior}")
for i, plano in enumerate(planos):
    with colunas[i]:
        with st.container(border=True): exibir_metricas_plano_dinamico(plano, df_filtrado_mes, df_anterior)
with col4:
    with st.container(border=True):
        precos_planos = {'Essencial': 149, 'Controle': 299, 'Avancado': 499}
        receita_por_plano = {
            plano: df_filtrado_mes[f"clientes_{plano.lower()}_realizado"].sum() * preco 
            for plano, preco in precos_planos.items()
        }
        df_pizza = pd.DataFrame(receita_por_plano.items(), columns=['Plano', 'Receita'])
        fig = px.pie(
            df_pizza, 
            names='Plano', 
            values='Receita', 
            hole=.4,
            color_discrete_sequence=px.colors.sequential.GnBu_r
        )
        fig.update_traces(textposition='inside', textinfo='percent')
        
        # --- AJUSTE APLICADO AQUI ---
        fig.update_layout(
            title_text="Distribuição dos Planos",
            title_x=0.01,
            title_font_size=16,
            showlegend=True,
            legend=dict(
                title_text="",
                orientation="h",
                yanchor="top",
                y=-0.1,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            ),
            # Margens reduzidas para alinhar a altura do container
            margin=dict(l=20, r=20, t=50, b=50) 
        )
        st.plotly_chart(fig, use_container_width=True)
# --- FUNIL DE VENDAS ---
st.subheader(f"Funil de Vendas e Metas ({', '.join(meses_selecionados_nomes)})")
col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container(border=True):
        st.markdown("##### Leads"); leads_atual = df_filtrado_mes['leads'].sum(); leads_anterior = df_anterior['leads'].sum() if not df_anterior.empty else 0; st.metric("Quantidade Total", f"{leads_atual}", f"{leads_atual - leads_anterior}"); contratos_atual = df_filtrado_mes['contratos_qtd'].sum(); contratos_anterior = df_anterior['contratos_qtd'].sum() if not df_anterior.empty else 0; tx_atual = contratos_atual / leads_atual if leads_atual else 0; tx_anterior = contratos_anterior / leads_anterior if leads_anterior else 0; st.metric("Taxa de Conversão", f"{tx_atual:.2%}", f"{tx_atual - tx_anterior:.2f} p.p.")
with col2:
    with st.container(border=True):
        st.markdown("##### Propostas"); qtd_atual = df_filtrado_mes['propostas_qtd'].sum(); qtd_anterior = df_anterior['propostas_qtd'].sum() if not df_anterior.empty else 0; rs_atual = df_filtrado_mes['propostas_rs'].sum(); rs_anterior = df_anterior['propostas_rs'].sum() if not df_anterior.empty else 0; st.metric("Quantidade", f"{qtd_atual}", f"{qtd_atual - qtd_anterior}"); st.metric("Valor (R$)", f"R$ {rs_atual:,.2f}", f"R$ {rs_atual - rs_anterior:,.2f}")
with col3:
    with st.container(border=True):
        st.markdown("##### Contratos"); qtd_atual = df_filtrado_mes['contratos_qtd'].sum(); qtd_anterior = df_anterior['contratos_qtd'].sum() if not df_anterior.empty else 0; rs_atual = df_filtrado_mes['contratos_rs'].sum(); rs_anterior = df_anterior['contratos_rs'].sum() if not df_anterior.empty else 0; st.metric("Quantidade", f"{qtd_atual}", f"{qtd_atual - qtd_anterior}"); st.metric("Valor (R$)", f"R$ {rs_atual:,.2f}", f"R$ {rs_atual - rs_anterior:,.2f}")
with col4:
    with st.container(border=True):
        st.markdown("##### Atingimento Meta"); meta_atual = df_filtrado_mes['meta_rs'].sum(); contratos_rs_atual = df_filtrado_mes['contratos_rs'].sum(); ating_atual = contratos_rs_atual / meta_atual if meta_atual else 0; st.metric(label="Meta", value=f"{ating_atual:.2%}", delta=f"R$ {contratos_rs_atual:,.2f}"); meta_anterior = df_anterior['meta_rs'].sum() if not df_anterior.empty else 0; contratos_rs_anterior = df_anterior['contratos_rs'].sum() if not df_anterior.empty else 0; ating_anterior = contratos_rs_anterior / meta_anterior if meta_anterior else 0; st.metric(label="Meta Anterior", value=f"{ating_anterior:.2%}", delta=f"R$ {contratos_rs_anterior:,.2f}")
st.markdown("---")
            
# --- MÉTRICAS OPERACIONAIS ---
st.subheader(f"Métricas Operacionais ({data_inicio_op.strftime('%d/%m/%y')} a {data_fim_op.strftime('%d/%m/%y')})")
col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container(border=True):
        st.markdown("##### Oportunidades"); op_atual = df_filtrado_op['oportunidades_qtd'].sum(); op_anterior = df_anterior_op['oportunidades_qtd'].sum(); leads_atual = df_filtrado_op['leads'].sum(); leads_anterior = df_anterior_op['leads'].sum(); st.metric("Oportunidades", f"{op_atual}", f"{op_atual - op_anterior}"); st.metric("Leads Gerados", f"{leads_atual}", f"{leads_atual - leads_anterior}")
with col2:
    with st.container(border=True):
        st.markdown("##### Performance Operacional"); ars_atual = df_filtrado_op['ars_feitos'].sum(); ars_anterior = df_anterior_op['ars_feitos'].sum(); total_clientes = df_filtrado_op[['clientes_essencial_realizado', 'clientes_controle_realizado', 'clientes_avancado_realizado']].sum().sum(); st.metric("ARs feitos", f"{ars_atual} / {total_clientes:.0f}", f"{ars_atual - ars_anterior}"); vel_atual = df_filtrado_op['velocidade_implantacao_dias'].mean(); vel_anterior = df_anterior_op['velocidade_implantacao_dias'].mean() if not df_anterior_op.empty else 0; st.metric("Velocidade Implementação", f"{vel_atual:.1f} dias", f"{vel_atual - vel_anterior:.1f} dias", delta_color="inverse")
with col3:
    with st.container(border=True):
        st.markdown("##### Performance de Mídia"); ctr_atual = df_filtrado_op['ctr_percent'].mean(); ctr_anterior = df_anterior_op['ctr_percent'].mean() if not df_anterior_op.empty else 0; cpr_atual = df_filtrado_op['cpr_rs'].mean(); cpr_anterior = df_anterior_op['cpr_rs'].mean() if not df_anterior_op.empty else 0; st.metric("CTR", f"{ctr_atual:.2%}", f"{ctr_atual - ctr_anterior:.2f} p.p."); st.metric("CPR", f"R$ {cpr_atual:,.2f}", f"R$ {cpr_atual - cpr_anterior:,.2f}", delta_color="inverse")
with col4:
    with st.container(border=True):
        st.markdown("##### Verba Gerenciada"); verba_atual = df_filtrado_op['verba_gerenciada_rs'].sum(); verba_anterior = df_anterior_op['verba_gerenciada_rs'].sum(); st.metric("Total Gasto", f"R$ {verba_atual:,.2f}", f"R$ {verba_atual - verba_anterior:,.2f}");
        with st.columns(1)[0]:
            st.line_chart(df_filtrado_op.set_index('Data')['verba_gerenciada_rs'])