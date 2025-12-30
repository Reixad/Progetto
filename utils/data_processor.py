class DataProcessor:
    def __init__(self, stats: dict, patterns: list):
        """Inizializza il processore con le statistiche calcolate"""
        self.stats = stats
        self.patterns = patterns
   
    def build_prompt(self, stats: dict, patterns : list):
        """Prepara un prompt chiaro e strutturato per l'LLM."""
 
        prompt = f"""
            Analizza i seguenti dati di consumo energetico domestico.
 
            STATISTICHE DI BASE:
            - Consumo totale: {stats.get('consumo_tot_giornaliero')} kWh
            - Consumo medio: {stats.get('consumo_medio')} kWh
            - Consumo massimo: {stats.get('picco_massimo_consumo')} kWh
            - Consumo minimo: {stats.get('picco_minimo_consumo')} kWh
            - Consumo totale fascia F3: {stats.get('consumo_tot_f3')} kWh
            - Consumo totale fascia F2: {stats.get('consumo_tot_f2')} kWh
            - Consumo totale fascia F1: {stats.get('consumo_tot_f1')} kWh
            - Consumo medio fascia F3: {stats.get('consumo_medio_f3')} kWh
            - Consumo medio fascia F2: {stats.get('consumo_medio_f2')} kWh
            - Consumo medio fascia F1: {stats.get('consumo_medio_f1')} kWh
 
            PATTERNS RILEVATI:
            - Fascia oraria con consumo medio più alto: {patterns.get('fascia_oraria_piu_costosa')}
            - Ora di picco massimo con relativo consumo: {patterns.get('ora_di_picco_massimo')}
            - Ora di picco minimo con relativo consumo: {patterns.get('ora_di_picco_minimo')}
            - Correlazione consumo-temperatura esterna: {patterns.get('correlazione_consumo_temperatura_esterna')}
            - Correlazione consumo-temperatura interna: {patterns.get('correlazione_consumo_temperatura_interna')}
           
            OBIETTIVO:
            - Spiega possibili cause dei picchi
            - Identifica sprechi energetici
            - Suggerisci strategie di ottimizzazione
 
            NOTE:
            le fasce orarie rappresentano le fasce di consumo energetico giornaliero standard in Italia.
 
            Rispondi in modo chiaro e strutturato.
                """
        return prompt.strip()
 