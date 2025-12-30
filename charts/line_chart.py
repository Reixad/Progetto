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
 