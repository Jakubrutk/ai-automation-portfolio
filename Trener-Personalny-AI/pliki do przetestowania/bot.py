import os
import requests
import json
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych
load_dotenv()

class PersonalTrainerBot:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.user_data = {}
        self.available_equipment = [
            'seated dip', 'biceps curl', 'linear leg press', 'abdominal crunch',
            'pectoral machine', 'leg extension', 'leg curl', 'arm curl',
            'seated leg press', 'front pulldown', 'decline chest press',
            'vertical traction', 'shoulder press', 'hip adduction', 'glute machine',
            'pectoral fly / rear deltoid', '4-stack multi-station', 'ławka rzymska',
            'podciąganie na drążku', 'bieżnia lub schody'
        ]

    def get_user_data(self):
        print("👋 Witaj! Jestem Twoim osobistym trenerem AI.")
        print("Aby stworzyć spersonalizowany plan treningowy, potrzebuję kilku informacji.\n")
        
        self.user_data['gender'] = input("Podaj płeć (kobieta/mężczyzna): ")
        self.user_data['age'] = input("Podaj wiek: ")
        self.user_data['height'] = input("Podaj wzrost (w cm): ")
        self.user_data['weight'] = input("Podaj aktualną wagę (w kg): ")
        self.user_data['level'] = input("Poziom zaawansowania (początkujący/średniozaawansowany/zaawansowany): ")
        self.user_data['goal'] = input("Cel (przyrost masy/redukcja tłuszczu/poprawa siły/poprawa sylwetki): ")
        
        print("\nDostępne partie ciała do wyboru:")
        print("1. Klatka piersiowa")
        print("2. Plecy")
        print("3. Nogi")
        print("4. Barki")
        print("5. Biceps")
        print("6. Triceps")
        print("7. Brzuch")
        print("8. Pośladki")
        
        focus_areas = input("\nNa których partiach chcesz się skupić? (podaj numery oddzielone przecinkami, np. 1,3,7): ")
        area_mapping = {
            '1': 'klatka piersiowa', '2': 'plecy', '3': 'nogi', 
            '4': 'barki', '5': 'biceps', '6': 'triceps', 
            '7': 'brzuch', '8': 'pośladki'
        }
        
        selected_areas = []
        for area in focus_areas.split(','):
            area = area.strip()
            if area in area_mapping:
                selected_areas.append(area_mapping[area])
        
        self.user_data['focus_areas'] = selected_areas

    def generate_workout_plan(self):
        prompt = self._create_prompt()
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Jesteś profesjonalnym trenerem personalnym i fizjologiem sportowym. Tworzysz szczegółowe plany treningowe."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"❌ Błąd podczas komunikacji z API: {e}")
            return None

    def _create_prompt(self):
        return f"""
Stwórz profesjonalny plan treningowy na 2 dni w tygodniu dla następującej osoby:
- Płeć: {self.user_data['gender']}
- Wiek: {self.user_data['age']}
- Wzrost: {self.user_data['height']} cm
- Waga: {self.user_data['weight']} kg
- Poziom: {self.user_data['level']}
- Cel: {self.user_data['goal']}
- Partie do skupienia: {', '.join(self.user_data['focus_areas'])}

Dostępny sprzęt: {', '.join(self.available_equipment)}

Wymagania:
1. Wybierz najlepsze ćwiczenia z dostępnego sprzętu
2. Stwórz plan na 2 różne dni treningowe
3. Dla każdego ćwiczenia podaj:
   - Liczbę serii
   - Liczbę powtórzeń
   - Długość przerw między seriami
   - Sugerowany ciężar (% ciężaru maksymalnego lub % masy ciała)
4. Dodaj progresję obciążeń/powtórzeń na kolejne tygodnie
5. Przedstaw plan w formie czytelnej tabeli (Dzień 1 i Dzień 2)
6. Dodaj krótkie wytłumaczenie, dlaczego taki plan został ułożony

Plan ma być profesjonalny, praktyczny i dopasowany indywidualnie.
"""

    def run(self):
        self.get_user_data()
        print("\n🔄 Tworzę Twój spersonalizowany plan treningowy...\n")
        
        plan = self.generate_workout_plan()
        if plan:
            print("✅ Twój plan treningowy został przygotowany!\n")
            print(plan)
            
            # Zapis planu do pliku
            with open('plan_treningowy.txt', 'w', encoding='utf-8') as f:
                f.write(plan)
            print(f"\n📝 Plan został również zapisany do pliku 'plan_treningowy.txt'")
        else:
            print("❌ Nie udało się wygenerować planu treningowego.")

if __name__ == "__main__":
    bot = PersonalTrainerBot()
    bot.run()