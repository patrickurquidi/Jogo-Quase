import streamlit as st
import time
import random
import json
import os

st.set_page_config(page_title="QUASE", layout="centered")

SAVE_FILE = "record.json"

def load_record():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f).get("best", 0.0)
    return 0.0

def save_record(value):
    with open(SAVE_FILE, "w") as f:
        json.dump({"best": value}, f)

# Estado
if "position" not in st.session_state:
    st.session_state.position = 0.0
    st.session_state.running = False
    st.session_state.start_time = time.time()
    st.session_state.speed = random.uniform(0.3, 0.8)
    st.session_state.attempts = 0
    st.session_state.best = load_record()

st.title("🎯 QUASE")
st.write("Chegue o mais perto possível do centro.")

# Alvo invisível após 10 tentativas
show_target = st.session_state.attempts < 10
target = 0.5

progress = st.session_state.position
st.progress(progress)

if st.session_state.running:
    elapsed = time.time() - st.session_state.start_time
    st.session_state.position = abs((elapsed * st.session_state.speed) % 1)

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Começar"):
        st.session_state.running = True
        st.session_state.start_time = time.time()
        st.session_state.speed = random.uniform(0.3, 0.9)

with col2:
    if st.button("⏹️ Parar"):
        st.session_state.running = False
        st.session_state.attempts += 1

        distance = abs(st.session_state.position - target)
        score = max(0, 100 - distance * 200)

        if score > st.session_state.best:
            st.session_state.best = score
            save_record(score)

        st.subheader(f"Quase: {score:.2f}%")
        st.write(f"Melhor de todos os tempos: {st.session_state.best:.2f}%")

        # Linguagem emocional
        if score >= 99:
            st.write("")
        elif score >= 95:
            st.write("Você sentiu o centro.")
        elif score >= 90:
            st.write("Foi por muito pouco.")
        elif score >= 80:
            st.write("Chegou perto.")
        else:
            st.write("Dá pra chegar mais.")

        st.session_state.position = 0.0
