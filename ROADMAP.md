# IDM Metrics Collector - Roadmap

## Vision

100% Feature-Parität zu Grafana bei deutlich einfacherer Handhabung und besserer Integration.

---

## Aktueller Stand: v0.7.0 (~80% Parität)

### ✅ Erledigt

- [x] Line Charts mit Zoom & Pan
- [x] Dual Y-Achsen
- [x] Stat & Gauge Panels
- [x] Chart Templates
- [x] Dark Mode
- [x] Drag & Drop Dashboard
- [x] Responsive Design
- [x] Tooltips mit deutschen Formaten

---

## Was fehlt zu 100% Grafana-Parität?

### 🔴 Hohe Priorität (Core Features)

#### 1. Annotations / Markierungen
**Beschreibung**: Zeitbasierte Markierungen im Chart (z.B. "Wartung am 15.1.", "Filter gewechselt")

**Grafana**: Annotations Panel mit Event-Overlay

**Umsetzung**:
- [ ] Annotations API Endpoint (`/api/annotations`)
- [ ] Annotation UI (Dialog zum Erstellen)
- [ ] Chart Rendering (vertikale Linien, Labels)
- [ ] Annotation Management (Liste, Edit, Delete)

**Aufwand**: 4-6 Stunden

**Files**:
- `idm_logger/web.py` - API Endpoints
- `idm_logger/annotations.py` - Model & Manager
- `frontend/src/components/AnnotationDialog.vue` - UI
- `frontend/src/components/ChartCard.vue` - Rendering

---

#### 2. Variables / Template Variables
**Beschreibung**: Platzhalter in Queries, z.B. `$heizkreis`, `$zeitraum`

**Grafana**: Dashboard Variables mit Dropdown-Auswahl

**Umsetzung**:
- [ ] Variables API (`/api/variables`)
- [ ] Variable Types: Query, Custom, Interval
- [ ] Variable UI (Dropdown im Dashboard)
- [ ] Query Parser (ersetze $vars in queries)
- [ ] Variable Dependencies (var2 hängt von var1 ab)

**Aufwand**: 6-8 Stunden

**Files**:
- `idm_logger/variables.py` - Model
- `idm_logger/web.py` - API
- `frontend/src/stores/variables.js` - Store
- `frontend/src/components/VariableSelector.vue` - UI
- `frontend/src/utils/queryParser.js` - Parser

---

#### 3. Bar Charts & Histograms
**Beschreibung**: Balkendiagramme für Verteilungen

**Grafana**: Bar Chart Panel

**Umsetzung**:
- [ ] Chart.js Bar Chart Integration
- [ ] BarCard Component
- [ ] Konfiguration (horizontal/vertikal, stacked, grouped)
- [ ] Time-based Bar Charts (z.B. Energie pro Tag)

**Aufwand**: 3-4 Stunden

**Files**:
- `frontend/src/components/BarCard.vue` - Component
- `frontend/src/utils/chartTypes.js` - Chart Type Registry

---

#### 4. Dashboard Export (PNG/PDF)
**Beschreibung**: Dashboard als Bild oder PDF exportieren

**Grafana**: Share → Export

**Umsetzung**:
- [ ] html2canvas oder dom-to-image Integration
- [ ] Export Dialog (Format, Qualität, Bereich)
- [ ] PDF Generation mit jsPDF
- [ ] Batch Export (alle Dashboards)

**Aufwand**: 4-5 Stunden

**Files**:
- `frontend/src/utils/dashboardExport.js` - Export Logic
- `frontend/src/components/ExportDialog.vue` - UI
- `frontend/package.json` - Dependencies (html2canvas, jsPDF)

---

### 🟡 Mittlere Priorität (Nice-to-Have)

#### 5. Math Queries / Expressions
**Beschreibung**: Mathematische Ausdrücke in Queries, z.B. `A/B`, `A*100`, `(A+B)/2`

**Grafana**: Query Expressions / Transformations

**Umsetzung**:
- [ ] Expression Parser (sicherer eval)
- [ ] Supported Operations: +, -, *, /, (), avg, sum, min, max
- [ ] Query Builder UI
- [ ] Expression Validation

**Aufwand**: 5-6 Stunden

**Files**:
- `idm_logger/query_parser.py` - Backend Parser
- `frontend/src/utils/expressionParser.js` - Frontend Parser
- `frontend/src/components/ExpressionBuilder.vue` - UI

---

#### 6. Custom CSS pro Dashboard
**Beschreibung**: Benutzerdefiniertes CSS für einzelne Dashboards

**Grafana**: CSS Panel Options

**Umsetzung**:
- [ ] CSS Editor (Monaco/CodeMirror)
- [ ] CSS Sandbox (scoped styles)
- [ ] CSS Validation
- [ ] Preview Mode

**Aufwand**: 3-4 Stunden

**Files**:
- `frontend/src/components/CssEditor.vue` - UI
- `idm_logger/dashboard_config.py` - CSS Storage
- Security: CSP restrictions beachten

