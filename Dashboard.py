import streamlit as st
from charts.draw_metrics import DrawMetrics
from utils.data_loader import DataLoader

st.title("📊 Dashboard dei Consumi Energetici")

dl = DataLoader("database/consumi.csv")
df = dl.df.copy()
dm = DrawMetrics()

# --- METRICHE CONSUMI TOTALI ---

st.header("Metriche sui Consumi Energetici Totali")

dm._energy_metrics()    

st.divider()