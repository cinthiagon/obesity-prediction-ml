# 🏥 Sistema Preditivo e Analítico de Obesidade com Machine Learning

Este projeto tem como objetivo desenvolver um **sistema de apoio à decisão clínica** para auxiliar profissionais de saúde na **identificação do nível de obesidade** de um indivíduo, utilizando técnicas de **Machine Learning**.

Além da predição individual, o projeto também disponibiliza um **painel analítico populacional estratégico**, permitindo a análise de padrões e perfis relacionados à obesidade para apoiar ações preventivas e decisões executivas em saúde.

---

## 👩‍💻 Autoria

Projeto desenvolvido por:

- Cinthia Gonçalez da Silva  
- Gabriel Huzian  
- Karyne Barbosa Silva  

Projeto apresentado ao **Tech Challenge 004**  
Pós-Graduação em Data Analytics – FIAP - 2025/26

---

## 🎯 Objetivo do Projeto

- Desenvolver um modelo de **Machine Learning multiclasse** para prever o nível de obesidade  
- Criar um **sistema preditivo interativo** para uso por equipes médicas  
- Construir um **painel analítico estratégico** para análise populacional  
- Realizar o Deploy utilizando o **Streamlit**

---

## 📊 Base de Dados

O projeto utiliza o dataset `obesity.csv`, contendo informações físicas, comportamentais e de estilo de vida.

### Principais grupos de variáveis

- **Demográficas:** idade, gênero, altura, peso  
- **Hábitos alimentares:** consumo de vegetais, alimentos calóricos, refeições diárias  
- **Estilo de vida:** atividade física, consumo de água, tempo de tela  
- **Histórico:** histórico familiar de excesso de peso  
- **Variável alvo:** nível de obesidade  

---

## 🧠 Metodologia

O desenvolvimento seguiu uma pipeline completa de Machine Learning:

1. Análise Exploratória de Dados (EDA)  
2. Pré-processamento  
   - One-Hot Encoding  
   - StandardScaler  
3. Construção de Pipeline com `ColumnTransformer`  
4. Treinamento e comparação de modelos  
5. Avaliação com métricas por classe  
6. Seleção do modelo final  
7. Serialização do modelo (.pkl)  
8. Deploy via API Flask  
9. Integração com interface Streamlit  
10. Conteinerização com Docker  

---

## 🤖 Modelos Avaliados

- Regressão Logística (baseline)  
- Random Forest  
- Gradient Boosting (**modelo final selecionado**)  

### Critérios de Escolha

- Acurácia global  
- Precision, Recall e F1-score por classe  
- Macro e Weighted average  
- Equilíbrio entre classes  
- Capacidade de generalização  

**Acurácia final do modelo escolhido: ~95%**

---

# 🏗 Arquitetura da Solução

A aplicação foi estruturada em arquitetura de microsserviços:

[ Streamlit Dashboard ] ---> [ API Flask ] ---> [ Modelo ML (.pkl) ]


### Componentes:

- **API Flask** → Responsável pela inferência do modelo  
- **Streamlit** → Interface preditiva + painel analítico  
- **Docker** → Conteinerização completa  
- **Render** → Deploy em nuvem  

---

## 🌐 Deploy em Produção

### 🔹 API (Backend)

https://obesity-prediction-ml-1sl8.onrender.com

### 🔹 Dashboard (Frontend)

https://obesity-dahboard.onrender.com/

> ⚠️ Observação: Em função do plano gratuito do Render, podem ocorrer limitações temporárias de requisições (erro 429) ou pequenos atrasos no primeiro acesso (cold start).

---

# 📊 Painel Analítico Estratégico

O dashboard inclui:

- Segmentação por gênero e faixa etária  
- Cálculo de IMC médio por grupo  
- Score comportamental de risco  
- Análise de hábitos alimentares  
- Análise de estilo de vida  
- Relação entre variáveis e níveis de obesidade  
- Visualizações explicativas para equipe médica  

Todos os gráficos possuem título e contextualização clínica.

---

# 🐳 Conteinerização

A aplicação foi totalmente conteinerizada utilizando Docker.

## Estrutura do Projeto

obesity-project/
│
├── api/
│ ├── app.py
│ ├── obesity_model.pkl
│ ├── Dockerfile
│ └── requirements.txt
│
├── app/
│ ├── app.py
│ ├── obesity.csv
│ ├── Dockerfile
│ └── requirements.txt
│
├── notebooks/
│ └── 01_eda_obesity.ipynb
│
├── docker-compose.yml
├── .gitignore
└── README.md


---

# ▶️ Executar Localmente com Docker

```bash
docker-compose build
docker-compose up
