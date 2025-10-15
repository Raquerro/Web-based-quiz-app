# Web-based-quiz-app

Aby uruchomić projekt lokalnie:

### 1️⃣ Sklonuj repozytorium
```bash```
git clone
cd web-based-quiz-app
### 2️⃣ Utwórz środowisko wirtualne
Linux
python3 -m venv venv
source venv/bin/activate

###  3️⃣ Zainstaluj zależności 
pip install -r requirements.txt


### Kolejne uruchomienie i uruchomienie aplikacji - flask
source venv/bin/activate

python app/app.py

### Wyłączenie środowiska
deactivate

### 🚀 4️⃣ **Uruchamianie aplikacji**

### Zbuduj i uruchom kontenery:
```bash```
podman compose up --build

### Sprawdź działające kontenery:
podman ps

### Aplikacja będzie dostępna pod:
http://localhost:5000 — interfejs quizu
http://localhost:5050 — pgAdmin (panel bazy danych)

### 🧠 6️⃣ **Podstawowe polecenia do zarządzania**
| Czynność | Polecenie |
|-----------|------------|
| Zatrzymanie kontenerów | `podman compose down` |
| Restart aplikacji | `podman compose restart web` |
| Logi aplikacji | `podman logs -f quiz_web` |
| Wejście do bazy danych | `podman exec -it quiz_db psql -U quizuser -d quizdb` |
| Uruchomienie kontenerów w tle | `podman compose up --build -d` |

## pgAdmin – interfejs graficzny bazy danych

pgAdmin jest dostępny pod adresem: [http://localhost:5050](http://localhost:5050)  
