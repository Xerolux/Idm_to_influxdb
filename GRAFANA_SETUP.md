# Grafana Dashboard Setup - Heizkreis A und COP

Diese Anleitung zeigt, wie Sie Heizkreis A und COP-Werte in Grafana als Diagramme visualisieren.

## Voraussetzungen

- InfluxDB läuft und sammelt Daten
- Grafana ist installiert und mit InfluxDB verbunden
- Port 3001 ist für Grafana konfiguriert

## 1. COP (Coefficient of Performance) Diagramm

### Was ist COP?
Der COP zeigt die Effizienz der Wärmepumpe: Verhältnis von abgegebener Wärmeenergie zu aufgenommener elektrischer Energie.

### COP berechnen in Grafana

**Query für COP-Berechnung:**
```flux
from(bucket: "idm_metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "heat_pump")
  |> filter(fn: (r) =>
      r["_field"] == "power_current" or
      r["_field"] == "energy_heat_total"
  )
  |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> map(fn: (r) => ({
      r with
      cop: if r.power_current > 0.0 then r.energy_heat_total / r.power_current else 0.0
  }))
  |> keep(columns: ["_time", "cop"])
```

**Panel-Einstellungen:**
- **Panel Type**: Time series
- **Title**: "COP (Coefficient of Performance)"
- **Y-Axis Label**: "COP"
- **Unit**: none
- **Min**: 0
- **Max**: 10 (typisch 2-6 für Wärmepumpen)
- **Graph Style**: Lines
- **Color**: Grün (gute Effizienz), Gelb (mittelmäßig), Rot (schlecht)

### Thresholds für COP:
- **Rot** (< 2.5): Schlechte Effizienz
- **Gelb** (2.5 - 3.5): Mittlere Effizienz
- **Grün** (> 3.5): Gute Effizienz

---

## 2. Heizkreis A - Vollständige Visualisierung

### Panel 1: Heizkreis A - Vorlauftemperaturen

**Query:**
```flux
from(bucket: "idm_metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "heat_pump")
  |> filter(fn: (r) =>
      r["_field"] == "temp_flow_current_circuit_a" or
      r["_field"] == "temp_flow_target_circuit_a"
  )
```

**Panel-Einstellungen:**
- **Title**: "Heizkreis A - Vorlauftemperaturen"
- **Y-Axis**: °C
- **Legend**:
  - `temp_flow_current_circuit_a` → "Ist-Temperatur"
  - `temp_flow_target_circuit_a` → "Soll-Temperatur"
- **Colors**: Ist = Blau, Soll = Orange gestrichelt

---

### Panel 2: Heizkreis A - Raumtemperaturen

**Query:**
```flux
from(bucket: "idm_metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "heat_pump")
  |> filter(fn: (r) =>
      r["_field"] == "temp_room_circuit_a" or
      r["_field"] == "temp_room_target_heating_normal_circuit_a" or
      r["_field"] == "temp_room_target_heating_eco_circuit_a"
  )
```

**Panel-Einstellungen:**
- **Title**: "Heizkreis A - Raumtemperaturen"
- **Y-Axis**: °C
- **Legend**:
  - `temp_room_circuit_a` → "Ist-Temperatur"
  - `temp_room_target_heating_normal_circuit_a` → "Soll Normal"
  - `temp_room_target_heating_eco_circuit_a` → "Soll Eco"

---

### Panel 3: Heizkreis A - Heizkurve und Offset

**Query:**
```flux
from(bucket: "idm_metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "heat_pump")
  |> filter(fn: (r) =>
      r["_field"] == "curve_circuit_a" or
      r["_field"] == "curve_offset_a"
  )
```

**Panel-Einstellungen:**
- **Title**: "Heizkreis A - Heizkurve & Parallelverschiebung"
- **Y-Axis**: Mixed (Kurve: keine Einheit, Offset: °C)
- **Legend**:
  - `curve_circuit_a` → "Heizkurve"
  - `curve_offset_a` → "Parallelverschiebung (°C)"

---

### Panel 4: Heizkreis A - Betriebsmodus

**Query:**
```flux
from(bucket: "idm_metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "heat_pump")
  |> filter(fn: (r) =>
      r["_field"] == "mode_circuit_a" or
      r["_field"] == "mode_active_circuit_a"
  )
```

**Panel-Einstellungen:**
- **Panel Type**: State timeline (oder Time series mit steps)
- **Title**: "Heizkreis A - Betriebsmodus"
- **Value Mappings**:
  - `mode_circuit_a`: 0=OFF, 1=TIMED, 2=NORMAL, 3=ECO, 4=MANUAL_HEAT, 5=MANUAL_COOL
  - `mode_active_circuit_a`: 0=OFF, 1=HEATING, 2=COOLING

---

## 3. Empfohlenes Dashboard-Layout

```
┌─────────────────────────────────────────────────────┐
│  COP (Coefficient of Performance)                   │
│  [Zeitreihen-Diagramm mit Threshold-Colors]        │
└─────────────────────────────────────────────────────┘

┌──────────────────────────┬──────────────────────────┐
│  HK A - Vorlauftemps     │  HK A - Raumtemps        │
│  [Ist vs Soll]           │  [Ist, Normal, Eco]      │
└──────────────────────────┴──────────────────────────┘

┌──────────────────────────┬──────────────────────────┐
│  HK A - Heizkurve        │  HK A - Betriebsmodus    │
│  [Kurve + Offset]        │  [Timeline/Status]       │
└──────────────────────────┴──────────────────────────┘
```

## 4. Zusätzliche Panels (Optional)

### Kühlbetrieb Heizkreis A
```flux
from(bucket: "idm_metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "heat_pump")
  |> filter(fn: (r) =>
      r["_field"] == "temp_room_target_cooling_normal_circuit_a" or
      r["_field"] == "temp_room_target_cooling_eco_circuit_a" or
      r["_field"] == "temp_flow_target_cooling_circuit_a"
  )
```

### Schwellenwerte Heizkreis A
```flux
from(bucket: "idm_metrics")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "heat_pump")
  |> filter(fn: (r) =>
      r["_field"] == "temp_threshold_heating_circuit_a" or
      r["_field"] == "temp_threshold_cooling_circuit_a"
  )
```

---

## 5. Alerting (Optional)

### Alert für niedrigen COP
Wenn der COP über längere Zeit < 2.0 ist, könnte ein Problem vorliegen.

**Alert Rule:**
- **Condition**: `avg() of query(COP) < 2.0`
- **For**: 30 Minuten
- **Severity**: Warning

### Alert für Heizkreis A Abweichung
Wenn Ist-Temperatur > 5°C von Soll-Temperatur abweicht.

---

## 6. Dashboard exportieren

Wenn Sie ein Dashboard erstellt haben:
1. Dashboard → Share → Export → Save to file
2. Datei: `grafana-dashboard-heizkreis-a-cop.json`
3. In Projekt speichern für andere Benutzer

---

## Tipps

1. **Zeitbereich**: Verwenden Sie „Last 24 hours" für Tagesverlauf, „Last 7 days" für Wochentrend
2. **Auto-Refresh**: 30s oder 1m für Live-Monitoring
3. **Variables**: Erstellen Sie Dashboard-Variable für Heizkreis (A, B, C...) um zwischen Heizkreisen zu wechseln
4. **Mobile**: Grafana-Dashboards sind responsive und funktionieren auf Smartphones
