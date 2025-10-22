import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --- Configurações da Página ---
st.set_page_config(
    page_title=" Métricas de Analise Financeira",
    page_icon="📊",
    layout="wide"
)

# --- Geração de Dados Fictícios ---
def gerar_dados_ficticios():
    # --- Mês Atual ---
    mrr_orcado_atual = 100000
    mrr_realizado_atual = random.randint(95000, 110000)
    fat_orcado_atual = 105000
    fat_realizado_atual = mrr_realizado_atual + random.randint(3000, 8000)

    # Clientes por plano (Orçado vs Realizado)
    clientes = {
        'atual': {
            'essencial': {'orcado': 80, 'realizado': random.randint(75, 85)},
            'controle': {'orcado': 50, 'realizado': random.randint(48, 55)},
            'avancado': {'orcado': 25, 'realizado': random.randint(22, 30)}
        },
        'anterior': {
            'essencial': {'orcado': 78, 'realizado': random.randint(72, 80)},
            'controle': {'orcado': 48, 'realizado': random.randint(45, 50)},
            'avancado': {'orcado': 22, 'realizado': random.randint(20, 25)}
        }
    }

    # --- Mês Anterior ---
    mrr_orcado_anterior = 98000
    mrr_realizado_anterior = random.randint(90000, 99000)
    fat_orcado_anterior = 99000
    fat_realizado_anterior = mrr_realizado_anterior + random.randint(2500, 6000)

    # --- Consolidando dados para retorno ---
    dados_atuais = {
        "mrr_orcado": mrr_orcado_atual, "mrr_realizado": mrr_realizado_atual,
        "fat_orcado": fat_orcado_atual, "fat_realizado": fat_realizado_atual,
        "clientes": clientes['atual']
    }
    dados_anteriores = {
        "mrr_orcado": mrr_orcado_anterior, "mrr_realizado": mrr_realizado_anterior,
        "fat_orcado": fat_orcado_anterior, "fat_realizado": fat_realizado_anterior,
        "clientes": clientes['anterior']
    }

    # Dados para gráfico de pizza (baseado na receita recorrente por plano)
    precos_planos = {'Essencial': 149, 'Controle': 299, 'Avancado': 499}
    receita_por_plano = {plano: clientes['atual'][plano.lower()]['realizado'] * preco for plano, preco in precos_planos.items()}
    
    return dados_atuais, dados_anteriores, receita_por_plano

# --- Carregando os dados ---
dados_atuais, dados_anteriores, receita_por_plano = gerar_dados_ficticios()

# --- Título do Dashboard ---
st.title("Indicadores Financeiros 💹")
st.markdown("---")

# --- Bloco de MRR ---
st.subheader("MRR (Receita Recorrente Mensal)")
mrr_orc, mrr_real, mrr_dif = st.columns(3)
with mrr_orc:
    orcado_atual = dados_atuais["mrr_orcado"]
    orcado_anterior = dados_anteriores["mrr_orcado"]
    orcado_delta = orcado_atual - orcado_anterior
    st.metric(label="Orçado", value=f"R$ {orcado_atual:,.2f}", delta=f"R$ {orcado_delta:,.2f} vs Mês Anterior")
    with st.expander("🔍 Detalhes"): st.write(f"**Orçado (Mês Anterior):** R$ {orcado_anterior:,.2f}")
with mrr_real:
    realizado_atual = dados_atuais["mrr_realizado"]
    realizado_anterior = dados_anteriores["mrr_realizado"]
    realizado_delta = realizado_atual - realizado_anterior
    st.metric(label="Realizado", value=f"R$ {realizado_atual:,.2f}", delta=f"R$ {realizado_delta:,.2f} vs Mês Anterior")
    with st.expander("🔍 Detalhes"): st.write(f"**Realizado (Mês Anterior):** R$ {realizado_anterior:,.2f}")
with mrr_dif:
    diferenca_atual = dados_atuais["mrr_realizado"] - dados_atuais["mrr_orcado"]
    diferenca_anterior = dados_anteriores["mrr_realizado"] - dados_anteriores["mrr_orcado"]
    diferenca_delta = diferenca_atual - diferenca_anterior
    st.metric(label="Diferença (Real vs Orçado)", value=f"R$ {diferenca_atual:,.2f}", delta=f"R$ {diferenca_delta:,.2f} vs Mês Anterior")
    with st.expander("🔍 Detalhes"): st.write(f"**Diferença (Mês Anterior):** R$ {diferenca_anterior:,.2f}")
st.markdown("---")

