import streamlit as st
import pandas as pd
import plotly.express as px
import random

# --- Configurações da Página ---
st.set_page_config(
    page_title=" Indicadores Kaptha",
    page_icon="📊",
    layout="wide"
)

# --- Geração de Dados Fictícios ---
def gerar_dados_ficticios():
    # --- DADOS FINANCEIROS ---
    mrr_orcado_atual = 100000; mrr_realizado_atual = random.randint(95000, 110000)
    fat_orcado_atual = 105000; fat_realizado_atual = mrr_realizado_atual + random.randint(3000, 8000)
    mrr_orcado_anterior = 98000; mrr_realizado_anterior = random.randint(90000, 99000)
    fat_orcado_anterior = 99000; fat_realizado_anterior = mrr_realizado_anterior + random.randint(2500, 6000)
    
    # --- DADOS DE PLANOS ---
    clientes = {'atual': {'essencial': {'orcado': 80, 'realizado': random.randint(75, 85)},'controle': {'orcado': 50, 'realizado': random.randint(48, 55)},'avancado': {'orcado': 25, 'realizado': random.randint(22, 30)}},'anterior': {'essencial': {'orcado': 78, 'realizado': random.randint(72, 80)},'controle': {'orcado': 48, 'realizado': random.randint(45, 50)},'avancado': {'orcado': 22, 'realizado': random.randint(20, 25)}}}
    
    # --- DADOS DO FUNIL DE VENDAS ---
    funil = {'atual': {'leads': random.randint(800, 1200),'propostas_qtd': random.randint(80, 120),'propostas_rs': random.randint(120000, 180000),'contratos_qtd': random.randint(25, 45),'contratos_rs': random.randint(95000, 130000),'meta_rs': 115000},'anterior': {'leads': random.randint(750, 1100),'propostas_qtd': random.randint(70, 110),'propostas_rs': random.randint(110000, 160000),'contratos_qtd': random.randint(20, 40),'contratos_rs': random.randint(85000, 120000),'meta_rs': 110000}}
    
    # --- DADOS OPERACIONAIS E DE MARKETING ---
    operacional = {'atual': {'oportunidades_qtd': int(funil['atual']['leads'] * random.uniform(0.2, 0.3)),'ars_feitos': random.randint(40, 60),'velocidade_implantacao_dias': random.randint(5, 12),'ctr_percent': random.uniform(0.01, 0.05),'cpr_rs': random.uniform(15.0, 25.0),'verba_gerenciada_rs': random.randint(18000, 25000)},'anterior': {'oportunidades_qtd': int(funil['anterior']['leads'] * random.uniform(0.2, 0.3)),'ars_feitos': random.randint(35, 55),'velocidade_implantacao_dias': random.randint(7, 15),'ctr_percent': random.uniform(0.01, 0.05),'cpr_rs': random.uniform(18.0, 28.0),'verba_gerenciada_rs': random.randint(15000, 22000)}}
    
    # --- Consolidando dados para retorno ---
    dados_atuais = {"mrr_orcado": mrr_orcado_atual, "mrr_realizado": mrr_realizado_atual, "fat_orcado": fat_orcado_atual, "fat_realizado": fat_realizado_atual, "clientes": clientes['atual']}
    dados_anteriores = {"mrr_orcado": mrr_orcado_anterior, "mrr_realizado": mrr_realizado_anterior, "fat_orcado": fat_orcado_anterior, "fat_realizado": fat_realizado_anterior, "clientes": clientes['anterior']}
    precos_planos = {'Essencial': 149, 'Controle': 299, 'Avancado': 499}
    receita_por_plano = {plano: clientes['atual'][plano.lower()]['realizado'] * preco for plano, preco in precos_planos.items()}
    
    return dados_atuais, dados_anteriores, receita_por_plano, funil['atual'], funil['anterior'], operacional['atual'], operacional['anterior']

# --- Carregando os dados ---
dados_atuais, dados_anteriores, receita_por_plano, dados_funil_atual, dados_funil_anterior, dados_op_atual, dados_op_anterior = gerar_dados_ficticios()

# --- Título do Dashboard ---
st.title("Indicadores Kaptha 💹")
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
        
st.subheader("Funil de Vendas e Metas")

# Layout principal: 4 colunas para os containers
col1, col2, col3, col4 = st.columns(4)

