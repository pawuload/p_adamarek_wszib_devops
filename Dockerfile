# ETAP 1: Builder - budowanie zależności i aplikacji
FROM python:3.11-slim as builder

# Instalacja narzędzi potrzebnych do budowania
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie requirements.txt i instalacja zależności
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Kopiowanie kodu aplikacji
COPY app/ .

# ETAP 2: Test - uruchamianie testów pytest
FROM builder as test

# Ustawienie zmiennych środowiskowych dla testów
ENV PYTHONPATH=/app
ENV FLASK_APP=wsgi.py

# Uruchomienie testów - build się zatrzyma jeśli testy nie przejdą
RUN pip install --user pytest pytest-cov pytest-flask && \
    python -m pytest tests/ -v --tb=short || exit 1

# ETAP 3: Final - lekki obraz produkcyjny
FROM python:3.11-slim as final

# Instalacja tylko runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie zainstalowanych pakietów z buildera
COPY --from=builder /root/.local /root/.local

# Upewnienie się, że skrypty są w PATH
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV FLASK_APP=wsgi.py

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie tylko kodu aplikacji (bez requirements.txt)
COPY app/ .

# Port aplikacji Flask
EXPOSE 5000

# Uruchomienie aplikacji
CMD ["python", "wsgi.py"]
