# app.py
# Plataforma Profissional de Avaliação Comportamental Multimodelo
# Big Five | HEXACO | DISC | MBTI | Produtividade

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Avaliação Comportamental Multimodelo",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Avaliação Comportamental Multimodelo")
st.caption("Big Five • HEXACO • DISC • MBTI • Produtividade")

# ==================================================
# QUESTIONÁRIOS
# ==================================================

BIG_FIVE = {
    "Abertura": [
        "Gosto de explorar novas ideias",
        "Sou curioso intelectualmente",
        "Busco soluções criativas",
        "Tenho interesse por inovação"
    ],
    "Conscienciosidade": [
        "Planejo antes de agir",
        "Cumpro prazos rigorosamente",
        "Sou disciplinado",
        "Mantenho organização"
    ],
    "Extroversão": [
        "Gosto de interações sociais",
        "Falo com facilidade",
        "Sinto-me energizado em grupo",
        "Assumo protagonismo"
    ],
    "Amabilidade": [
        "Busco harmonia",
        "Tenho empatia",
        "Coopero com facilidade",
        "Evito conflitos"
    ],
    "Estabilidade Emocional": [
        "Mantenho calma sob pressão",
        "Lido bem com estresse",
        "Sou emocionalmente estável",
        "Recupero-me rápido de frustrações"
    ]
}

HEXACO_H = [
    "Evito tirar vantagem dos outros",
    "Sou honesto mesmo sem supervisão",
    "Não manipulo pessoas para benefício próprio",
    "Valorizo justiça acima de ganhos pessoais"
]

DISC_QUESTIONS = {
    "Dominance": [
        "Tomo decisões rápidas",
        "Assumo riscos com facilidade"
    ],
    "Influence": [
        "Convenço pessoas com facilidade",
        "Gosto de inspirar os outros"
    ],
    "Steadiness": [
        "Sou paciente",
        "Prefiro estabilidade"
    ],
    "Compliance": [
        "Sigo regras rigorosamente",
        "Valorizo processos claros"
    ]
}

MBTI_QUESTIONS = {
    "EI": [
        "Prefiro falar do que ouvir",
        "Ganho energia com pessoas"
    ],
    "SN": [
        "Foco mais em possibilidades do que em fatos",
        "Gosto de pensar no futuro"
    ],
    "TF": [
        "Decido mais pela lógica que emoção",
        "Prioritizo justiça à empatia"
    ],
    "JP": [
        "Prefiro planejamento a improviso",
        "Gosto de decisões fechadas"
    ]
}

WORK_STYLE = [
    "Organizo meu tempo por prioridades",
    "Antevejo problemas",
    "Mantenho foco prolongado",
    "Busco feedback constantemente",
    "Sou consistente na entrega",
    "Executo com eficiência"
]

# ==================================================
# FUNÇÕES DE CÁLCULO
# ==================================================

def mean_score(values):
    return round(float(np.mean(values)), 2)

def calculate_big_five(resp):
    return {k: mean_score(v) for k, v in resp.items()}

def calculate_hexaco(h_scores):
    return mean_score(h_scores)

def calculate_productivity(scores):
    return round(np.mean(scores) * 20, 1)

def calculate_disc(disc_raw):
    return {k: mean_score(v) for k, v in disc_raw.items()}

def calculate_mbti(mbti_raw):
    result = ""
    result += "E" if mean_score(mbti_raw["EI"]) >= 3 else "I"
    result += "N" if mean_score(mbti_raw["SN"]) >= 3 else "S"
    result += "T" if mean_score(mbti_raw["TF"]) >= 3 else "F"
    result += "J" if mean_score(mbti_raw["JP"]) >= 3 else "P"
    return result

def radar(data, title):
    labels = list(data.keys())
    values = list(data.values()) + [list(data.values())[0]]
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1)

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.3)
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_ylim(0, 5)
    ax.set_title(title)
    return fig

# ==================================================
# INTERFACE
# ==================================================

st.header("📋 Questionário")

responses_bigfive = {}
for trait, qs in BIG_FIVE.items():
    with st.expander(trait, True):
        responses_bigfive[trait] = [st.slider(q, 1, 5, 3) for q in qs]

st.subheader("🧭 Honestidade & Humildade (HEXACO)")
hexaco_scores = [st.slider(q, 1, 5, 3) for q in HEXACO_H]

st.subheader("🎯 DISC")
disc_raw = {}
for d, qs in DISC_QUESTIONS.items():
    disc_raw[d] = [st.slider(q, 1, 5, 3) for q in qs]

st.subheader("🧩 MBTI")
mbti_raw = {}
for k, qs in MBTI_QUESTIONS.items():
    mbti_raw[k] = [st.slider(q, 1, 5, 3) for q in qs]

st.subheader("⚙️ Estilo de Trabalho")
work_scores = [st.slider(q, 1, 5, 3) for q in WORK_STYLE]

# ==================================================
# RESULTADOS
# ==================================================

if st.button("📊 Gerar Avaliação Completa", use_container_width=True):

    bigfive = calculate_big_five(responses_bigfive)
    hexaco = calculate_hexaco(hexaco_scores)
    disc = calculate_disc(disc_raw)
    mbti = calculate_mbti(mbti_raw)
    productivity = calculate_productivity(work_scores)

    st.divider()
    st.header("📈 Resultados")

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(radar(bigfive, "Big Five"))
    with col2:
        st.metric("Produtividade Estrutural", f"{productivity}/100")
        st.metric("Honestidade-Humildade (HEXACO)", f"{hexaco}/5")
        st.metric("Perfil MBTI (Interpretativo)", mbti)

    st.subheader("🎯 DISC")
    for k, v in disc.items():
        st.write(f"**{k}:** {v}/5")

    st.caption(
        f"Avaliação gerada em {datetime.now().strftime('%d/%m/%Y %H:%M')} • "
        "Modelo Multimodelo Profissional"
    )
