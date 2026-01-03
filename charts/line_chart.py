import plotly.graph_objects as go  
import pandas as pd
 
class LineChart:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.df = (
            self.df
            .sort_values("timestamp")
            .reset_index(drop=True)
        )
 
    def _default_chart(self, field: str, xaxis_title: str, yaxis_title: str, color: str) -> go.Figure:
       
        lch = go.Figure()
 
        lch.add_trace(
            go.Scatter(
                x=self.df["timestamp"],
                y=self.df[field],
                mode="lines",
                line=dict(color=color, width=2),
                showlegend=False
            )
        )
               
        lch.update_layout(
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            xaxis=dict(
                rangeslider=dict(visible=True),   # pan orizzontale
                type="date"
                ),
            yaxis=dict(
                fixedrange=True                   # blocca scroll verticale
                ),
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
       
        return lch
    def _energy_timeslot_chart(self) -> go.Figure:
       
        color_map = {
            "F1": "#2ecc71",  # verde
            "F2": "#f1c40f",  # giallo
            "F3": "#34495e"   # blu scuro
        }
 
        lch = go.Figure()
 
        start_idx = 0 # indice di inizio del segmento
 
        for i in range(1, len(self.df)):
            fascia_corrente = self.df.loc[i, "time_slot"]
            fascia_precedente = self.df.loc[i - 1, "time_slot"]
           
            # quando cambia fascia → chiudi il segmento
            if fascia_corrente != fascia_precedente:
                   
                segment = self.df.iloc[start_idx:i+1]
                lch.add_trace(
                    go.Scatter(
                        x=segment["timestamp"],
                        y=segment["consumo_kWh"],
                        mode="lines",
                        line=dict(color=color_map[fascia_precedente], width=2),
                    )
                )
 
                start_idx = i
               
        lch.update_layout(
            xaxis_title="Data / Ora",
            yaxis_title="Consumo (kW)",
            xaxis=dict(
                rangeslider=dict(visible=True),   # pan orizzontale
                type="date"
                ),
            yaxis=dict(
                fixedrange=True                   # blocca scroll verticale
                ),
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
           
        )
 
        return lch
 