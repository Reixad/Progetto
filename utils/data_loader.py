import pandas as pd
import numpy as np
 
class DataLoader:
    def __init__(self, csv_path):
        """Inizializza l'analizzatore con i dati del CSV"""

        if csv_path is None:
            csv_path = "/app/database/consumi.csv"
        self.df = pd.read_csv(csv_path)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df['hour'] = self.df['timestamp'].dt.hour
        self.df['time_slot'] = self.df['hour'].apply(self._get_time_slot)
 
    def _get_time_slot(self, hour):
        """Classifica le ore in fasce orarie"""
        if 0 <= hour < 7 or hour >= 23:
            return 'F3'
        elif 7 <= hour < 8 or 19 <= hour < 23:
            return 'F2'
        elif 8 <= hour < 19:
            return 'F1'
       
    def basic_stats(self):
        """Calcola statistiche base dei consumi"""
        stats = {
            'consumo_tot': f"{np.round(self.df['consumo_kWh'].sum(), 4)} kWh",
            'consumo_medio': f"{np.round(self.df['consumo_kWh'].mean(), 4)} kWh",
            'picco_massimo_consumo': f"{self.df['picco_kW'].max()} kWh",
            'picco_minimo_consumo': f"{self.df['picco_kW'].min()} kWh",
            'consumo_tot_f3': f"{np.round(self.df[self.df['time_slot'] == 'F3']['consumo_kWh'].sum(), 4)} kWh",
            'consumo_tot_f2': f"{np.round(self.df[self.df['time_slot'] == 'F2']['consumo_kWh'].sum(), 4)} kWh",
            'consumo_tot_f1': f"{np.round(self.df[self.df['time_slot'] == 'F1']['consumo_kWh'].sum(), 4)} kWh",
            'consumo_medio_f3': f"{np.round(self.df[self.df['time_slot'] == 'F3']['consumo_kWh'].mean(), 4)} kWh",
            'consumo_medio_f2': f"{np.round(self.df[self.df['time_slot'] == 'F2']['consumo_kWh'].mean(), 4)} kWh",
            'consumo_medio_f1': f"{np.round(self.df[self.df['time_slot'] == 'F1']['consumo_kWh'].mean(), 4)} kWh",
        }
        
        return stats
    
    def detect_patterns(self):
        """Identifica pattern nei consumi"""
        consumo_medio_per_fascia = self.df.groupby('time_slot')['consumo_kWh'].mean()
        patterns = {
            "fascia_oraria_piu_costosa": consumo_medio_per_fascia.idxmax(),
            "ora_di_picco_massimo": self.df.loc[self.df['consumo_kWh'].idxmax()],
            "ora_di_picco_minimo": self.df.loc[self.df['consumo_kWh'].idxmin()],
            "correlazione_consumo_temperatura_esterna": self.df['consumo_kWh'].corr(self.df['temperatura_esterna']),
            "correlazione_consumo_temperatura_interna": self.df['consumo_kWh'].corr(self.df['temperatura_interna'])
        }
        
        return patterns