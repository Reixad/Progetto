import pandas as pd
import numpy as np
 
class DataLoader:
    def __init__(self, csv_path):
        """Inizializza l'analizzatore con i dati del CSV"""
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
            'consumo_tot_giornaliero': f"{np.round(self.df['consumo_kWh'].sum(), 4)} kWh",
            'consumo_medio': f"{np.round(self.df['consumo_kWh'].mean(), 4)} kWh",
            'picco_massimo_consumo': f"{self.df['picco_kW'].max()} kWh",
            'picco_minimo_consumo': f"{self.df['picco_kW'].min()} kWh",
            'consumo_tot_f3': f"{np.round(self.df[((self.df['hour'] >= 0) & (self.df['hour'] < 7)) | (self.df['hour'] >= 23)]['consumo_kWh'].sum(), 4)} kWh",
            'consumo_tot_f2': f"{np.round(self.df[((self.df['hour'] >= 7) & (self.df['hour'] < 8)) | ((self.df['hour'] >= 19) & (self.df['hour'] < 23))]['consumo_kWh'].sum(), 4)} kWh",
            'consumo_tot_f1': f"{np.round(self.df[(self.df['hour'] >= 8) & (self.df['hour'] < 19)]['consumo_kWh'].sum(), 4)} kWh",
            'consumo_medio_f3': f"{np.round(self.df[((self.df['hour'] >= 0) & (self.df['hour'] < 7)) | (self.df['hour'] >= 23)]['consumo_kWh'].mean(), 4)} kWh",
            'consumo_medio_f2': f"{np.round(self.df[((self.df['hour'] >= 7) & (self.df['hour'] < 8)) | ((self.df['hour'] >= 19) & (self.df['hour'] < 23))]['consumo_kWh'].mean(), 4)} kWh",
            'consumo_medio_f1': f"{np.round(self.df[(self.df['hour'] >= 8) & (self.df['hour'] < 19)]['consumo_kWh'].mean(), 4)} kWh"
        }
        return stats