import streamlit as st
from utils.data_loader import DataLoader
from utils.LLM_analyzer import LLMAnalyzer

st.set_page_config(page_title="Chatbot AI", page_icon="🤖")

st.title("🤖 Chatbot Analisi Consumi")

# --- INIT ---
loader = DataLoader("database/consumi.csv")

llm = LLMAnalyzer(api_key=st.secrets["OPEN_API_KEY"])
context = llm.build_context(loader)

# --- SESSION STATE ---
# Inizializza la cronologia della chat se non esiste alcun messaggio
# Resetta la cronologia al refresh della pagina
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CHAT HISTORY ---
# Ristampa la cronologia della chat ad ogni nuovo messaggio
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- USER INPUT ---
if prompt := st.chat_input("Chiedimi qualcosa sui consumi energetici..."):
    
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # prompt finale per LLM
    full_prompt = f"""
    Contesto dati:
    {context}

    Domanda utente:
    {prompt}

    Rispondi in modo chiaro e conciso, usando i dati forniti.
    """
    response = llm.generate_response(full_prompt)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        with st.status("L'AI sta analizzando i consumi...", expanded=True) as status:
            st.write("Recupero statistiche e pattern...")
            
            response = llm.generate_response(full_prompt)
            status.update(label="Analisi completata!", state="complete", expanded=False)
        st.markdown(response)