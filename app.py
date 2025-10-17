
import streamlit as st
import random
import sqlite3
from datetime import datetime
import json

DB_PATH = "ket_practice.db"

# -------------------------
# Database helpers
# -------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            details TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_result(student_name, topic, score, total, details):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO results (student_name, topic, score, total, details, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (student_name, topic, score, total, json.dumps(details, ensure_ascii=False), datetime.now().isoformat(timespec="seconds"))
    )
    conn.commit()
    conn.close()

def load_results(student_name=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if student_name:
        c.execute("SELECT student_name, topic, score, total, created_at FROM results WHERE student_name = ? ORDER BY id DESC", (student_name,))
    else:
        c.execute("SELECT student_name, topic, score, total, created_at FROM results ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# -------------------------
# Content: Present Perfect (KET-friendly)
# -------------------------
EXPLANATION_MD = """
# Present Perfect (nivel KET, sexto de primaria)

**Estructura básica:** `have/has + participio pasado`  
- I/you/we/they **have** + V3 → *I have finished.*  
- He/she/it **has** + V3 → *She has finished.*

**Usos principales (lo que debes saber para KET):**
1. **Experiencias de vida** (sin decir *cuándo*) — *Have you ever…?* / *I have never…*  
   - *Have you ever eaten sushi?* → ¿Alguna vez has comido sushi?  
   - *I have never been to London.* → Nunca he estado en Londres.

2. **Resultados recientes** (importa el **resultado ahora**). Palabras: **just**, **already**, **yet**  
   - *I have just finished my homework.* (just = hace un momento)  
   - *She has already eaten.* (already = ya)  
   - *Have you finished yet?* / *I haven’t finished yet.* (yet = ya/todavía no en preguntas/negativas)

3. **Tiempo no terminado** con **for**/**since** (duración/comienzo)  
   - *I have lived here **for** three years.* (for = duración)  
   - *He has worked here **since** 2022.* (since = desde un punto en el tiempo)

4. **Preguntas y negativas**  
   - **Pregunta:** *Have/Has + sujeto + V3?* → *Have they arrived?*  
   - **Negativa:** *haven’t/hasn’t + V3* → *She hasn’t finished.*

**Participios regulares:** `-ed` (work → worked).  
**Participios irregulares** (V3): be–**been**, go–**gone**, do–**done**, eat–**eaten**, make–**made**, take–**taken**, see–**seen**, write–**written**, have–**had**, say–**said**, know–**known**, give–**given**, come–**come**, become–**become**, buy–**bought**, think–**thought**, tell–**told**, leave–**left**, feel–**felt**.

> **Regla clave KET:** Si dices **cuándo** (ayer, en 2023, last week), usa **Past Simple**.  
> Si importa la **experiencia/resultado presente** y **no dices cuándo**, usa **Present Perfect**.
"""

IRREGULARS = {
    "be": "been", "go": "gone", "do": "done", "eat": "eaten", "make": "made",
    "take": "taken", "see": "seen", "write": "written", "have": "had",
    "say": "said", "know": "known", "give": "given", "come": "come",
    "become": "become", "buy": "bought", "think": "thought", "tell": "told",
    "leave": "left", "feel": "felt"
}

SUBJECTS_3SG = ["He", "She", "It", "My friend", "The teacher", "Ana"]
SUBJECTS_PL = ["I", "You", "We", "They", "My parents", "The students"]

# -------------------------
# Item generators per topic
# -------------------------
def gen_aux_agreement_item():
    subject = random.choice(SUBJECTS_3SG + SUBJECTS_PL)
    is_3sg = subject in SUBJECTS_3SG
    base, part = random.choice(list(IRREGULARS.items()))
    options_aux = ["has", "have"]
    correct_aux = "has" if is_3sg else "have"
    stem = f"{subject} ___ {part} (choose the correct auxiliary)."
    return {
        "type": "mcq",
        "topic": "Aux/Participio",
        "stem": stem,
        "options": options_aux,
        "answer": correct_aux,
        "explanation": f"Con {subject} se usa **{'has' if is_3sg else 'have'}** + participio: *{subject} {correct_aux} {part}.*"
    }

def gen_participle_fill_item():
    base, part = random.choice(list(IRREGULARS.items()))
    subject = random.choice(SUBJECTS_3SG + SUBJECTS_PL)
    is_3sg = subject in SUBJECTS_3SG
    aux = "has" if is_3sg else "have"
    stem = f"Completa con el **participio** de **{base}**: “{subject} {aux} ___.”"
    return {
        "type": "fill",
        "topic": "Participios irregulares",
        "stem": stem,
        "answer": part,
        "explanation": f"El participio (V3) de **{base}** es **{part}**."
    }

def gen_ever_never_item():
    subject = random.choice(SUBJECTS_PL + SUBJECTS_3SG)
    is_3sg = subject in SUBJECTS_3SG
    aux = "has" if is_3sg else "have"
    base, part = random.choice(list(IRREGULARS.items()))
    stem = f"Elige **ever** o **never**: “{subject} {aux} ___ {part} sushi.”"
    options = ["ever", "never"]
    correct = random.choice(options)
    explanation = ("**ever** se usa en preguntas/experiencias; **never** = nunca (afirmación negativa). "
                   f"Ambas van con Present Perfect: *{subject} {aux} {correct} {part} sushi.*")
    return {
        "type": "mcq",
        "topic": "Ever/Never (experiencias)",
        "stem": stem,
        "options": options,
        "answer": correct,
        "explanation": explanation
    }

def gen_already_yet_just_item():
    subject = random.choice(SUBJECTS_PL + SUBJECTS_3SG)
    is_3sg = subject in SUBJECTS_3SG
    aux = "has" if is_3sg else "have"
    base, part = random.choice(list(IRREGULARS.items()))
    pattern = random.choice(["affirm", "question", "negative"])
    if pattern == "affirm":
        options = ["already", "just"]
        correct = random.choice(options)
        stem = f"Elige **already** o **just**: “{subject} {aux} ___ {part} the homework.”"
        expl = "**already** = ya; **just** = hace un momento. Ambos van antes del participio en afirmaciones."
    elif pattern == "question":
        options = ["already", "yet", "just"]
        correct = "already"
        stem = f"Elige la mejor opción: “{aux.capitalize()} {subject.lower()} ___ finished?”"
        expl = "**already** se usa en preguntas para sorprenderse de que algo esté hecho; **yet** va al final (*...finished yet?*)."
    else:
        options = ["already", "yet", "just"]
        correct = "yet"
        stem = f"Elige la mejor opción: “{subject} {aux} not finished ___.”"
        expl = "**yet** se usa en negativas y va al final: *haven’t/hasn’t finished yet*."
    return {
        "type": "mcq",
        "topic": "Already/Yet/Just (resultado)",
        "stem": stem,
        "options": options,
        "answer": correct,
        "explanation": expl
    }

def gen_for_since_item():
    subject = random.choice(SUBJECTS_PL + SUBJECTS_3SG)
    is_3sg = subject in SUBJECTS_3SG
    aux = "has" if is_3sg else "have"
    base = random.choice(["live", "work", "study", "play", "know"])
    part = base + "ed" if base != "know" else "known"
    if random.random() < 0.5:
        duration = random.choice(["three years", "a long time", "two weeks", "ten minutes"])
        stem = f"Elige **for** o **since**: “{subject} {aux} {part} ___ {duration}.”"
        correct = "for"
        expl = "**for** = durante (duración). **since** = desde (punto inicial)."
    else:
        start = random.choice(["2022", "last Monday", "January", "8 o’clock"])
        stem = f"Elige **for** o **since**: “{subject} {aux} {part} ___ {start}.”"
        correct = "since"
        expl = "**since** introduce un **punto** de inicio en el tiempo."
    return {
        "type": "mcq",
        "topic": "For/Since (tiempo no terminado)",
        "stem": stem,
        "options": ["for", "since"],
        "answer": correct,
        "explanation": expl
    }

def gen_question_order_item():
    subject = random.choice(SUBJECTS_PL + SUBJECTS_3SG)
    is_3sg = subject in SUBJECTS_3SG
    aux = "Has" if is_3sg else "Have"
    base, part = random.choice(list(IRREGULARS.items()))
    options = [
        f"{aux} {subject.lower()} {part}?",
        f"{subject} {aux.lower()} {part}?",
        f"{aux} {part} {subject.lower()}?"
    ]
    correct = options[0]
    stem = "Elige el **orden correcto** para la **pregunta** (Present Perfect):"
    return {
        "type": "mcq",
        "topic": "Preguntas (orden)",
        "stem": stem + f" {subject} / {aux.lower()} / {part}",
        "options": options,
        "answer": correct,
        "explanation": "Pregunta = **Have/Has + sujeto + participio**."
    }

TOPIC_GENERATORS = {
    "Aux/Participio": [gen_aux_agreement_item],
    "Participios irregulares": [gen_participle_fill_item],
    "Ever/Never (experiencias)": [gen_ever_never_item],
    "Already/Yet/Just (resultado)": [gen_already_yet_just_item],
    "For/Since (tiempo no terminado)": [gen_for_since_item],
    "Preguntas (orden)": [gen_question_order_item],
}
ALL_TOPICS = list(TOPIC_GENERATORS.keys())
ALL_TOPICS_WITH_MIXED = ["Mixto"] + ALL_TOPICS

def build_quiz(topic, n_items):
    gens = []
    if topic == "Mixto":
        for _ in range(n_items):
            t = random.choice(ALL_TOPICS)
            gens.append(random.choice(TOPIC_GENERATORS[t]))
    else:
        gens = [random.choice(TOPIC_GENERATORS[topic]) for _ in range(n_items)]
    items = [g() for g in gens]
    return items

def grade_quiz(items, user_answers):
    score = 0
    details = []
    for i, item in enumerate(items):
        ua = user_answers.get(str(i), "").strip()
        correct = item["answer"]
        is_correct = (ua.lower() == str(correct).lower())
        if item["type"] == "fill":
            is_correct = ua.lower() == correct.lower()
        if is_correct:
            score += 1
        details.append({
            "stem": item["stem"],
            "your_answer": ua,
            "correct": correct,
            "explanation": item["explanation"],
            "result": "correct" if is_correct else "incorrect"
        })
    return score, details

def main():
    st.set_page_config(page_title="KET: Present Perfect Trainer", page_icon="✅")
    init_db()

    st.sidebar.title("Configuración")
    student_name = st.sidebar.text_input("Nombre del alumno", help="Se usará para guardar tus resultados.")
    topic = st.sidebar.selectbox("Tema", ALL_TOPICS_WITH_MIXED, index=0)
    n_items = st.sidebar.slider("Número de ejercicios", 5, 20, 10, 1)
    st.sidebar.write("---")
    show_history = st.sidebar.checkbox("Ver historial", value=False)

    st.title("KET: Entrenador de Present Perfect")
    st.caption("Hecho con ❤️ en Streamlit — Practica con ejercicios aleatorios y guarda tus puntajes por tema.")

    with st.expander("Explicación rápida (lo esencial para KET)", expanded=True):
        st.markdown(EXPLANATION_MD)

    # ⚠️ Use a key name that doesn't clash with SessionState.items() method
    if "quiz_items" not in st.session_state:
        st.session_state["quiz_items"] = []
        st.session_state["topic_used"] = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Generar ejercicios"):
            st.session_state["quiz_items"] = build_quiz(topic, n_items)
            st.session_state["topic_used"] = topic

    with col2:
        if st.button("🧹 Limpiar / nuevo intento"):
            st.session_state["quiz_items"] = []
            st.session_state["topic_used"] = None

    if st.session_state["quiz_items"]:
        st.subheader(f"Ejercicios: {st.session_state['topic_used']} ({len(st.session_state['quiz_items'])})")

        ans = {}
        for i, item in enumerate(st.session_state["quiz_items"]):
            st.write(f"**{i+1}.** {item['stem']}")
            if item["type"] == "mcq":
                ans[str(i)] = st.radio("Selecciona una opción:", item["options"], key=f"q_{i}", index=0, label_visibility="collapsed")
            elif item["type"] == "fill":
                ans[str(i)] = st.text_input("Escribe tu respuesta:", key=f"q_{i}", label_visibility="collapsed")
            st.divider()

        if st.button("✅ Calificar y guardar puntaje"):
            if not student_name:
                st.error("Por favor escribe el **nombre del alumno** en la barra lateral para guardar el resultado.")
            else:
                score, details = grade_quiz(st.session_state["quiz_items"], ans)
                total = len(st.session_state["quiz_items"])
                st.success(f"Tu puntaje: **{score}/{total}**")
                with st.expander("Ver respuestas y explicaciones"):
                    for d in details:
                        st.write(f"- **Enunciado:** {d['stem']}")
                        st.write(f"  - Tu respuesta: `{d['your_answer']}`")
                        st.write(f"  - Correcta: `{d['correct']}`")
                        st.write(f"  - Explicación: {d['explanation']}")
                        st.write(f"  - Resultado: **{d['result']}**")
                        st.write("---")

                save_result(student_name, st.session_state["topic_used"], score, total, details)

    if show_history:
        st.subheader("Historial de puntajes")
        rows = load_results(student_name if student_name else None)
        if rows:
            st.write("| Alumno | Tema | Puntaje | Total | Fecha |")
            st.write("|---|---|---:|---:|---|")
            for r in rows:
                st.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")
        else:
            st.info("No hay resultados guardados aún.")

    st.caption("Consejo: practica con 'Mixto' para combinar todos los usos (ever/never, already/yet/just, for/since, preguntas, participios).")

if __name__ == "__main__":
    main()
