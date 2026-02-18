"""
Sistema Estratégico de Análise de Obesidade

Aplicação desenvolvida para integrar modelo preditivo de Machine Learning
e painel analítico estratégico voltado ao apoio à decisão clínica.

Versão Standalone:
O modelo é carregado localmente, sem dependência de API externa.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import joblib

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title="Sistema Estratégico de Obesidade",
    layout="wide"
)

st.title("🏥 Sistema Estratégico de Análise de Obesidade")
st.subheader("Plataforma de apoio à decisão clínica baseada em Machine Learning e análise populacional.")
st.divider()

# =====================================================
# CAMINHOS CORRETOS PARA STREAMLIT CLOUD
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "obesity_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "obesity.csv")

# =====================================================
# CARREGAR MODELO COM CACHE
# =====================================================
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# =====================================================
# MAPAS DE TRADUÇÃO
# =====================================================
yes_no_map = {"Sim": "yes", "Não": "no"}
yes_no_display = {"yes": "Sim", "no": "Não"}

gender_map = {"Masculino": "Male", "Feminino": "Female"}
gender_display = {"Male": "Masculino", "Female": "Feminino"}

caec_map = {
    "Não": "no",
    "Às vezes": "Sometimes",
    "Frequentemente": "Frequently",
    "Sempre": "Always"
}

caec_display = {
    "no": "Não",
    "Sometimes": "Às vezes",
    "Frequently": "Frequentemente",
    "Always": "Sempre"
}

mtrans_map = {
    "Transporte Público": "Public_Transportation",
    "Caminhada": "Walking",
    "Automóvel": "Automobile",
    "Motocicleta": "Motorbike",
    "Bicicleta": "Bike"
}

mtrans_display = {
    "Public_Transportation": "Transporte Público",
    "Walking": "Caminhada",
    "Automobile": "Automóvel",
    "Motorbike": "Motocicleta",
    "Bike": "Bicicleta"
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
    return pd.read_csv(DATA_PATH)

df = load_data()

df["IMC"] = df["Weight"] / (df["Height"] ** 2)
df["Nível de Obesidade"] = df["Obesity"].map(obesity_map_pt)

# Traduzir valores para dashboard
df["Gender"] = df["Gender"].map(gender_display)
df["family_history"] = df["family_history"].map(yes_no_display)
df["FAVC"] = df["FAVC"].map(yes_no_display)
df["SMOKE"] = df["SMOKE"].map(yes_no_display)
df["SCC"] = df["SCC"].map(yes_no_display)
df["CAEC"] = df["CAEC"].map(caec_display)
df["CALC"] = df["CALC"].map(caec_display)
df["MTRANS"] = df["MTRANS"].map(mtrans_display)

# =====================================================
# ABAS
# =====================================================
tab1, tab2 = st.tabs(["🔍 Predição Individual", "📊 Painel Analítico"])

# =====================================================
# 🔍 PREDIÇÃO INDIVIDUAL
# =====================================================
with tab1:

    st.header("Avaliação Clínica Individual")

    gender_pt = st.selectbox("Gênero", ["Masculino", "Feminino"])
    age = st.number_input("Idade", 0, 120, 30)
    height = st.number_input("Altura (m)", 1.0, 2.5, 1.70)
    weight = st.number_input("Peso (kg)", 30.0, 300.0, 70.0)

    family_history_pt = st.selectbox("Histórico familiar de excesso de peso?", ["Sim", "Não"])
    favc_pt = st.selectbox("Consumo frequente de alimentos calóricos?", ["Sim", "Não"])
    fcvc = st.slider("Frequência de consumo de vegetais (1=baixo, 3=alto)", 1.0, 3.0, 2.0)
    ncp = st.slider("Número de refeições principais por dia", 1.0, 4.0, 3.0)
    caec_pt = st.selectbox("Alimentação entre refeições", ["Não", "Às vezes", "Frequentemente", "Sempre"])
    ch2o = st.slider("Consumo diário de água (1=baixo, 3=alto)", 1.0, 3.0, 2.0)
    calc_pt = st.selectbox("Consumo de álcool", ["Não", "Às vezes", "Frequentemente", "Sempre"])
    smoke_pt = st.selectbox("Fuma?", ["Sim", "Não"])
    scc_pt = st.selectbox("Monitora ingestão calórica?", ["Sim", "Não"])
    faf = st.slider("Nível de atividade física (0=nenhuma, 3=alta)", 0.0, 3.0, 1.0)
    tue = st.slider("Tempo diário de uso de tela (0=baixo, 2=alto)", 0.0, 2.0, 1.0)
    mtrans_pt = st.selectbox("Meio de transporte principal",
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
            "CALC": caec_map[calc_pt],
            "MTRANS": mtrans_map[mtrans_pt]
        }])

        prediction_raw = model.predict(input_data)[0]
        prediction_pt = obesity_map_pt.get(prediction_raw, prediction_raw)

        st.success(f"🎯 Classificação estimada: {prediction_pt}")

# =====================================================
# 📊 DASHBOARD ANALÍTICO COMPLETO
# =====================================================
with tab2:

    st.header("Painel Estratégico de Saúde Populacional")

    idade_min, idade_max = st.sidebar.slider(
        "Faixa Etária",
        int(df["Age"].min()),
        int(df["Age"].max()),
        (int(df["Age"].min()), int(df["Age"].max()))
    )

    genero = st.sidebar.selectbox("Gênero", ["Todos", "Masculino", "Feminino"])

    df_filtrado = df[(df["Age"] >= idade_min) & (df["Age"] <= idade_max)].copy()

    if genero != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Gender"] == genero]

    # KPIs
    st.subheader("📌 Indicadores Estratégicos")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Indivíduos", len(df_filtrado))
    col2.metric("IMC Médio", round(df_filtrado["IMC"].mean(), 2))
    col3.metric("% com Obesidade",
                f"{(df_filtrado['Nível de Obesidade'].str.contains('Obesidade').mean()*100):.1f}%")

    st.divider()

    def painel_hist(coluna, titulo, explicacao):
        st.subheader(f"📌 {titulo}")
        st.markdown(explicacao)
        fig = px.histogram(
            df_filtrado,
            x=coluna,
            color="Nível de Obesidade",
            barmode="group",
            labels={coluna: titulo}
        )
        st.plotly_chart(fig, width="stretch")
        st.divider()

    def painel_box(coluna, titulo, explicacao):
        st.subheader(f"📌 {titulo}")
        st.markdown(explicacao)
        fig = px.box(
            df_filtrado,
            x="Nível de Obesidade",
            y=coluna,
            color="Nível de Obesidade",
            labels={coluna: titulo}
        )
        st.plotly_chart(fig, width="stretch")
        st.divider()

    # TODOS OS PAINÉIS
    painel_hist("Nível de Obesidade", "Distribuição dos Níveis de Obesidade",
                "Distribuição populacional das classificações de obesidade.")

    painel_box("IMC", "Índice de Massa Corporal (IMC)",
               "Comparação do IMC entre os diferentes níveis de obesidade.")

    painel_box("Age", "Idade",
               "Distribuição etária entre os níveis de obesidade.")

    painel_hist("family_history", "Histórico Familiar de Excesso de Peso",
                "Possível influência genética associada à obesidade.")

    painel_hist("FAVC", "Consumo Frequente de Alimentos Calóricos",
                "Impacto da dieta hipercalórica na classificação.")

    painel_box("FCVC", "Frequência de Consumo de Vegetais",
               "Análise do padrão de ingestão de vegetais.")

    painel_box("NCP", "Número de Refeições Principais por Dia",
               "Distribuição da frequência alimentar.")

    painel_hist("CAEC", "Alimentação Entre Refeições",
                "Avaliação do hábito alimentar intermediário.")

    painel_box("CH2O", "Consumo Diário de Água",
               "Avaliação da ingestão hídrica média.")

    painel_hist("CALC", "Frequência de Consumo de Álcool",
                "Análise do padrão de ingestão alcoólica.")

    painel_hist("SMOKE", "Tabagismo",
                "Distribuição do hábito de fumar.")

    painel_hist("SCC", "Monitoramento de Ingestão Calórica",
                "Comparação entre indivíduos que monitoram calorias.")

    painel_box("FAF", "Nível de Atividade Física",
               "Distribuição do nível de atividade física.")

    painel_box("TUE", "Tempo Diário de Uso de Tela",
               "Possível associação com comportamento sedentário.")

    painel_hist("MTRANS", "Meio de Transporte Utilizado",
                "Padrão de mobilidade associado aos níveis de obesidade.")