# --- Coluna 1: Leads e Conversão ---
with col1:
    with st.container(border=True):
        st.markdown("##### Leads")
        
        # Métrica: Quantidade de Leads
        leads_atual = dados_funil_atual['leads']
        leads_anterior = dados_funil_anterior['leads']
        st.metric("Quantidade Total", f"{leads_atual}", delta=f"{leads_atual - leads_anterior}")

        # Métrica: Taxa de Conversão Geral (Lead -> Contrato)
        tx_atual = dados_funil_atual['contratos_qtd'] / leads_atual if leads_atual else 0
        tx_anterior = dados_funil_anterior['contratos_qtd'] / leads_anterior if leads_anterior else 0
        delta_tx = tx_atual - tx_anterior
        st.metric("Taxa de Conversão", f"{tx_atual:.2%}", delta=f"{delta_tx:.2f} p.p.")
        
        with st.expander("🔍 Detalhes (Mês Anterior)"):
            st.write(f"**Leads:** {leads_anterior}")
            st.write(f"**Taxa de Conversão:** {tx_anterior:.2%}")

# --- Coluna 2: Propostas ---
with col2:
    with st.container(border=True):
        st.markdown("##### Propostas")
        
        # Métrica: Quantidade de Propostas
        qtd_atual = dados_funil_atual['propostas_qtd']
        qtd_anterior = dados_funil_anterior['propostas_qtd']
        st.metric("Quantidade", f"{qtd_atual}", delta=f"{qtd_atual - qtd_anterior}")
        
        # Métrica: Valor das Propostas
        rs_atual = dados_funil_atual['propostas_rs']
        rs_anterior = dados_funil_anterior['propostas_rs']
        st.metric("Valor (R$)", f"R$ {rs_atual:,.2f}", delta=f"R$ {rs_atual - rs_anterior:,.2f}")
        
        with st.expander("🔍 Análise Anterior"):
            st.write(f"**Propostas Qtd:** {qtd_anterior}")
            st.write(f"**Propostas R$:** R$ {rs_anterior:,.2f}")

# --- Coluna 3: Contratos ---
with col3:
    with st.container(border=True):
        st.markdown("##### Contratos")
        
        # Métrica: Quantidade de Contratos
        qtd_atual = dados_funil_atual['contratos_qtd']
        qtd_anterior = dados_funil_anterior['contratos_qtd']
        st.metric("Quantidade", f"{qtd_atual}", delta=f"{qtd_atual - qtd_anterior}")
        
        # Métrica: Valor dos Contratos
        rs_atual = dados_funil_atual['contratos_rs']
        rs_anterior = dados_funil_anterior['contratos_rs']
        st.metric("Valor (R$)", f"R$ {rs_atual:,.2f}", delta=f"R$ {rs_atual - rs_anterior:,.2f}")
        
        with st.expander("🔍 Detalhes"):
            st.write(f"**Contratos Qtd:** {qtd_anterior}")
            st.write(f"**Contratos R$:** R$ {rs_anterior:,.2f}")

# --- Coluna 4: Atingimento da Meta ---
with col4:
    with st.container(border=True):
        st.markdown("##### Atingimento Meta")

        # Métrica: Mês Atual
        meta_atual = dados_funil_atual['meta_rs']
        contratos_rs_atual = dados_funil_atual['contratos_rs']
        ating_atual = contratos_rs_atual / meta_atual if meta_atual else 0
        st.metric(
            label="Meta",
            value=f"{ating_atual:.2%}",
            delta=f"R$ {contratos_rs_atual:,.2f}"
        )

        # Métrica: Mês Anterior
        meta_anterior = dados_funil_anterior['meta_rs']
        contratos_rs_anterior = dados_funil_anterior['contratos_rs']
        ating_anterior = contratos_rs_anterior / meta_anterior if meta_anterior else 0
        st.metric(
            label="Meta Anterior",
            value=f"{ating_anterior:.2%}",
            delta=f"R$ {contratos_rs_anterior:,.2f}"
        )
        
        with st.expander("🔍 Detalhes"):
            st.write(f"**Meta Atual:** R$ {contratos_rs_atual:,.2f} de R$ {meta_atual:,.2f}")
            st.write(f"**Meta Anterior:** R$ {contratos_rs_anterior:,.2f} de R$ {meta_anterior:,.2f}")
            
