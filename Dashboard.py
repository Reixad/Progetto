import streamlit as st
from charts.draw_metrics import DrawMetrics
from charts.line_chart import LineChart
from charts.histogram_chart import HistogramChart
from charts.pie_chart import PieChart
from utils.data_loader import DataLoader


st.title("📊 Dashboard dei Consumi Energetici")

dl = DataLoader("database/consumi.csv")
df = dl.df.copy()
dm = DrawMetrics()
lch = LineChart(df)
hc = HistogramChart(df)
pc = PieChart(df)

# --- METRICHE CONSUMI TOTALI ---

st.header("Metriche sui Consumi Energetici Totali")
dm._energy_sum_metrics()    
st.divider()

# --- LINE CHART ---
 
st.subheader("Andamento dei Consumi nel Tempo")
 
lche = lch._energy_timeslot_chart()
 
st.plotly_chart(lche, width="stretch")
 
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
 
 # --- ISTOGRAMMA CONSUMI TOTALI ---
 
st.subheader("Consumo Totale vs Medio Giornaliero per Fascia Oraria")
 
ist1 = hc._tot_consumes_timeslot_histogram()
 
# --- ISTOGRAMMA CONSUMI MEDI ---
 
ist2 = hc._avg_consumes_timeslot_histogram()
 
col1, col2 = st.columns(2)
 
with col1:
    st.plotly_chart(ist1, width="stretch")
 
with col2:
    st.plotly_chart(ist2, width="stretch")
 
# --- METRICHE CONSUMI MEDI ---

st.subheader("Metriche sui Consumi Energetici Medi Orari")
dm._energy_mean_metrics()
st.divider()

# --- GRAFICO A TORTA ---

st.subheader("Grafico a Torta dei Consumi per Fascia Oraria")

piec = pc._tot_consumes_timeslot_pie_chart()

st.plotly_chart(piec, width="stretch")
 