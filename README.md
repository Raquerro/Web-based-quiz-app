# Web-based-quiz-app

Aby uruchomić projekt lokalnie bez zastosowania kontenera.
### 1️⃣ Sklonuj repozytorium
```bash```
git clone
cd web-based-quiz-app
### 2️⃣ Utwórz środowisko wirtualne
`` Linux ``
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

## 🚀 Uruchamianie środowiska developerskiego
Domyślnie Docker Compose korzysta z pliku `docker-compose.yml`.  
W przypadku tego projektu używamy jednak pliku **`dev-docker-compose.yml`**, który jest przeznaczony do pracy w trybie development.
### Uruchomienie
Aby zbudować i uruchomić kontenery, wykonaj polecenie:
```bash
docker compose -f dev-docker-compose.yml up --build
```
### Zatrzymywanie pracy kontenera bez utraty danych
```bash
docker compose -f dev-docker-compose.yml stop
```
### Wznawianie pracy na kontenerze 
```bash
docker compose -f dev-docker-compose.yml up
```

## 🛑 Zatrzymywanie i usuwanie kontenerów

#### Całkowite wyłączenie i usunięcie kontenerów (z zachowaniem danych)
Aby zatrzymać i usunąć kontenery, ale **pozostawić dane w wolumenach** (np. baza danych):

```bash
docker compose -f dev-docker-compose.yml down 
```
## 🗑️ Usuwanie kontenerów wraz z danymi tj. wolumenami

Jeśli chcesz całkowicie wyczyścić środowisko **łącznie z danymi przechowywanymi w wolumenach** (np. bazą danych), użyj polecenia:

```bash
docker compose -f dev-docker-compose.yml down -v
```

# 🐧Uruchamianie środowiska developerskiego z Podmanem
W projekcie dostępne są dwa pliki Compose:
docker-compose.yml → konfiguracja środowiska produkcyjnego
dev-docker-compose.yml → konfiguracja środowiska developerskiego
Podman jest w pełni kompatybilny z plikami Docker Compose dzięki narzędziu podman-compose lub natywnej integracji podman compose w nowszych wersjach.

## 🔧 Wymagania
Upewnij się, że masz zainstalowany:
```bash
podman --version
podman-compose --version   # lub używaj podman compose (jeśli dostępne)
```
🧩 Jeśli nie masz podman-compose, możesz zainstalować:
```bash
pip install podman-compose
```
## 🚀 Uruchamianie środowiska developerskiego
### 1️⃣ Uruchomienie kontenerów
Zbudowanie i uruchomienie środowiska deweloperskiego:
```bash
podman compose -f dev-docker-compose.yml up --build
```
lub, jeśli używasz osobnego narzędzia podman-compose:
```bash
podman-compose -f dev-docker-compose.yml up --build
```
🔹 Flaga --build wymusza przebudowanie obrazów po zmianach w kodzie.
🔹 Wszystko działa identycznie jak w Docker Compose.
### 2️⃣ Zatrzymywanie środowiska (bez utraty danych)
Zatrzymaj działające kontenery bez usuwania danych:
```bash
podman compose -f dev-docker-compose.yml stop
```
lub
```bash
podman-compose -f dev-docker-compose.yml stop
```
Wszystkie wolumeny i dane pozostają nienaruszone.
### 3️⃣ Wznowienie środowiska
Aby ponownie uruchomić zatrzymane kontenery:
```bash
podman compose -f dev-docker-compose.yml start
```
## 🛑Zatrzymywanie i usuwanie środowiska
### Usunięcie kontenerów (z zachowaniem danych)
```bash
podman compose -f dev-docker-compose.yml down
```
### Usuwa kontenery, ale zostawia dane w wolumenach.
## 🗑️Całkowite czyszczenie (łącznie z danymi)
Jeśli chcesz usunąć kontenery i dane w wolumenach (czyli np. wyczyścić bazę danych):
```bash
podman compose -f dev-docker-compose.yml down -v --remove-orphans
```
🔸 --remove-orphans usuwa kontenery niepowiązane z bieżącym plikiem Compose.
🔸 -v usuwa wolumeny, czyli dane (np. bazy, pliki).

### W projekcie opracowane zostały manifesty kubernetes