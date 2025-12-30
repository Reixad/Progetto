import openai
 
class LLMAnalyzer:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
 
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