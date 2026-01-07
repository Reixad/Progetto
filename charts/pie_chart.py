import pandas as pd
import plotly.graph_objects as go

class PieChart:
    def __init__(self, df : pd.DataFrame):
        self.df = df
        self.df['data'] = self.df['timestamp'].dt.date
        self.df_sum_sorted = (
            self.df
            .groupby(["data", "time_slot"])["consumo_kWh"]
            .sum()
            .reset_index()
        )
        
        
    def _tot_consumes_timeslot_pie_chart(self) -> go.Figure:
        totale = self.df_sum_sorted['consumo_kWh'].sum()
        self.df_sum_sorted['percentuale'] = (self.df_sum_sorted['consumo_kWh'] / totale * 100).round(1)

        colors = {
            "F1": "#2ecc71",  # verde
            "F2": "#f1c40f",  # giallo
            "F3": "#34495e"   # blu scuro
        }

        fig = go.Figure(
            data=[go.Pie(
                labels=self.df_sum_sorted['time_slot'],
                values=self.df_sum_sorted['consumo_kWh'],
                hole=.7, 
                marker_colors=[colors[f] for f in self.df_sum_sorted['time_slot']],
                textinfo='percent',
                hoverinfo='label+value',   
                textfont_size=15
            )]
        )

        fig.update_layout(
            height=400,
            width=400,
            showlegend=True,
            annotations=[dict(text='Consumo', x=0.5, y=0.5, font_size=20, showarrow=False)],
            margin=dict(l=40, r=150, t=40, b=40),
            legend=dict(orientation="v", yanchor="top", y=0.9, xanchor="left", x=-0.3)
        )
        
        return fig