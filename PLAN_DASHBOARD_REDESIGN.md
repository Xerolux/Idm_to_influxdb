# Dashboard Redesign Plan

## Ziel
Das Dashboard funktional machen mit:
- Benutzerdefinierte Dashboards (erstellen, löschen, verwalten)
- Sensor-Liste in Sidebar zum Hinzufügen zu Charts
- Echte Grafana/VictoriaMetrics Integration

## Architektur

### Backend (idm_logger/)
1. **Neu: `dashboard_config.py`** - Dashboard-Konfigurationsmanager
   - Dashboards in `config.data["dashboards"]` speichern
   - Struktur:
     ```yaml
     dashboards:
       - id: "default"
         name: "Home Dashboard"
         charts:
           - id: "chart1"
             title: "Underfloor Heating"
             queries: [...]
               - label: "Flow Temp"
                 query: "temp_flow_current_circuit_A"
                 color: "#f59e0b"
             hours: 12
       - id: "custom1"
         name: "Mein Dashboard"
         charts: [...]
     ```

2. **Neu: API Endpoints in `web.py`**
   - `GET /api/dashboards` - Liste aller Dashboards
   - `POST /api/dashboards` - Neues Dashboard erstellen
   - `PUT /api/dashboards/<id>` - Dashboard aktualisieren
   - `DELETE /api/dashboards/<id>` - Dashboard löschen
   - `GET /api/metrics/available` - Liste aller verfügbaren Sensoren von VictoriaMetrics

### Frontend (frontend/src/)

#### Neue Components
1. **`DashboardManager.vue`** - Hauptdashboard-Komponente
   - Dashboard-Auswahl (Dropdown)
   - Dashboard erstellen/löschen Buttons
   - Grid von ChartCard-Komponenten

2. **`SensorSidebar.vue`** - Sidebar mit Sensor-Liste
   - Holt alle verfügbaren Sensoren von `/api/metrics/available`
   - Drag-and-drop oder Klick zum Hinzufügen zu Charts
   - Filter/Suche nach Sensoren

3. **`ChartCard.vue`** - Verbesserte `LineChartCard`
   - Edit-Modus zum Entfernen
   - Konfigurieren (Queries, Farben, Zeitraum)
   -Fullscreen-Option

4. **`ChartConfigDialog.vue`** - Dialog zum Konfigurieren eines Charts
   - Queries hinzufügen/entfernen
   - Farben auswählen
   - Zeitraum wählen

#### Änderungen an bestehenden Dateien
1. **`views/Dashboard.vue`** - Komplett überarbeiten
   - Fake Breadcrumbs entfernen
   - `DashboardManager` verwenden
   - `SensorSidebar` integrieren

2. **`router/index.js`** - Keine Änderungen nötig (Route bleibt `/`)

3. **`components/Layout.vue`** - Keine Änderungen nötig

## Implementierungs-Schritte

### Phase 1: Backend API
1. `dashboard_config.py` erstellen mit Dashboard-Klasse
2. API Endpoints in `web.py` hinzufügen
3. Endpoint `/api/metrics/available` implementiert:
   - Queryt VictoriaMetrics nach allen `idm_heatpump` Metriken
   - Gibt strukturierte Liste zurück (gruppiert nach Typ)

### Phase 2: Frontend Components
4. `SensorSidebar.vue` erstellen
5. `ChartConfigDialog.vue` erstellen
6. `DashboardManager.vue` erstellen
7. `Dashboard.vue` überarbeiten

### Phase 3: Integration
8. Dashboard-Konfiguration speichern/laden
9. Edit-Modus für Dashboards
10. Tests und Bugfixes

## Dateien

### Neu erstellen
- `idm_logger/dashboard_config.py`
- `frontend/src/components/DashboardManager.vue`
- `frontend/src/components/SensorSidebar.vue`
- `frontend/src/components/ChartConfigDialog.vue`

### Bearbeiten
- `frontend/src/views/Dashboard.vue` (komplettes Redesign)
- `idm_logger/web.py` (neue API Endpoints)
- `idm_logger/config.py` (evtl. für Dashboards-Struktur)

## UI-Flow

1. User öffnet `/` → sieht aktuelles Dashboard
2. Sidebar links zeigt Liste aller Sensoren
3. User kann:
   - Neues Dashboard erstellen (Button oben)
   - Dashboard wechseln (Dropdown)
   - Aktuelles Dashboard löschen (wenn nicht das einzige)
   - Sensor aus Sidebar anklicken → wird zu neuem Chart hinzugefügt
   - Bearbeiten-Modus aktivieren → Charts können konfiguriert/entfernt werden
4. Änderungen werden automatisch gespeichert

## Technische Details

### VictoriaMetrics Query für verfügbare Sensoren
```
{__name__=~"idm_heatpump.*"}
```
Antwort analysieren und gruppieren nach:
- Temperaturen (temp_*)
- Leistung (power_*)
- Druck (pressure_*)
- Status (status_*)
- etc.
