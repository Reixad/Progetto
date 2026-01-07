import streamlit as st
from utils.data_loader import DataLoader

class DrawMetrics:
    
    def __init__(self):
        self.dl = DataLoader("database/consumi.csv")
        self.df = self.dl.df.copy()

    def _energy_sum_metrics(self):
        df_sum_timeslot_sorted = (
            self.df
            .groupby("time_slot")["consumo_kWh"]
            .sum()
            .reindex(["F1", "F2", "F3"])
        )
        
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "🔆 F1 (8–19)",
            f"{df_sum_timeslot_sorted['F1']:.1f} kWh",
        )

        col2.metric(
            "🌗 F2 (7–8 / 19–23)",
            f"{df_sum_timeslot_sorted['F2']:.1f} kWh",
        )

        col3.metric(
            "🌙 F3 (23–7)",
            f"{df_sum_timeslot_sorted['F3']:.1f} kWh",
        )
        
    def _energy_mean_metrics(self):
        df_mean_timeslot_sorted = (
            self.df
            .groupby("time_slot")["consumo_kWh"]
            .mean()
            .reindex(["F1", "F2", "F3"])
        )
        
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "🔆 F1 (8–19)",
            f"{df_mean_timeslot_sorted['F1']:.2f} kWh",
        )

        col2.metric(
            "🌗 F2 (7–8 / 19–23)",
            f"{df_mean_timeslot_sorted['F2']:.2f} kWh",
        )

        col3.metric(
            "🌙 F3 (23–7)",
            f"{df_mean_timeslot_sorted['F3']:.2f} kWh",
        )
        
    def _temp_metrics(self):
        patterns = self.dl.detect_patterns()
        
        col1, col2 = st.columns(2)

        col1.metric(
            "🏠 Consumo vs T. Interna",
            f"{round(patterns.get('correlazione_consumo_temperatura_interna')*100, 2)}%",
        )

        col2.metric(
            "🏕️ Consumo vs T. Esterne",
            f"{round(patterns.get('correlazione_consumo_temperatura_esterna')*100, 2)}%",
        )