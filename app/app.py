"""
Este aplicativo foi desenvolvido como parte de um trabalho acadêmico aplicado, com foco na
integração entre modelagem preditiva e inteligência analítica voltada à tomada de decisão
em saúde. A solução combina um modelo de Machine Learning treinado para classificação de
níveis de obesidade com um painel estratégico interativo construído em Streamlit.

A aplicação está estruturada em duas camadas principais: (1) módulo de predição individual,
que coleta dados clínicos e comportamentais do paciente e realiza inferência por meio de
uma API Flask contendo o modelo previamente treinado; e (2) painel analítico populacional,
que permite segmentação por faixa etária e gênero, cálculo de score comportamental de risco,
análise multivariada e visualização detalhada de todas as variáveis clínicas e de estilo de
vida presentes no formulário.

Cada visualização inclui contextualização interpretativa, garantindo não apenas exposição
gráfica dos dados, mas suporte à análise clínica e estratégica. O projeto foi concebido
com foco em aplicabilidade real no ambiente hospitalar, possibilitando tanto avaliação
individual quanto monitoramento populacional e apoio a decisões preventivas baseadas em dados.
"""


import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
import plotly.express as px

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(page_title="Sistema Estratégico de Obesidade", layout="wide")

st.title("🏥 Sistema Estratégico de Análise de Obesidade")
st.markdown("Plataforma de apoio à decisão clínica baseada em Machine Learning e análise populacional.")

# =====================================================
# MAPAS DE TRADUÇÃO
# =====================================================
yes_no_map = {"Sim": "yes", "Não": "no"}
gender_map = {"Masculino": "Male", "Feminino": "Female"}

caec_map = {
    "Não": "no",
    "Às vezes": "Sometimes",
    "Frequentemente": "Frequently",
    "Sempre": "Always"
}

calc_map = caec_map.copy()

mtrans_map = {
    "Transporte Público": "Public_Transportation",
    "Caminhada": "Walking",
    "Automóvel": "Automobile",
    "Motocicleta": "Motorbike",
    "Bicicleta": "Bike"
}

obesity_map_pt = {
    "Insufficient_Weight": "Peso Insuficiente",
    "Normal_Weight": "Peso Normal",
    "Overweight_Level_I": "Sobrepeso Grau I",
    "Overweight_Level_II": "Sobrepeso Grau II",
    "Obesity_Type_I": "Obesidade Tipo I",
    "Obesity_Type_II": "Obesidade Tipo II",
    "Obesity_Type_III": "Obesidade Tipo III"
}

# =====================================================
# CARREGAR DADOS
# =====================================================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "obesity.csv")
    return pd.read_csv(data_path)

df = load_data()
df["IMC"] = df["Weight"] / (df["Height"] ** 2)
df["Nível de Obesidade"] = df["Obesity"].map(obesity_map_pt)

# =====================================================
# ABAS
# =====================================================
tab1, tab2 = st.tabs(["🔍 Predição Individual", "📊 Painel Analítico"])

# =====================================================
# 🔍 PREDIÇÃO INDIVIDUAL
# =====================================================
with tab1:

    st.header("Avaliação Clínica Individual")

    st.subheader("1️⃣ Dados Corporais")
    gender_pt = st.selectbox("Gênero", ["Masculino", "Feminino"])
    age = st.number_input("Idade", 0, 120, 30)
    height = st.number_input("Altura (m)", 1.0, 2.5, 1.70)
    weight = st.number_input("Peso (kg)", 30.0, 300.0, 70.0)

    st.divider()

    st.subheader("2️⃣ Hábitos Alimentares")
    family_history_pt = st.selectbox("Histórico familiar?", ["Sim", "Não"])
    favc_pt = st.selectbox("Alimentos calóricos frequentes?", ["Sim", "Não"])
    fcvc = st.slider("Consumo de vegetais (1=baixo, 3=alto)", 1.0, 3.0, 2.0)
    ncp = st.slider("Refeições principais por dia", 1.0, 4.0, 3.0)
    caec_pt = st.selectbox("Alimentação entre refeições", ["Não", "Às vezes", "Frequentemente", "Sempre"])
    ch2o = st.slider("Consumo de água (1=baixo, 3=alto)", 1.0, 3.0, 2.0)
    calc_pt = st.selectbox("Consumo de álcool", ["Não", "Às vezes", "Frequentemente", "Sempre"])

    st.divider()

    st.subheader("3️⃣ Estilo de Vida")
    smoke_pt = st.selectbox("Fuma?", ["Sim", "Não"])
    scc_pt = st.selectbox("Monitora calorias?", ["Sim", "Não"])
    faf = st.slider("Atividade física (0=nenhuma, 3=alta)", 0.0, 3.0, 1.0)
    tue = st.slider("Tempo de tela (0=baixo, 2=alto)", 0.0, 2.0, 1.0)
    mtrans_pt = st.selectbox("Meio de transporte",
                             ["Transporte Público", "Caminhada", "Automóvel", "Motocicleta", "Bicicleta"])

    if st.button("🔎 Calcular Classificação"):

        input_data = {
            "Gender": gender_map[gender_pt],
            "Age": age,
            "Height": height,
            "Weight": weight,
            "family_history": yes_no_map[family_history_pt],
            "FAVC": yes_no_map[favc_pt],
            "FCVC": fcvc,
            "NCP": ncp,
            "CAEC": caec_map[caec_pt],
            "SMOKE": yes_no_map[smoke_pt],
            "CH2O": ch2o,
            "SCC": yes_no_map[scc_pt],
            "FAF": faf,
            "TUE": tue,
            "CALC": calc_map[calc_pt],
            "MTRANS": mtrans_map[mtrans_pt]
        }

        try:
            response = requests.post("http://SEU-ENDERECO-API/predict", json=input_data)
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                st.success(f"🎯 Classificação estimada: {prediction}")
            else:
                st.error("Erro ao consultar API.")
        except:
            st.error("API não está ativa.")

