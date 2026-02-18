"""
Frontend oficial do Sistema Estratégico de Obesidade.

Esta versão:
- Utiliza API Flask hospedada no Render para predição
- Carrega dataset local para análises populacionais
- Mantém arquitetura desacoplada (Frontend + API)
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
import plotly.express as px

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title="Sistema Estratégico de Obesidade",
    layout="wide"
)

st.title("🏥 Sistema Estratégico de Análise de Obesidade")
st.markdown("Plataforma de apoio à decisão clínica baseada em Machine Learning e análise populacional.")
st.divider()

# =====================================================
# CONFIGURAÇÃO DA API
# =====================================================
API_URL = "https://obesity-api-2uun.onrender.com/predict"

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
# CARREGAR DADOS PARA DASHBOARD
# =====================================================
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "obesity.csv")
    return pd.read_csv(DATA_PATH)

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
    family_history_pt = st.selectbox("Histórico familiar de obesidade?", ["Sim", "Não"])
    favc_pt = st.selectbox("Consome alimentos calóricos com frequência?", ["Sim", "Não"])
    fcvc = st.slider("Consumo de vegetais (1=baixo, 3=alto)", 1.0, 3.0, 2.0)
    ncp = st.slider("Número de refeições principais por dia", 1.0, 4.0, 3.0)
    caec_pt = st.selectbox("Alimentação entre refeições", ["Não", "Às vezes", "Frequentemente", "Sempre"])
    ch2o = st.slider("Consumo diário de água (1=baixo, 3=alto)", 1.0, 3.0, 2.0)
    calc_pt = st.selectbox("Consumo de álcool", ["Não", "Às vezes", "Frequentemente", "Sempre"])

    st.divider()

    st.subheader("3️⃣ Estilo de Vida")
    smoke_pt = st.selectbox("Fuma?", ["Sim", "Não"])
    scc_pt = st.selectbox("Monitora ingestão calórica?", ["Sim", "Não"])
    faf = st.slider("Atividade física (0=nenhuma, 3=alta)", 0.0, 3.0, 1.0)
    tue = st.slider("Tempo diário de tela (0=baixo, 2=alto)", 0.0, 2.0, 1.0)
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
            "CALC": caec_map[calc_pt],
            "MTRANS": mtrans_map[mtrans_pt]
        }

        try:
            response = requests.post(API_URL, json=input_data)
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                prediction_pt = obesity_map_pt.get(prediction, prediction)
                st.success(f"🎯 Classificação estimada: {prediction_pt}")
            else:
                st.error(f"Erro na API: {response.status_code}")

        except requests.exceptions.RequestException:
            st.error("⚠️ Não foi possível conectar à API.")

# =====================================================
# 📊 DASHBOARD ANALÍTICO
# =====================================================
with tab2:

    st.header("Painel Estratégico de Saúde Populacional")

    # FILTROS
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

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Indivíduos", len(df_filtrado))
    col2.metric("IMC Médio", round(df_filtrado["IMC"].mean(), 2))
    col3.metric("% com Obesidade",
                f"{(df_filtrado['Obesity'].str.contains('Obesity').mean()*100):.1f}%")

    st.divider()

    def painel(coluna, titulo, explicacao, tipo="hist"):
        st.subheader(f"📌 {titulo}")
        st.markdown(explicacao)

        if tipo == "hist":
            fig = px.histogram(
                df_filtrado,
                x=coluna,
                color="Nível de Obesidade",
                barmode="group"
            )
        else:
            fig = px.box(
                df_filtrado,
                x="Nível de Obesidade",
                y=coluna,
                color="Nível de Obesidade"
            )

        st.plotly_chart(fig, use_container_width=True)
        st.divider()

    painel("Nível de Obesidade",
           "Distribuição dos Níveis de Obesidade",
           "Distribuição populacional das classificações.")

    painel("IMC",
           "Índice de Massa Corporal",
           "Comparação do IMC entre os níveis.",
           tipo="box")

    painel("family_history",
           "Histórico Familiar",
           "Relação entre predisposição genética e obesidade.")

    painel("FAVC",
           "Consumo Frequente de Alimentos Calóricos",
           "Impacto da dieta hipercalórica.")

    painel("FCVC",
           "Consumo de Vegetais",
           "Frequência de ingestão de vegetais.",
           tipo="box")

    painel("NCP",
           "Número de Refeições",
           "Frequência alimentar diária.",
           tipo="box")

    painel("CAEC",
           "Alimentação Entre Refeições",
           "Consumo intermediário de alimentos.")

    painel("CH2O",
           "Consumo de Água",
           "Nível médio de ingestão hídrica.",
           tipo="box")

    painel("CALC",
           "Consumo de Álcool",
           "Padrão de ingestão alcoólica.")

    painel("SMOKE",
           "Tabagismo",
           "Distribuição do hábito de fumar.")

    painel("SCC",
           "Monitoramento de Calorias",
           "Controle alimentar declarado.")

    painel("FAF",
           "Atividade Física",
           "Nível de atividade física semanal.",
           tipo="box")

    painel("TUE",
           "Tempo de Tela",
           "Tempo médio de exposição a dispositivos.",
           tipo="box")

    painel("MTRANS",
           "Meio de Transporte",
           "Padrão de mobilidade.")
