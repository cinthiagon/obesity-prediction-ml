# =========================
#A aplicação preditiva foi desenvolvida com foco em usabilidade clínica, 
# apresentando interface em português e explicações claras sobre as escalas e unidades de cada variável utilizada. 
# Para preservar a consistência do modelo treinado, foi implementada uma camada de mapeamento entre as respostas do usuário 
# e as categorias originais do modelo, garantindo clareza para o usuário final sem impacto na performance preditiva.
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

st.title("🏥 Sistema Preditivo de Obesidade")
st.write(
    """
    Esta aplicação utiliza **Machine Learning** para **auxiliar profissionais de saúde**
    na identificação do nível de obesidade de um indivíduo.

    ⚠️ **Aviso importante:** o resultado apresentado é apenas um **apoio à decisão clínica**
    e **não substitui** avaliação médica profissional.
    """
)

# =========================
# Mapas de tradução PT -> EN
# =========================
yes_no_map = {
    "Sim": "yes",
    "Não": "no"
}

gender_map = {
    "Masculino": "Male",
    "Feminino": "Female"
}

caec_map = {
    "Não": "no",
    "Às vezes": "Sometimes",
    "Frequentemente": "Frequently",
    "Sempre": "Always"
}

calc_map = {
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
# Inputs do usuário
# =========================
st.header("📋 Informações do Paciente")

gender_pt = st.selectbox(
    "Gênero",
    ["Masculino", "Feminino"]
)

age = st.number_input(
    "Idade (anos)",
    min_value=0,
    max_value=120,
    value=30
)

height = st.number_input(
    "Altura (metros)",
    min_value=1.0,
    max_value=2.5,
    value=1.70,
    help="Altura do paciente em metros (ex.: 1.70)."
)

weight = st.number_input(
    "Peso (kg)",
    min_value=30.0,
    max_value=300.0,
    value=70.0,
    help="Peso corporal em quilogramas."
)

family_history_pt = st.selectbox(
    "Histórico familiar de excesso de peso?",
    ["Sim", "Não"]
)

favc_pt = st.selectbox(
    "Consome alimentos altamente calóricos com frequência?",
    ["Sim", "Não"]
)

fcvc = st.slider(
    "Frequência de consumo de vegetais",
    min_value=1.0,
    max_value=3.0,
    value=2.0,
    help="""
    Escala de frequência:
    1 = raramente  
    2 = às vezes  
    3 = frequentemente
    """
)

ncp = st.slider(
    "Número de refeições principais por dia",
    min_value=1.0,
    max_value=4.0,
    value=3.0,
    help="Quantidade de refeições principais realizadas ao longo do dia."
)

caec_pt = st.selectbox(
    "Consome alimentos entre as refeições?",
    ["Não", "Às vezes", "Frequentemente", "Sempre"]
)

smoke_pt = st.selectbox(
    "Fuma?",
    ["Sim", "Não"]
)

ch2o = st.slider(
    "Consumo diário de água",
    min_value=1.0,
    max_value=3.0,
    value=2.0,
    help="""
    Escala aproximada de consumo:
    1 = menos de 1 litro/dia  
    2 = entre 1 e 2 litros/dia  
    3 = mais de 2 litros/dia
    """
)

scc_pt = st.selectbox(
    "Monitora a ingestão calórica?",
    ["Sim", "Não"]
)

faf = st.slider(
    "Frequência de atividade física",
    min_value=0.0,
    max_value=3.0,
    value=1.0,
    help="""
    Frequência semanal:
    0 = nenhuma  
    1 = 1–2 vezes/semana  
    2 = 2–4 vezes/semana  
    3 = mais de 4 vezes/semana
    """
)

tue = st.slider(
    "Tempo de uso de dispositivos tecnológicos",
    min_value=0.0,
    max_value=2.0,
    value=1.0,
    help="""
    Escala de uso diário:
    0 = baixo  
    1 = moderado  
    2 = elevado
    """
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

# =========================
# Predição
# =========================
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
