# app.py
# App de Avaliação Comportamental e Produtividade
# Stack: Streamlit + Python

import streamlit as st
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ==============================
# Configuração da página
# ==============================

st.set_page_config(
    page_title="Avaliação Comportamental",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Avaliação Comportamental e Produtividade")
st.markdown("Avaliação profissional baseada em Big Five, Estilo de Trabalho e Análise Automática.")

# ==============================
# Questionários
# ==============================

big_five_questions = {
    "Abertura": [
        "Gosto de experimentar métodos novos para resolver problemas",
        "Tenho curiosidade por temas fora da minha área"
    ],
    "Conscienciosidade": [
        "Planejo minhas tarefas antes de executá-las",
        "Cumpro prazos mesmo sob pressão"
    ],
    "Extroversão": [
        "Gosto de interagir com novas pessoas no trabalho",
        "Reuniões sociais me energizam"
    ],
    "Amabilidade": [
        "Gosto de colaborar para tomar decisões",
        "Busco manter harmonia no ambiente"
    ],
    "Estabilidade Emocional": [
        "Mantenho a calma sob pressão",
        "Lido bem com situações inesperadas"
    ]
}

work_style_questions = [
    "Organizo meu tempo por prioridades",
    "Antecipação de problemas",
    "Consigo manter foco prolongado",
    "Busco feedback frequentemente"
]

# ==============================
# Funções
# ==============================

def calculate_big_five(responses):
    return {k: float(np.mean(v)) for k, v in responses.items()}


def calculate_productivity(scores):
    return float(np.mean(scores) * 20)


def automatic_analysis(big_five):
    insights = []
    if big_five["Conscienciosidade"] >= 4:
        insights.append("Alta confiabilidade e orientação a resultados")
    if big_five["Extroversão"] < 3:
        insights.append("Perfil mais introspectivo, indicado para funções técnicas")
    if big_five["Abertura"] >= 4:
        insights.append("Alta capacidade de aprendizado e inovação")
    if big_five["Amabilidade"] >= 4:
        insights.append("Forte colaboração e trabalho em equipe")
    return insights


def radar_chart(data):
    labels = list(data.keys())
    values = list(data.values()) + [list(data.values())[0]]
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.35)
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_ylim(0, 5)
    ax.set_title("Perfil Comportamental (Big Five)")
    return fig

# ==============================
# Interface
# ==============================

responses_raw = {}

st.header("📋 Questionário de Personalidade (Big Five)")

for trait, questions in big_five_questions.items():
    st.subheader(trait)
    scores = []
    for q in questions:
        scores.append(st.slider(q, 1, 5, 3))
    responses_raw[trait] = scores

st.header("⚙️ Estilo de Trabalho & Produtividade")
work_scores = []
for q in work_style_questions:
    work_scores.append(st.slider(q, 1, 5, 3))

# ==============================
# Resultados
# ==============================

if st.button("📊 Gerar Avaliação"):
    big_five_scores = calculate_big_five(responses_raw)
    productivity = calculate_productivity(work_scores)
    insights = automatic_analysis(big_five_scores)

    st.divider()
    st.header("📈 Resultados")

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(radar_chart(big_five_scores))

    with col2:
        st.metric("Produtividade Estrutural", f"{productivity:.0f} / 100")
        if productivity >= 80:
            st.success("Alta produtividade esperada")
        elif productivity >= 60:
            st.warning("Produtividade moderada")
        else:
            st.error("Produtividade abaixo do esperado")

    st.subheader("🧠 Análise Automática")
    for i in insights:
        st.write("•", i)

    st.caption("Modelo profissional de avaliação comportamental – Big Five + Estilo de Trabalho")
