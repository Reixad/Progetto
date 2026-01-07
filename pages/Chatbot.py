import streamlit as st
from utils.data_loader import DataLoader
from utils.LLM_analyzer import LLMAnalyzer
from pathlib import Path

def check_openai_key() -> tuple[bool, str]:
    """Controlla se la OpenAI API Key è configurata"""
    
    # Controlla se il file esiste
    config_file = Path(".streamlit/secrets.toml")
    
    if not config_file.exists():
        return False, "File secrets.toml non trovato"
    
    # Controlla se la key esiste nei secrets
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        return False, "Errore nel leggere secrets.toml"
    
    # Controlla se la key ha formato valido
    if not api_key.startswith("sk-"):
        return False, f"Formato key non valido (inizia con: {api_key[:10]}...)"
    
    return True, "✅ API Key configurata correttamente"
   

def setup_openai_key():
    """Guida l'utente a configurare la API key"""
    
    st.sidebar.title("🔑 Configurazione OpenAI")
    
    config_file = Path(".streamlit/secrets.toml")
    
    # Controlla se già configurato
    is_configured, message = check_openai_key()
    
    if is_configured:
        st.sidebar.success("✅ API Key configurata")
        return True
    
    # Se non configurato, mostra setup guidato
    with st.sidebar.expander("⚙️ Configura Chatbot AI", expanded=True):
        st.info(f"""
        Attenzione: {message}
        
        Per usare il chatbot, serve una OpenAI API Key.
        
        **Ottienila gratuitamente:**
        1. Vai su [platform.openai.com](https://platform.openai.com)
        2. Crea account (crediti gratuiti inclusi)
        3. Vai a API Keys → Create new key
        4. Copia la chiave (inizia con `sk-`)
        """)
        
        api_key = st.text_input(
            "Incolla la tua OpenAI API Key:",
            type="password",
            placeholder="sk-...",
            help="La chiave rimane solo sul tuo computer"
        )
        
        if st.button("💾 Salva Configurazione", type="primary"):
            if api_key and api_key.startswith("sk-"):
                # Crea cartella .streamlit se non esiste
                config_file.parent.mkdir(exist_ok=True)
                
                # Salva in secrets.toml
                with open(config_file, "w") as f:
                    f.write(f'OPENAI_API_KEY = "{api_key}"')
                
                st.success("✅ Configurazione salvata in `.streamlit/secrets.toml`")
                st.rerun()
            else:
                st.error("⚠️ Inserisci una API key valida (inizia con 'sk-')")
                
def main():
    """Main function per la pagina Chatbot"""

    st.set_page_config(page_title="Chatbot AI", page_icon="🤖")
    
    loader = DataLoader("database/consumi.csv")
    
    st.title("🤖 Chatbot Analisi Consumi")

    # --- CHECK OPENAI KEY ---
    
    if not setup_openai_key():
        st.warning("""
        ## ⚠️ Chatbot AI non configurato
        
        Configura la OpenAI API Key nella sidebar per usare il chatbot.
        
        Nel frattempo puoi:
        - Vedere la dashboard dei consumi
        - Analizzare i grafici
        - Esplorare le statistiche
        """)
        return
    
    # --- INIT ---
    
    llm = LLMAnalyzer(api_key=st.secrets["OPENAI_API_KEY"])
    
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
            
if __name__ == "__main__":
    main()