---

#### 7. WebSocket Live Updates
**Beschreibung**: Echtzeit-Updates ohne Polling

**Grafana**: Live Streaming

**Umsetzung**:
- [ ] WebSocket Server (Flask-SocketIO)
- [ ] WebSocket Client Integration
- [ ] Auto-Reconnect Logic
- [ ] Selective Subscriptions (nur benötigte Metriken)

**Aufwand**: 6-8 Stunden

**Files**:
- `idm_logger/websocket.py` - Server
- `idm_logger/__init__.py` - SocketIO Integration
- `frontend/src/utils/websocket.js` - Client
- `frontend/package.json` - socket.io-client

---

#### 8. Shared Dashboards (Links)
**Beschreibung**: Sharebare Links mit optionaler Auth

**Grafana**: Share Link

**Umsetzung**:
- [ ] Share Token System
- [ ] Public/Private Dashboards
- [ ] Share URL Generation
- [ ] Access Token Management
- [ ] View-Only Mode

**Aufwand**: 4-5 Stunden

**Files**:
- `idm_logger/sharing.py` - Share Tokens
- `idm_logger/web.py` - Share Endpoints
- `frontend/src/views/SharedDashboard.vue` - View Mode

---

### 🟢 Niedrige Priorität (Advanced)

#### 9. Heatmaps
**Beschreibung**: Wärmekarten-Darstellung

**Grafana**: Heatmap Panel

**Umsetzung**:
- [ ] Chart.js Heatmap Adapter
- [ ] HeatmapCard Component
- [ ] Color Scales
- [ ] Time-based Heatmaps

**Aufwand**: 5-6 Stunden

---

#### 10. Table Panel
**Beschreibung**: Tabellarische Darstellung von Daten

**Grafana**: Table Panel

**Umsetzung**:
- [ ] TableCard Component
- [ ] Sortierung, Filterung
- [ ] Pagination
- [ ] Column Configuration

**Aufwand**: 4-5 Stunden

---

#### 11. State Timeline
**Beschreibung**: Zeitstrahl für Status-Verläufe (Heizen/Aus, etc.)

**Grafana**: State Timeline Panel

**Umsetzung**:
- [ ] StateTimelineCard Component
- [ ] State Detection (Wertänderungen)
- [ ] Color Coding (pro Status)
- [ ] Interactive States

**Aufwand**: 5-6 Stunden

---

#### 12. Alert Display im Chart
**Beschreibung**: Alert-Markierungen direkt im Chart anzeigen

**Grafana**: Alert Thresholds

**Umsetzung**:
- [ ] Alert Thresholds in Chart Options
- [ ] Rote/Linie Markierungen
- [ ] Alert History Overlay
- [ ] Click-to-Details

**Aufwand**: 3-4 Stunden

---

## Geplante Releases

### v0.8.0 - Core Features Complete

**Ziel**: 90% Feature-Parität

**Scope**:
- [ ] Annotations
- [ ] Variables/Templates
- [ ] Bar Charts
- [ ] Dashboard Export

**Release**: Q2 2025

---

### v0.9.0 - Advanced Features

**Ziel**: 95% Feature-Parität

**Scope**:
- [ ] Math Queries
- [ ] Custom CSS
- [ ] WebSocket Live
- [ ] Shared Dashboards

**Release**: Q3 2025

---

### v1.0.0 - Feature Complete

**Ziel**: 100% Feature-Parität + Extras

**Scope**:
- [ ] Heatmaps
- [ ] Table Panels
- [ ] State Timeline
- [ ] Alert Display
- [ ] Mobile Apps (iOS/Android)
- [ ] Cloud-Sync

**Release**: Q4 2025

---

## Wie kann ich helfen?

### Quick Wins (2-3 Stunden)

1. **Dashboard Export** - Hoher Impact, einfach zu implementieren
2. **Bar Charts** - Chart.js hat das schon eingebaut
3. **Alert Display** - Nur visuelle Erweiterung

### Weekend Projects (6-8 Stunden)

1. **Variables System** - Sehr nützlich, aber komplexer
2. **WebSocket Live** - Großes Plus für UX
3. **Math Queries** - Mächtig, aber braucht sorgfältige Implementierung

### Week-long Projects

1. **Annotations** - Braucht API + UI + Chart Rendering
2. **Shared Dashboards** - Braucht Auth System + View Mode

---

## Contributing

Jede Hilfe ist willkommen! Schau dir die Issues an oder sprich mich auf Discord an.

**Für Anfänger**:
- Dashboard Export
- Bar Charts
- Alert Display

**Für Fortgeschrittene**:
- Variables System
- WebSocket Integration
- Math Query Parser

**Für Experten**:
- Annotations System
- Sharing/Permissions
- Mobile Apps

---

**Stand**: 2025-01-22
**Version**: 0.7.0
**Nächstes Release**: 0.8.0 (Core Features Complete)
