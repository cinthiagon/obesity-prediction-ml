# =========================
# A aplicação preditiva foi desenvolvida com foco em usabilidade clínica, 
# apresentando interface em português e explicações claras sobre as escalas e unidades de cada variável utilizada. 
# Para preservar a consistência do modelo treinado, foi implementada uma camada de mapeamento entre as respostas do usuário 
# e as categorias originais do modelo, garantindo clareza para o usuário final sem impacto na performance preditiva.

# Antes do deploy, o projeto foi atualizado com um novo commit contendo a versão final da aplicação,
# o modelo treinado e os ajustes necessários para execução em ambiente de produção,
# garantindo que o código utilizado no deploy correspondesse exatamente ao estado versionado no repositório.

# O sistema final integra uma aplicação preditiva individual e um painel analítico populacional 
# em uma única solução desenvolvida em Streamlit. Enquanto o módulo preditivo auxilia a avaliação clínica individual, 
# o painel analítico fornece insights estratégicos baseados em dados históricos, apoiando decisões preventivas, 
# educativas e de gestão em saúde.
# =========================

import streamlit as st
import pandas as pd
import joblib
import os

# =========================
# Configuração da página
# =========================
st.set_page_config(
    page_title="Sistema Preditivo de Obesidade",
    layout="centered"
)

st.title("🏥 Sistema Preditivo e Analítico de Obesidade")
st.write(
    """
    Esta aplicação utiliza **Machine Learning** para apoiar profissionais de saúde
    na **avaliação individual** e na **análise populacional** relacionada à obesidade.

    ⚠️ **Aviso:** os resultados apresentados são apenas **apoio à decisão clínica**
    e **não substituem** avaliação médica profissional.
    """
)

# =========================
# Mapas PT -> EN (modelo)
# =========================
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

# =========================
# Mapas EN -> PT (painel)
# =========================
obesity_map_pt = {
    "Insufficient_Weight": "Peso Insuficiente",
    "Normal_Weight": "Peso Normal",
    "Overweight_Level_I": "Sobrepeso Grau I",
    "Overweight_Level_II": "Sobrepeso Grau II",
    "Obesity_Type_I": "Obesidade Tipo I",
    "Obesity_Type_II": "Obesidade Tipo II",
    "Obesity_Type_III": "Obesidade Tipo III"
}

gender_map_pt = {
    "Male": "Masculino",
    "Female": "Feminino"
}

# =========================
# Carregamento do modelo
# =========================
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "..", "models", "obesity_model.pkl")
    return joblib.load(model_path)

model = load_model()

# =========================
# Carregamento dos dados
# =========================
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "..", "data", "obesity.csv")
    return pd.read_csv(data_path)

df = load_data()

# =========================
# Abas
# =========================
tab1, tab2 = st.tabs(["🔍 Predição Individual", "📊 Painel Analítico"])

# ======================================================
# ABA 1 — SISTEMA PREDITIVO
# ======================================================
with tab1:
    st.header("📋 Avaliação Individual")

    gender_pt = st.selectbox("Gênero", ["Masculino", "Feminino"])
    age = st.number_input("Idade (anos)", 0, 120, 30)

    height = st.number_input(
        "Altura (metros)", 1.0, 2.5, 1.70,
        help="Altura em metros (ex.: 1.70)."
    )

    weight = st.number_input(
        "Peso (kg)", 30.0, 300.0, 70.0,
        help="Peso corporal em quilogramas."
    )

    family_history_pt = st.selectbox(
        "Histórico familiar de excesso de peso?", ["Sim", "Não"]
    )

    favc_pt = st.selectbox(
        "Consome alimentos altamente calóricos com frequência?", ["Sim", "Não"]
    )

    fcvc = st.slider(
        "Frequência de consumo de vegetais",
        1.0, 3.0, 2.0,
        help="1 = raramente | 2 = às vezes | 3 = frequentemente"
    )

    ncp = st.slider(
        "Número de refeições principais por dia",
        1.0, 4.0, 3.0,
        help="Quantidade de refeições principais realizadas por dia."
    )

    caec_pt = st.selectbox(
        "Consome alimentos entre as refeições?",
        ["Não", "Às vezes", "Frequentemente", "Sempre"]
    )

    smoke_pt = st.selectbox("Fuma?", ["Sim", "Não"])

    ch2o = st.slider(
        "Consumo diário de água",
        1.0, 3.0, 2.0,
        help="1 = < 1 litro | 2 = 1–2 litros | 3 = > 2 litros por dia"
    )

    scc_pt = st.selectbox(
        "Monitora a ingestão calórica?", ["Sim", "Não"]
    )

    faf = st.slider(
        "Frequência de atividade física",
        0.0, 3.0, 1.0,
        help="0 = nenhuma | 1 = 1–2x/sem | 2 = 2–4x/sem | 3 = >4x/sem"
    )

    tue = st.slider(
        "Tempo de uso de dispositivos tecnológicos",
        0.0, 2.0, 1.0,
        help="0 = baixo | 1 = moderado | 2 = elevado"
    )

    calc_pt = st.selectbox(
        "Frequência de consumo de álcool",
        ["Não", "Às vezes", "Frequentemente", "Sempre"]
    )

    mtrans_pt = st.selectbox(
        "Meio de transporte utilizado",
        [
            "Transporte Público",
            "Caminhada",
            "Automóvel",
            "Motocicleta",
            "Bicicleta"
        ]
    )

    if st.button("🔍 Realizar Predição"):
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

        prediction = model.predict(input_data)[0]

        st.subheader("📌 Resultado da Predição")
        st.success(f"Nível estimado de obesidade: **{prediction}**")

# ======================================================
# ABA 2 — PAINEL ANALÍTICO
# ======================================================
with tab2:
    st.header("📊 Painel Analítico — Visão Populacional")

    st.markdown(
        """
        Este painel apresenta **insights populacionais** baseados em dados históricos,
        apoiando decisões estratégicas, ações preventivas e programas educativos
        relacionados à obesidade.
        """
    )

    # DataFrame apenas para visualização
    df_panel = df.copy()
    df_panel["Nível de Obesidade"] = df_panel["Obesity"].map(obesity_map_pt)
    df_panel["Gênero"] = df_panel["Gender"].map(gender_map_pt)

    # Gráfico 1
    st.subheader("Distribuição dos níveis de obesidade")
    st.bar_chart(df_panel["Nível de Obesidade"].value_counts())

    # Gráfico 2
    st.subheader("Níveis de obesidade por gênero")
    st.bar_chart(
        df_panel
        .groupby(["Nível de Obesidade", "Gênero"])
        .size()
        .unstack()
    )

    # Gráfico 3
    st.subheader("Atividade física e níveis de obesidade")
    st.line_chart(
        df_panel
        .groupby(["FAF", "Nível de Obesidade"])
        .size()
        .unstack()
    )

    # Gráfico 4
    st.subheader("Consumo de vegetais e níveis de obesidade")
    st.line_chart(
        df_panel
        .groupby(["FCVC", "Nível de Obesidade"])
        .size()
        .unstack()
    )