st.subheader("Métricas Operacionais e de Marketing")
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.markdown("##### Oportunidades")
        # Oportunidades
        op_atual = dados_op_atual['oportunidades_qtd']
        op_anterior = dados_op_anterior['oportunidades_qtd']
        st.metric("Oportunidades", f"{op_atual}", delta=f"{op_atual - op_anterior}")
        # Leads Gerados (reutilizando dados)
        leads_atual = dados_funil_atual['leads']
        leads_anterior = dados_funil_anterior['leads']
        st.metric("Leads Gerados", f"{leads_atual}", delta=f"{leads_atual - leads_anterior}")
        with st.expander("🔍 Detalhes"):
            st.write(f"**Oportunidades (mês anterior):** {op_anterior}")
            st.write(f"**Leads Gerados (mês anterior):** {leads_anterior}")

with col2:
    with st.container(border=True):
        st.markdown("##### Performance Operacional")
        # ARs
        ars_atual = dados_op_atual['ars_feitos']
        ars_anterior = dados_op_anterior['ars_feitos']
        total_clientes = sum(p['realizado'] for p in dados_atuais['clientes'].values())
        st.metric("ARs feitos", f"{ars_atual} / {total_clientes}", delta=f"{ars_atual - ars_anterior}")
        # Velocidade de Implementação
        vel_atual = dados_op_atual['velocidade_implantacao_dias']
        vel_anterior = dados_op_anterior['velocidade_implantacao_dias']
        st.metric("Velocidade Implementação", f"{vel_atual} dias", delta=f"{vel_atual - vel_anterior} dias", delta_color="inverse", help="Menos dias é melhor")
        with st.expander("🔍 Detalhes"):
            st.write(f"**ARs feitos (mês anterior):** {ars_anterior}")
            st.write(f"**Velocidade (mês anterior):** {vel_anterior} dias")
            
with col3:
    with st.container(border=True):
        st.markdown("##### Performance de Mídia")
        # CTR
        ctr_atual = dados_op_atual['ctr_percent']
        ctr_anterior = dados_op_anterior['ctr_percent']
        st.metric("CTR", f"{ctr_atual:.2%}", delta=f"{ctr_atual - ctr_anterior:.2f} p.p.")
        # CPR
        cpr_atual = dados_op_atual['cpr_rs']
        cpr_anterior = dados_op_anterior['cpr_rs']
        st.metric("CPR", f"R$ {cpr_atual:,.2f}", delta=f"R$ {cpr_atual - cpr_anterior:,.2f}", delta_color="inverse", help="Menor custo é melhor")
        with st.expander("🔍 Detalhes"):
            st.write(f"**CTR (mês anterior):** {ctr_anterior:.2%}")
            st.write(f"**CPR (mês anterior):** R$ {cpr_anterior:,.2f}")

with col4:
    with st.container(border=True): # Este container define a borda
        st.markdown("##### Verba Gerenciada")
        
        verba_atual = dados_op_atual['verba_gerenciada_rs']
        verba_anterior = dados_op_anterior['verba_gerenciada_rs']
        st.metric("Total Gasto", f"R$ {verba_atual:,.2f}", delta=f"R$ {verba_atual - verba_anterior:,.2f}")

        # --- Gráfico de Linha da Evolução da Verba ATUAL ---
        dias_no_mes = 21
        gasto_diario_simulado = [random.uniform(0.5, 1.5) for _ in range(dias_no_mes)]
        gasto_acumulado_bruto = pd.Series(gasto_diario_simulado).cumsum()
        fator_escala = verba_atual / gasto_acumulado_bruto.iloc[-1] if gasto_acumulado_bruto.iloc[-1] > 0 else 0
        gasto_acumulado_final = (gasto_acumulado_bruto * fator_escala)

        df_verba_evolucao = pd.DataFrame({
            'Dia': range(1, dias_no_mes + 1),
            'Verba Acumulada': gasto_acumulado_final
        })
        
        # Envolva o gráfico em uma coluna dentro do container para respeitar a borda
        with st.columns(1)[0]: # Cria uma única sub-coluna que respeita o container pai
            st.line_chart(df_verba_evolucao.set_index('Dia'))

        with st.expander("🔍 Detalhes"):
            st.write(f"**Verba (mês anterior):** R$ {verba_anterior:,.2f}")