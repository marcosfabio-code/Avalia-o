# app.py
# App de Avaliação Comportamental e Produtividade
# Stack: Streamlit + Python

import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ==============================
# CONFIGURAÇÃO DA PÁGINA
# ==============================

st.set_page_config(
    page_title="Avaliação Comportamental Profissional",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Avaliação Comportamental & Produtividade")
st.caption("Modelo profissional baseado em Big Five, Estilo de Trabalho e Análise Inteligente")

st.divider()

# ==============================
# DADOS DO AVALIADO
# ==============================

with st.container():
    st.subheader("👤 Identificação do Avaliado")
    col1, col2, col3 = st.columns(3)
    with col1:
        nome = st.text_input("Nome completo")
    with col2:
        cargo = st.text_input("Cargo / Função")
    with col3:
        area = st.text_input("Área / Setor")

st.divider()

# ==============================
# QUESTIONÁRIOS
# ==============================

big_five_questions = {
    "Abertura": [
        "Gosto de experimentar novas abordagens para resolver problemas",
        "Tenho curiosidade intelectual e gosto de aprender"
    ],
    "Conscienciosidade": [
        "Planejo minhas atividades com antecedência",
        "Cumpro prazos mesmo sob pressão"
    ],
    "Extroversão": [
        "Sinto-me energizado ao interagir com pessoas",
        "Gosto de ambientes dinâmicos e colaborativos"
    ],
    "Amabilidade": [
        "Busco manter um ambiente harmonioso",
        "Tenho facilidade em cooperar com os outros"
    ],
    "Estabilidade Emocional": [
        "Mantenho a calma em situações difíceis",
        "Lido bem com mudanças inesperadas"
    ]
}

work_style_questions = [
    "Organizo meu tempo com base em prioridades",
    "Antecipação e prevenção de problemas",
    "Consigo manter foco por longos períodos",
    "Busco feedback para melhorar meu desempenho"
]

# ==============================
# FUNÇÕES
# ==============================

def calculate_big_five(responses):
    return {k: round(float(np.mean(v)), 2) for k, v in responses.items()}

def calculate_productivity(scores):
    return round(float(np.mean(scores) * 20), 1)

def generate_insights(big_five, productivity):
    insights = []

    if big_five["Conscienciosidade"] >= 4:
        insights.append("Alto nível de confiabilidade, disciplina e orientação a resultados.")

    if big_five["Abertura"] >= 4:
        insights.append("Perfil inovador, com elevada capacidade de aprendizado.")

    if big_five["Extroversão"] < 3:
        insights.append("Perfil mais analítico e introspectivo, adequado para funções técnicas ou estratégicas.")

    if big_five["Amabilidade"] >= 4:
        insights.append("Forte capacidade de colaboração e trabalho em equipe.")

    if big_five["Estabilidade Emocional"] < 3:
        insights.append("Pode apresentar sensibilidade ao estresse; recomenda-se suporte e gestão de pressão.")

    if productivity >= 80:
        insights.append("Produtividade estrutural elevada, com alta previsibilidade de entrega.")
    elif productivity >= 60:
        insights.append("Produtividade consistente, com oportunidades de otimização.")
    else:
        insights.append("Produtividade abaixo do esperado; recomenda-se intervenção gerencial.")

    return insights

def radar_chart(data):
    labels = list(data.keys())
    values = list(data.values())
    values += values[:1]

    angles = np.linspace(0, 2 * np.pi, len(labels) + 1)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.3)
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_ylim(0, 5)
    ax.set_title("Perfil Comportamental – Big Five", pad=20)

    return fig

# ==============================
# INTERFACE – QUESTIONÁRIOS
# ==============================

responses_raw = {}

st.header("📋 Questionário de Personalidade – Big Five")

for trait, questions in big_five_questions.items():
    with st.expander(trait, expanded=True):
        scores = []
        for q in questions:
            scores.append(st.slider(q, 1, 5, 3))
        responses_raw[trait] = scores

st.header("⚙️ Estilo de Trabalho & Produtividade")

work_scores = []
for q in work_style_questions:
    work_scores.append(st.slider(q, 1, 5, 3))

# ==============================
# RESULTADOS
# ==============================

if st.button("📊 Gerar Avaliação Profissional", use_container_width=True):

    big_five_scores = calculate_big_five(responses_raw)
    productivity = calculate_productivity(work_scores)
    insights = generate_insights(big_five_scores, productivity)

    st.divider()
    st.header("📈 Resultado da Avaliação")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.pyplot(radar_chart(big_five_scores))

    with col2:
        st.metric("Produtividade Estrutural", f"{productivity} / 100")

        if productivity >= 80:
            st.success("Classificação: Alta Produtividade")
        elif productivity >= 60:
            st.warning("Classificação: Produtividade Moderada")
        else:
            st.error("Classificação: Produtividade Baixa")

        st.subheader("🧠 Scores Big Five")
        for k, v in big_five_scores.items():
            st.write(f"**{k}:** {v} / 5")

    st.divider()

    st.subheader("📄 Análise Profissional Automática")
    for item in insights:
        st.write("•", item)

    st.caption(
        f"Avaliação gerada em {datetime.now().strftime('%d/%m/%Y %H:%M')} | "
        "Modelo profissional de análise comportamental"
    )
