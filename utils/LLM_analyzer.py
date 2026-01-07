from unittest import loader
import openai
from utils.data_loader import DataLoader

class LLMAnalyzer:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    def build_context(self, loader):
        stats = loader.basic_stats()
        patterns = loader.detect_patterns()

        context = "STATISTICHE DI CONSUMO:\n"
        for k, v in stats.items():
            context += f"- {k}: {v}\n"

        context += "\nPATTERN RILEVATI:\n"
        for p in patterns:
            context += f"- {p}\n"

        return context
 
    def generate_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": "Sei un assistente esperto nell'analisi dei consumi energetici domestici."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
 
        return response.choices[0].message.content