# 🏥 Sistema Preditivo e Analítico de Obesidade com Machine Learning

Este projeto tem como objetivo desenvolver um **sistema de apoio à decisão clínica** para auxiliar profissionais de saúde na **identificação do nível de obesidade** de um indivíduo, utilizando técnicas de **Machine Learning**.

Além da predição individual, o projeto também disponibiliza um **painel analítico populacional**, permitindo a análise de padrões e perfis relacionados à obesidade para apoiar ações preventivas e estratégicas em saúde.

---

## 👩‍💻 Autoria

Projeto desenvolvido por:

- Cinthia Gonçalez da Silva
- Gabriel Huzian
- Karyne Barbosa Silva

Projeto apresentado ao Tech Challenge 004 da Pós-Graduação em Data Analytics da FIAP.

---

## 🎯 Objetivo do Projeto

- Desenvolver um **modelo de Machine Learning** capaz de prever o nível de obesidade de um indivíduo  
- Criar um **sistema preditivo interativo** para uso por equipes médicas  
- Disponibilizar uma **visão analítica dos dados históricos** para geração de insights  
- Garantir uma solução **reprodutível, interpretável e orientada ao negócio**

---

## 📊 Base de Dados

O projeto utiliza o dataset `obesity.csv`, que contém informações físicas, comportamentais e de hábitos de vida.

### Principais variáveis
- **Demográficas:** idade, gênero, altura, peso  
- **Hábitos alimentares:** consumo de vegetais, alimentos calóricos, refeições diárias  
- **Estilo de vida:** atividade física, consumo de água, uso de tecnologia  
- **Histórico:** histórico familiar de excesso de peso  
- **Variável alvo:** nível de obesidade  

---

## 🧠 Metodologia

O desenvolvimento do projeto seguiu todas as etapas de uma **pipeline completa de Machine Learning**:

1. Análise Exploratória de Dados (EDA)  
2. Pré-processamento e feature engineering  
   - One-Hot Encoding para variáveis categóricas  
   - StandardScaler para variáveis numéricas  
3. Construção de pipelines de Machine Learning  
4. Treinamento e comparação de modelos  
5. Avaliação com métricas por classe (precision, recall e F1-score)  
6. Seleção do modelo final  
7. Deploy do sistema preditivo  
8. Construção do painel analítico  

---

## 🤖 Modelos Avaliados

Os seguintes modelos foram treinados e comparados:

- Regressão Logística (baseline)  
- Random Forest  
- Gradient Boosting (**modelo final escolhido**)  

### Critérios de escolha
- Acurácia global  
- Recall e F1-score por classe  
- Equilíbrio entre classes  
- Capacidade de generalização  
- Adequação ao contexto de saúde  

**Acurácia final do modelo escolhido:** ~95%

---

## 📌 Sistema Preditivo

O sistema permite que profissionais de saúde insiram informações de um indivíduo e obtenham uma **estimativa do nível de obesidade**.

### Características
- Interface 100% em português  
- Escalas explicadas diretamente na aplicação  
- Mapeamento PT → EN preservando o modelo treinado  
- Resultado apresentado como **apoio à decisão clínica**

---

## 📊 Painel Analítico

O painel analítico oferece uma **visão populacional dos dados**, permitindo:

- Visualizar a distribuição dos níveis de obesidade  
- Analisar diferenças por gênero  
- Avaliar a relação entre atividade física e obesidade  
- Avaliar a relação entre hábitos alimentares e obesidade  

Todos os rótulos e gráficos são apresentados em **português**, facilitando a interpretação por equipes médicas.

---

## 🌐 Aplicação Online (Deploy)

A aplicação foi implantada no **Streamlit Cloud** e está disponível publicamente no link abaixo:

https://obesity-prediction-ml-fiap-tech-004.streamlit.app/

---

## 📂 Estrutura do Projeto

```text
obesity-project/
│
├── app/
│   └── app.py               # Aplicação Streamlit (predição + painel)
│
├── data/
│   └── obesity.csv          # Base de dados
│
├── models/
│   └── obesity_model.pkl    # Modelo treinado
│
├── notebooks/
│   └── 01_eda_obesity.ipynb # Análise exploratória e modelagem
│
├── requirements.txt         # Dependências do projeto
├── .gitignore
└── README.md 
```
---

## ▶️ Como Executar Localmente

1. Clonar o repositório:
```text
git clone https://github.com/cinthiagon/obesity-prediction-ml.git
cd obesity-project
```
<br>

2. Criar e ativar o ambiente virtual:
```text
python -m venv venv
source venv/bin/activate  # Linux/macOS 
venv\Scripts\activate`     # Windows
```
<br>

3. Instalar Dependências:
``` text
pip install -r requirements.txt
```
<br>
   
4. Executar a aplicação: 
```text
python -m streamlit run app/app.py
```
---

## ⚠️ Aviso Importante

Este sistema não substitui avaliação médica profissional.
Os resultados devem ser utilizados exclusivamente como apoio à decisão clínica.