# --- Bloco de Faturamento ---
st.subheader("Faturamento")
fat_orc, fat_real, fat_dif = st.columns(3)
with fat_orc:
    orcado_atual = dados_atuais["fat_orcado"]
    orcado_anterior = dados_anteriores["fat_orcado"]
    orcado_delta = orcado_atual - orcado_anterior
    st.metric(label="Orçado", value=f"R$ {orcado_atual:,.2f}", delta=f"R$ {orcado_delta:,.2f} vs Mês Anterior")
    with st.expander("🔍 Detalhes"): st.write(f"**Orçado (Mês Anterior):** R$ {orcado_anterior:,.2f}")
with fat_real:
    realizado_atual = dados_atuais["fat_realizado"]
    realizado_anterior = dados_anteriores["fat_realizado"]
    realizado_delta = realizado_atual - realizado_anterior
    st.metric(label="Realizado", value=f"R$ {realizado_atual:,.2f}", delta=f"R$ {realizado_delta:,.2f} vs Mês Anterior")
    with st.expander("🔍 Detalhes"): st.write(f"**Realizado (Mês Anterior):** R$ {realizado_anterior:,.2f}")
with fat_dif:
    diferenca_atual = dados_atuais["fat_realizado"] - dados_atuais["fat_orcado"]
    diferenca_anterior = dados_anteriores["fat_realizado"] - dados_anteriores["fat_orcado"]
    diferenca_delta = diferenca_atual - diferenca_anterior
    st.metric(label="Diferença (Real vs Orçado)", value=f"R$ {diferenca_atual:,.2f}", delta=f"R$ {diferenca_delta:,.2f} vs Mês Anterior")
    with st.expander("🔍 Detalhes"): st.write(f"**Diferença (Mês Anterior):** R$ {diferenca_anterior:,.2f}")
st.markdown("---")

# --- SEÇÃO DE ANÁLISE DE PLANOS ---
st.subheader("Análise de Clientes e Distribuição por Plano")

# Função auxiliar para exibir as métricas de um plano
def exibir_metricas_plano(nome_plano):
    plano_key = nome_plano.lower()
    dados_plano_atual = dados_atuais['clientes'][plano_key]
    dados_plano_anterior = dados_anteriores['clientes'][plano_key]
    
    st.markdown(f"##### {nome_plano}")
    orcado_atual = dados_plano_atual['orcado']
    orcado_anterior = dados_plano_anterior['orcado']
    st.metric("Orçado", f"{orcado_atual} clientes", delta=f"{orcado_atual - orcado_anterior} vs Mês Ant.")
    realizado_atual = dados_plano_atual['realizado']
    realizado_anterior = dados_plano_anterior['realizado']
    st.metric("Realizado", f"{realizado_atual} clientes", delta=f"{realizado_atual - realizado_anterior} vs Mês Ant.")
    diferenca_atual = realizado_atual - orcado_atual
    diferenca_anterior = realizado_anterior - orcado_anterior
    st.metric("Diferença", f"{diferenca_atual} clientes", delta=f"{diferenca_atual - diferenca_anterior}")
    with st.expander("🔍 Detalhes do Mês Anterior"):
        st.write(f"**Orçado:** {orcado_anterior}")
        st.write(f"**Realizado:** {realizado_anterior}")
        st.write(f"**Diferença:** {diferenca_anterior}")

# --- Layout principal da seção: 3 colunas para planos + 1 para o gráfico
col1, col2, col3, col4 = st.columns(4)
planos = ["Essencial", "Controle", "Avancado"]
colunas = [col1, col2, col3]

# Itera sobre os planos e colunas para criar os containers de métricas
for i, plano in enumerate(planos):
    with colunas[i]:
        with st.container(border=True):
            exibir_metricas_plano(plano)

# Adiciona o gráfico de pizza na quarta coluna
with col4:
    with st.container(border=True):
        df_pizza = pd.DataFrame(receita_por_plano.items(), columns=['Plano', 'Receita'])
        fig = px.pie(
            df_pizza, 
            names='Plano', 
            values='Receita', 
            hole=.4,
            color_discrete_sequence=px.colors.sequential.GnBu_r
        )
        
        fig.update_traces(textposition='inside', textinfo='percent')
        fig.update_layout(
            title_text="Distribuição dos Planos",
            title_x=0.01,
            title_font_size=16,

            showlegend=True,
            legend=dict(
                title_text="",
                orientation="h",
                yanchor="top",
                y=-0.1,  # Posição abaixo do gráfico
                xanchor="center",
                x=0.5,
                font=dict(size=10) # Fonte menor para a legenda
            ),
            margin=dict(l=40, r=40, t=60, b=80), # Margens para ajustar o layout
        )
        st.plotly_chart(fig, use_container_width=True)