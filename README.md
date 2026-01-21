# Web-based-quiz-app

Projekt stanowi aplikację webową umożliwiającą tworzenie oraz rozwiązywanie quizów online. Aplikacja może być uruchamiana lokalnie, w środowisku kontenerowym, a także została przygotowana do wdrożenia w środowisku Kubernetes.

### W projekcie opracowane zostały manifesty kubernetes
W ramach projektu opracowane zostały manifesty Kubernetes, umożliwiające wdrożenie aplikacji w środowisku klastrowym (k3s). Zapewniają one kontenerowy model wdrożenia, orkiestrację zasobów oraz możliwość dalszej skalowalności systemu.

### Uruchamianie lokalne
```bash
git clone
cd web-based-quiz-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/app.py
```

Aplikacja będzie dostępna pod http://localhost:5000

## Uruchamianie w kontenerach (Docker)
W przypadku tego projektu używamy pliku **`dev-docker-compose.yml`**, który przeznaczony był do pracy w trybie development.
```bash
docker compose -f dev-docker-compose.yml up --build
```
### Zatrzymywanie pracy kontenera bez utraty danych
```bash
docker compose -f dev-docker-compose.yml stop
```
### Sprawdź działające kontenery:
docker ps
### Kontenery dostępne są pod:
http://localhost:5000 — aplikacja webowa
http://localhost:5050 — pgAdmin (panel bazy danych)

### Zatrzymywanie pracy kontenera bez utraty danych
```bash
docker compose -f dev-docker-compose.yml stop
```
### Wznawianie pracy na kontenerze 
```bash
docker compose -f dev-docker-compose.yml up
```
### Zatrzymywanie i usuwanie kontenerów
Aby zatrzymać i usunąć kontenery, ale **pozostawić dane w wolumenach** (np. baza danych):

```bash
docker compose -f dev-docker-compose.yml down
```
Jeśli chcesz całkowicie wyczyścić środowisko **łącznie z danymi przechowywanymi w wolumenach** (np. bazą danych), użyj polecenia:

```bash
docker compose -f dev-docker-compose.yml down -v
```
