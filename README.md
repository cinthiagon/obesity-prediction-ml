# 🏥 Sistema Estratégico de Predição de Obesidade  
### Tech Challenge 004 – Pós-Graduação em Data Analytics – FIAP

Projeto desenvolvido com foco em aplicabilidade executiva no contexto hospitalar, integrando Machine Learning, API REST, containerização e dashboard analítico para apoio à decisão clínica.

---

## 👩‍💻 Autoria

- **Cinthia Gonçalez da Silva**  
- **Gabriel Huzian**  
- **Karyne Barbosa Silva**

Projeto apresentado ao **Tech Challenge 004 da Pós-Graduação em Data Analytics da FIAP - 2025/2026**.

---

# 🎯 Objetivo do Projeto

Desenvolver um sistema inteligente capaz de:

- Predizer o nível de obesidade de um paciente com base em variáveis clínicas e comportamentais.
- Fornecer suporte à decisão médica individual.
- Gerar insights populacionais estratégicos para a equipe de saúde.
- Demonstrar pipeline completa de Machine Learning e arquitetura fullstack desacoplada.

---

# ✅ Atendimento aos Requisitos do Tech Challenge

## ✔ 1. Pipeline Completa de Machine Learning

A solução contempla todas as etapas da pipeline:

- Análise exploratória de dados (EDA)
- Tratamento e limpeza
- Feature Engineering
- Codificação de variáveis categóricas (One Hot Encoding)
- Padronização (StandardScaler)
- Separação treino/teste
- Treinamento de múltiplos modelos
- Avaliação com métricas detalhadas
- Seleção do melhor modelo
- Serialização com `joblib`

Notebook disponível em:
`notebooks/`


---

## ✔ 2. Modelo com Assertividade > 75%

Modelo selecionado: **Gradient Boosting**

Resultados obtidos:

- 🎯 Acurácia: ~95%
- 📊 Precision, Recall e F1-score avaliados por classe
- ⚖️ Equilíbrio entre generalização e robustez

---

## ✔ 3. Deploy do Modelo em Aplicação Preditiva (Streamlit)

A aplicação preditiva foi implementada em duas arquiteturas distintas:

---

### 🔹 🔹 Versão 1 — Standalone (Modelo Carregado Localmente)

Aplicação Streamlit que carrega diretamente o modelo `.pkl`, sem dependência de API externa.

🔗 **Link da aplicação Standalone:**  
https://obesity-prediction-ml.streamlit.app/

Essa versão garante:

- Maior estabilidade em ambientes gratuitos
- Simplicidade arquitetural
- Ideal para demonstração acadêmica

---

### 🔹 🔹 Versão 2 — Arquitetura Completa (Frontend + API)

Arquitetura desacoplada, simulando ambiente corporativo real.

#### 🔹 Frontend (Streamlit Cloud)
Interface interativa + dashboard analítico  
Consome API REST

🔗 **Frontend:**  
https://obesity-prediction-ml-fiap-main.streamlit.app/

#### 🔹 API (Render)
Carrega modelo treinado e expõe endpoints REST

🔗 **API:**  
https://obesity-api-2uun.onrender.com/

Endpoints disponíveis:

- `GET /` → Status da API  
- `POST /predict` → Predição individual  
- `GET /data` → Dataset para dashboard  

---

## ✔ 4. Construção de Painel Analítico com Insights Estratégicos

O dashboard inclui:

- Distribuição por nível de obesidade
- IMC médio por grupo
- Histórico familiar
- Consumo de vegetais
- Consumo de alimentos calóricos
- Consumo de água
- Consumo de álcool
- Número de refeições
- Atividade física
- Tempo de tela
- Meio de transporte
- Segmentação por faixa etária
- Segmentação por gênero

### 🎯 Visão de Negócio

O painel permite à equipe médica:

- Identificar padrões comportamentais
- Avaliar fatores de risco populacionais
- Mapear perfis críticos
- Apoiar decisões preventivas
- Direcionar campanhas de intervenção

---

## ✔ 5. Links para Entrega

### 🔹 Aplicação Standalone (Streamlit Cloud)
https://obesity-prediction-ml.streamlit.app/

### 🔹 Aplicação Frontend (Arquitetura Completa)
https://obesity-prediction-ml-fiap-main.streamlit.app/

### 🔹 API (Render)
https://obesity-api-2uun.onrender.com/

### 🔹 Repositório GitHub
https://github.com/cinthiagon/obesity-prediction-ml

---

## ✔ 6. Gravação do Vídeo (4–10 minutos)

O vídeo contempla:

- Estratégia de modelagem
- Justificativa da escolha do modelo
- Pipeline completa de ML
- Arquitetura da solução
- Demonstração da API
- Demonstração da aplicação preditiva
- Exploração do dashboard analítico
- Apresentação sob visão executiva hospitalar

---

# 🏗 Arquitetura da Solução

### 🔹 Versão Standalone
`Streamlit → Modelo (.pkl)`


### 🔹 Versão Completa
``` 
Streamlit (Frontend)
↓
API Flask (Render)
↓
Modelo Gradient Boosting (.pkl) 
```

Arquitetura desacoplada, escalável e alinhada a padrões de mercado.

---

# 🐳 Execução Local com Docker

Para rodar localmente:

```bash
docker-compose up --build
``` 

Serviços:

API → http://localhost:5000
Frontend → http://localhost:8501

---
# 📁 Estrutura do Projeto

```
obesity-project/
│
├── api/
│   ├── api.py
│   ├── obesity_model.pkl
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   ├── obesity.csv
│   └── requirements.txt
│
├── notebooks/
│   └── model_training.ipynb
│
├── docker-compose.yml
├── README.md
└── requirements.txt
```

---

# 📌 Considerações Finais

O projeto atende os critérios do Tech Challenge 004, demonstrando não apenas capacidade técnica em Machine Learning, mas também maturidade arquitetural, visão executiva e aplicabilidade real no contexto hospitalar.