# =====================================================
# 📊 DASHBOARD COMPLETO
# =====================================================
with tab2:

    st.header("Painel Estratégico de Saúde Populacional")

    # FILTROS
    st.sidebar.header("Filtros")
    idade_min, idade_max = st.sidebar.slider(
        "Faixa Etária",
        int(df["Age"].min()),
        int(df["Age"].max()),
        (int(df["Age"].min()), int(df["Age"].max()))
    )

    genero = st.sidebar.selectbox("Gênero", ["Todos", "Male", "Female"])

    df_filtrado = df[(df["Age"] >= idade_min) & (df["Age"] <= idade_max)].copy()

    if genero != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Gender"] == genero]

    # SCORE
    df_filtrado["risk_score"] = (
        (df_filtrado["family_history"] == "yes").astype(int) * 2 +
        (df_filtrado["FAF"] == 0).astype(int) * 2 +
        (df_filtrado["TUE"] >= 1.5).astype(int) +
        (df_filtrado["CH2O"] == 1).astype(int) +
        (df_filtrado["FAVC"] == "yes").astype(int)
    )

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("IMC Médio", round(df_filtrado["IMC"].mean(), 2))
    col2.metric("Idade Média", round(df_filtrado["Age"].mean(), 1))
    col3.metric("% Obesidade",
                f"{(df_filtrado['Obesity'].str.contains('Obesity').mean()*100):.1f}%")
    col4.metric("Score Médio de Risco",
                round(df_filtrado["risk_score"].mean(), 2))

    st.divider()

    # FUNÇÃO AUXILIAR PARA PAINÉIS
    def painel_hist(coluna, titulo, explicacao):
        st.subheader(titulo)
        st.markdown(explicacao)
        fig = px.histogram(
            df_filtrado,
            x=coluna,
            color="Nível de Obesidade",
            barmode="group",
            color_discrete_sequence=px.colors.sequential.Blues
        )
        st.plotly_chart(fig, use_container_width=True)
        st.divider()

    def painel_box(coluna, titulo, explicacao):
        st.subheader(titulo)
        st.markdown(explicacao)
        fig = px.box(
            df_filtrado,
            x="Nível de Obesidade",
            y=coluna,
            color="Nível de Obesidade",
            color_discrete_sequence=px.colors.sequential.Blues
        )
        st.plotly_chart(fig, use_container_width=True)
        st.divider()

    # DISTRIBUIÇÕES
    painel_hist("Nível de Obesidade",
                "📌 Distribuição dos Níveis de Obesidade",
                "Distribuição populacional dos níveis de obesidade.")

    painel_box("IMC",
               "📌 IMC por Nível de Obesidade",
               "Comparação do índice de massa corporal entre os grupos.")

    painel_hist("family_history",
                "📌 Histórico Familiar",
                "Associação entre predisposição genética e obesidade.")

    painel_hist("FAVC",
                "📌 Consumo de Alimentos Calóricos",
                "Impacto da dieta hipercalórica.")

    painel_box("FCVC",
               "📌 Consumo de Vegetais",
               "Frequência de ingestão de vegetais.")

    painel_box("NCP",
               "📌 Número de Refeições",
               "Frequência alimentar diária.")

    painel_hist("CAEC",
                "📌 Alimentação Entre Refeições",
                "Consumo intermediário de alimentos.")

    painel_box("CH2O",
               "📌 Consumo de Água",
               "Nível médio de ingestão hídrica.")

    painel_hist("CALC",
                "📌 Consumo de Álcool",
                "Padrão de ingestão alcoólica.")

    painel_hist("SMOKE",
                "📌 Tabagismo",
                "Distribuição do hábito de fumar.")

    painel_hist("SCC",
                "📌 Monitoramento de Calorias",
                "Controle alimentar declarado.")

    painel_box("FAF",
               "📌 Atividade Física",
               "Nível de atividade física semanal.")

    painel_box("TUE",
               "📌 Tempo de Tela",
               "Tempo médio de exposição a dispositivos.")

    painel_hist("MTRANS",
                "📌 Meio de Transporte",
                "Padrão de mobilidade e possível associação com sedentarismo.")

    painel_hist("Gender",
                "📌 Distribuição por Gênero",
                "Diferenças de prevalência entre homens e mulheres.")
