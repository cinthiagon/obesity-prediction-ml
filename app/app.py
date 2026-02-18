"""
Este aplicativo foi desenvolvido como parte de um trabalho acadêmico aplicado,
com foco na integração entre modelagem preditiva e inteligência analítica voltada
à tomada de decisão em saúde.

Nesta versão standalone, o modelo de Machine Learning é carregado diretamente
no Streamlit, eliminando a dependência de API externa para fins de estabilidade
em ambiente de deploy gratuito.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import joblib

# =====================================================
# CONFIGURAÇÃO
# =====================================================
st.set_page_config(page_title="Sistema Estratégico de Obesidade", layout="wide")

st.title("🏥 Sistema Estratégico de Análise de Obesidade")
st.markdown("Plataforma de apoio à decisão clínica baseada em Machine Learning e análise populacional.")

# =====================================================
# CARREGAR MODELO (STANDALONE)
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "obesity_model.pkl")

model = joblib.load(MODEL_PATH)

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
    data_path = os.path.join(BASE_DIR, "obesity.csv")
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

        input_data = pd.DataFrame([{
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
        }])

        prediction_raw = model.predict(input_data)[0]
        prediction_pt = obesity_map_pt.get(prediction_raw, prediction_raw)

        st.success(f"🎯 Classificação estimada: {prediction_pt}")

# =====================================================
# 📊 DASHBOARD (mantido igual)
# =====================================================
with tab2:

    st.header("Painel Estratégico de Saúde Populacional")

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

    df_filtrado["risk_score"] = (
        (df_filtrado["family_history"] == "yes").astype(int) * 2 +
        (df_filtrado["FAF"] == 0).astype(int) * 2 +
        (df_filtrado["TUE"] >= 1.5).astype(int) +
        (df_filtrado["CH2O"] == 1).astype(int) +
        (df_filtrado["FAVC"] == "yes").astype(int)
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("IMC Médio", round(df_filtrado["IMC"].mean(), 2))
    col2.metric("Idade Média", round(df_filtrado["Age"].mean(), 1))
    col3.metric("% Obesidade",
                f"{(df_filtrado['Obesity'].str.contains('Obesity').mean()*100):.1f}%")
    col4.metric("Score Médio de Risco",
                round(df_filtrado["risk_score"].mean(), 2))

    st.divider()

    fig = px.histogram(df_filtrado, x="Nível de Obesidade",
                       color="Nível de Obesidade")
    st.plotly_chart(fig, use_container_width=True)
