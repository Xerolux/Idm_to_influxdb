# Schnelle Lösung für ModuleNotFoundError

## Problem
Der Container konnte nicht starten mit folgendem Fehler:
```
ModuleNotFoundError: No module named 'idm_logger'
```

## Ursache
Das Dockerfile hatte `WORKDIR /app/data` gesetzt, wodurch Python das Modul nicht finden konnte.

## Lösung (SOFORT TESTEN)

Da der Fix im Feature-Branch ist, musst du das Image **lokal bauen** oder zum Main-Branch mergen:

### Option 1: Lokales Image bauen (EMPFOHLEN zum Testen)

```bash
cd ~/idm-metrics-collector

# 1. Aktuellen Branch pullen
git pull

# 2. Docker Compose mit lokalem Build starten
docker compose -f docker-compose.dev.yml down
docker compose -f docker-compose.dev.yml up --build -d

# 3. Logs prüfen
docker compose -f docker-compose.dev.yml logs -f idm-logger
```

**Erwartetes Ergebnis:**
```
idm-logger  | INFO:idm_logger.logger:Starting IDM Metrics Collector
idm-logger  | INFO:idm_logger.web:Starting web server on 0.0.0.0:5000
```

### Option 2: Zum Main-Branch mergen (für automatisches GHCR Build)

```bash
# Erst lokal testen (Option 1), dann:
git checkout main
git merge claude/test-docker-compose-website-dnR2k
git push origin main

# Warte 2-3 Minuten auf GitHub Actions Build
gh run watch

# Dann das neue GHCR Image pullen
docker compose pull
docker compose up -d
```

## Überprüfung

### Container Status prüfen
```bash
docker compose ps
```

Alle Container sollten **"healthy"** sein.

### Logs prüfen
```bash
docker compose logs idm-logger
```

**KEIN** `ModuleNotFoundError` mehr!

### Website testen
```bash
curl http://localhost:5008/api/health
```

**Erwartete Antwort:**
```json
{
  "status": "healthy",
  "setup_completed": false
}
```

### Im Browser
Öffne: http://localhost:5008

Du solltest automatisch zum Setup weitergeleitet werden.

## Was wurde geändert?

**Dockerfile (vor dem Fix):**
```dockerfile
WORKDIR /app
COPY idm_logger/ idm_logger/
WORKDIR /app/data  # ❌ Dies brach Python imports!
CMD ["python", "-m", "idm_logger.logger"]
```

**Dockerfile (nach dem Fix):**
```dockerfile
WORKDIR /app
COPY idm_logger/ idm_logger/
ENV DATA_DIR=/app/data  # ✅ Umgebungsvariable statt WORKDIR
CMD ["python", "-m", "idm_logger.logger"]
```

## Technische Details

Die Anwendung verwendet `DATA_DIR` Umgebungsvariable für Persistenz:
- `config.py:11`: `DATA_DIR = os.environ.get("DATA_DIR", ".")`
- `db.py:9`: `DATA_DIR = os.environ.get("DATA_DIR", ".")`

Daher funktioniert die Persistenz auch mit `ENV DATA_DIR=/app/data`, während Python das Modul von `/app` aus finden kann.

## Nächste Schritte

1. ✅ **Lokales Testen:** Nutze docker-compose.dev.yml zum lokalen Build
2. ✅ **Setup durchlaufen:** http://localhost:5008
3. ✅ **IDM konfigurieren:** Wärmepumpe verbinden
4. ✅ **Merge zum Main:** Nach erfolgreichem Test
5. ✅ **GHCR Image verwenden:** Nach GitHub Actions Build

---

**Fix committed:** 8dca60f
**Branch:** claude/test-docker-compose-website-dnR2k
**Datum:** 2026-01-08
