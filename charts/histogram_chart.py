import pandas as pd
import plotly.express as px
 
class HistogramChart:
   
    def __init__(self, df: pd.DataFrame):
        self.df = df
 
    def _tot_consumes_timeslot_histogram(self) -> px.bar:
        df_sum_sorted = (
            self.df
            .groupby(["data", "time_slot"])["consumo_kWh"]
            .sum()
            .reset_index()
        )
       
        hist = px.bar(
            df_sum_sorted,
            x="data",
            y="consumo_kWh",
            color="time_slot",
            barmode="group",
            color_discrete_map={
                "F1": "#2ecc71",  # verde
                "F2": "#f1c40f",  # giallo
                "F3": "#34495e"   # blu scuro
            }
        )
 
        hist.update_layout(
            xaxis_title="Data",
            yaxis_title="Consumo (kWh)",
            yaxis=dict(
                fixedrange=True                   # blocca scroll verticale
            ),
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
 
        return hist
   
    def _avg_consumes_timeslot_histogram(self) -> px.bar:
        df_avg_sorted = (
            self.df
            .groupby(["data", "time_slot"])["consumo_kWh"]
            .mean()
            .reset_index()
        )
       
        hist = px.bar(
            df_avg_sorted,
            x="data",
            y="consumo_kWh",
            color="time_slot",
            barmode="group",
            color_discrete_map={
                "F1": "#2ecc71",  # verde
                "F2": "#f1c40f",  # giallo
                "F3": "#34495e"   # blu scuro
            }
        )
 
        hist.update_layout(
            xaxis_title="Data",
            yaxis_title="Consumo (kWh)",
            yaxis=dict(
                fixedrange=True                   # blocca scroll verticale
            ),
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
 
        return hist
 