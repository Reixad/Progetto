import streamlit as st
from charts.draw_metrics import DrawMetrics
from charts.line_chart import LineChart
from utils.data_loader import DataLoader

st.title("📊 Dashboard dei Consumi Energetici")

dl = DataLoader("database/consumi.csv")
df = dl.df.copy()
dm = DrawMetrics()
lch = LineChart(df)

# --- METRICHE CONSUMI TOTALI ---

st.header("Metriche sui Consumi Energetici Totali")

dm._energy_metrics()    

st.divider()

# --- LINE CHART TEMPERATURE ---
 
st.subheader("Andamento della Temperatura Interna vs Esterna nel Tempo")
 
lchti = lch._default_chart("temperatura_interna", "Data / Ora", "Temperatura Interna (°C)", "#e74c3c")
 
lchte = lch._default_chart("temperatura_esterna", "Data / Ora", "Temperatura Esterna (°C)", "#3498db")
 
col1, col2 = st.columns(2)
 
with col1:
    st.plotly_chart(lchti, width="stretch")
 
with col2:
    st.plotly_chart(lchte, width="stretch")
 
# ---------- METRICHE CORRELAZIONE ----------
   
st.subheader("Informazioni sulla Correlazione Consumi vs Temperature")
 
dm._temp_metrics()
 
st.divider()
 