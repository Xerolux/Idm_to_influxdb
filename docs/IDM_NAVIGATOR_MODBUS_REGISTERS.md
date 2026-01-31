# IDM Navigator 2.0 Modbus-Register

Detaillierte Dokumentation aller lesbaren und schreibbaren Modbus-Register der IDM Navigator 2.0 Wärmepumpen-Serie.

Letzte Aktualisierung: 31.01.2026

## Grundlagen

### Modbus-Parameter
- **Protokoll**: Modbus TCP
- **Unit ID**: 1
- **Port**: 502 (Standard)
- **Byte Order**: Big-Endian
- **Word Order**: Little-Endian
- **Datentypen**:
  - Float32: 2 Register (4 Bytes)
  - Int16/UInt16: 1 Register (2 Bytes)
  - Int32/UInt32: 2 Register (4 Bytes)
  - Enum: UInt16 mit vordefinierten Werten
  - BitField: UInt16 mit Flags

### Register-Adressbereiche
| Bereich | Adressen | Beschreibung |
|---------|----------|-------------|
| **Power Management** | 74-86 | Leistung, Batterie, PV-Überschuss |
| **Temperaturen** | 1000-1099 | Außentemperatur, Speicher, Wärmequelle |
| **Status** | 1100-1199 | Systemstatus, Fehler, Ventile, Pumpen |
| **Heizkreise** | 1350-1650 | Heizkreis A-G (je 2 Offset pro HK) |
| **Zonen** | 2000+ | Zonenmodule (je 65 Register pro Zone) |
| **Energie** | 1748-1799 | Energiezähler (kWh) |
| **Leistung** | 1790-1820 | Aktuelle Leistungsaufnahme (kW) |
| **Solar** | 1850-1899 | Solar-Kollektor, Ladung |
| **Kaskade** | 1200-1231 | Kaskaden-Steuerung |
| **Smart Grid** | 1710-1722 | Externe Steuerung, GLT |

---

## 1. Power Management (74-86)

### Lesbar + Schreibbar

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **power_solar_surplus** | 74 | PV-Überschuss | kW | Float32 | -10 | 10 | Verfügbarer PV-Überschuss (nur schreiben) |
| **power_resistive_heater** | 76 | Heizstableistung | kW | Float32 | 0 | - | Aktuelle Leistung des Heizstabs |
| **power_solar_production** | 78 | PV-Produktion | kW | Float32 | 0 | - | Aktuelle PV-Leistung (write-only für Steuerung) |
| **power_use_house** | 82 | Hausverbrauch | kW | Float32 | 0 | - | Aktueller Verbrauch (write-only) |
| **power_drain_battery** | 84 | Batterieentladung | kW | Float32 | 0 | - | Batterie-Entladeleistung (write-only) |
| **charge_state_battery** | 86 | Batterie-SoC | % | UInt16 | 0 | 100 | Batterie-Ladezustand (write-only) |

**Hinweise**:
- Register 74, 78, 82, 84, 86 sind **nur schreibbar** für Smart-Grid-Steuerung
- Diese werden verwendet, um die Wärmepumpe in ein Energemanagement-System einzubinden

---

## 2. Temperaturen (1000-1099)

### 2.1 Außentemperatur

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **temp_outside** | 1000 | Außentemperatur | °C | Float32 | Gemessene Außentemperatur |
| **temp_outside_avg** | 1002 | Außentemperatur gemittelt | °C | Float32 | Gemittelte Außentemperatur |

### 2.2 Speichertemperaturen

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **temp_heat_storage** | 1008 | Pufferspeicher oben | °C | Float32 | Temperatur im warmen Teil des Pufferspeichers |
| **temp_cold_storage** | 1010 | Pufferspeicher unten | °C | Float32 | Temperatur im kalten Teil des Pufferspeichers |
| **temp_water_heater_bottom** | 1012 | Warmwasser unten | °C | Float32 | Temperatur im Warmwasserspeicher unten |
| **temp_water_heater_top** | 1014 | Warmwasser oben | °C | Float32 | Temperatur im Warmwasserspeicher oben |
| **temp_water_heater_tap** | 1030 | Warmwasser Zapfung | °C | Float32 | Temperatur am Warmwasser-Entnahmestellen |

### 2.3 Warmwasser-Sollwerte (schreibbar!)

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **temp_water_target** | 1032 | WW-Solltemperatur | °C | UInt16 | 5 | 95 | Sollwert für Warmwasser |
| **temp_water_switch_on** | 1033 | WW-Einschaltschwelle | °C | UInt16 | 5 | 95 | Temperatur zum Einschalten der Ladung |
| **temp_water_switch_off** | 1034 | WW-Ausschaltschwelle | °C | UInt16 | 5 | 95 | Temperatur zum Ausschalten der Ladung |

### 2.4 Wärmequelle

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **temp_heat_pump_flow** | 1050 | WP-Vorlauf | °C | Float32 | Vorlauftemperatur der Wärmepumpe |
| **temp_heat_pump_return** | 1052 | WP-Rücklauf | °C | Float32 | Rücklauftemperatur der Wärmepumpe |
| **temp_hgl_flow** | 1054 | Heizkreis-Vorlauf | °C | Float32 | Vorlauftemperatur Heizkreis |
| **temp_heat_source_input** | 1056 | Quellen-Eingang | °C | Float32 | Temperatur Wärmequelle Eingang |
| **temp_heat_source_output** | 1058 | Quellen-Ausgang | °C | Float32 | Temperatur Wärmequelle Ausgang |

### 2.5 Lufttemperaturen (bei Luft-Wasser-WP)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **temp_air_input** | 1060 | Luft-Eingang | °C | Float32 | Außluft-Eintrittstemperatur |
| **temp_air_heat_exchanger** | 1062 | Luft-Wärmetauscher | °C | Float32 | Temperatur nach Wärmetauscher |
| **temp_air_input_2** | 1064 | Luft-Eingang 2 | °C | Float32 | Temperatur zweite Luftstufe |
| **temp_charge_sensor** | 1066 | Ladungstemperatur | °C | Float32 | Temperatur am Lade_sensor |

### 2.6 Feuchtigkeit und Preis

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **humidity** | 1392 | Luftfeuchtigkeit | % | Float32 | Relative Luftfeuchtigkeit |
| **price_energy** | 1048 | Strompreis | EUR | Float32 | Aktueller Strompreis (scale: 0.001) |

---

## 3. Status und Fehler (1004-1200)

### 3.1 Systemstatus

| Register | Adresse | Name | Typ | Werte | Beschreibung |
|----------|---------|------|-----|-------|-------------|
| **failure_id** | 1004 | Fehlernummer | UInt16 | - | Aktuelle Fehlernummer |
| **status_system** | 1005 | Systemstatus | Enum | 0=Init, 1=Standby, 2=Heizen, 3=Kühlen, 4=WW, 5=Defrost | Hauptstatus (schreibbar!) |
| **status_smart_grid** | 1006 | Smart Grid Status | Enum | 0=Off, 1=On | Smart-Grid-Aktivierung |

### 3.2 Wärmepumpen-Status (BitField)

| Register | Adresse | Name | Typ | Flags | Beschreibung |
|----------|---------|------|-----|-------|-------------|
| **status_heat_pump** | 1090 | WP-Status | BitField | Siehe Tabelle unten | Kombinierte Status-Bits |

**HeatPumpStatus Flags:**
```
Bit 0: Compressor 1
Bit 1: Compressor 2
Bit 2: Compressor 3
Bit 3: Compressor 4
Bit 4: Second Heat Source
Bit 5: Defrost Active
Bit 6: Circulation Pump
Bit 7: Heating Mode
Bit 8: Cooling Mode
Bit 9: DHW Mode
Bit 10: Pool Mode
```

### 3.3 Anforderungs-Flags

| Register | Adresse | Name | Typ | Beschreibung |
|----------|---------|------|-----|-------------|
| **request_heating** | 1091 | Heiz-Anforderung | UInt16 | >0 = Heizung wird angefordert |
| **request_cooling** | 1092 | Kühl-Anforderung | UInt16 | >0 = Kühlung wird angefordert |
| **request_water_status** | 1093 | WW-Anforderung | UInt16 | >0 = Warmwasser wird angefordert |
| **evu_lock_status** | 1098 | EVU-Sperre | UInt16 | Status der EVU-Sperre (Stromversorger) |
| **failure_heat_pump** | 1099 | WP-Fehler | UInt16 | >0 = Fehler vorhanden |

### 3.4 Kompressor- und Pumpenstatus

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **state_compressor_1_uchar** | 1100 | Kompressor 1 | - | UInt16 | -1 | 100 | Drehzahl oder Status (0=Aus, >0=An) |
| **state_compressor_2_uchar** | 1101 | Kompressor 2 | - | UInt16 | -1 | 100 | Drehzahl oder Status |
| **state_compressor_3_uchar** | 1102 | Kompressor 3 | - | UInt16 | -1 | 100 | Drehzahl oder Status |
| **state_compressor_4_uchar** | 1103 | Kompressor 4 | - | UInt16 | -1 | 100 | Drehzahl oder Status |
| **state_charge_pump** | 1104 | Ladepumpe | % | Int16 | -1 | 100 | Leistung in % |
| **state_brine_pump** | 1105 | Solepumpe | % | Int16 | -1 | 100 | Leistung in % |
| **state_ground_water_pump** | 1106 | Grundwasserpumpe | % | Int16 | -1 | 100 | Leistung in % |
| **load_isc_cold_storage_pump** | 1108 | ISC-Kühlpumpe | % | Int16 | 0 | 100 | Belastung in % |
| **load_isc_recooling_pump** | 1109 | ISC-Nachkühlpumpe | % | Int16 | 0 | 100 | Belastung in % |

### 3.5 Ventilzustände (Enums)

| Register | Adresse | Name | Typ | Werte | Beschreibung |
|----------|---------|------|-----|-------|-------------|
| **valve_state_circuit_heating_cooling** | 1110 | Ventil HK Heiz/Kühl | Enum | 0=Heizen, 1=Kühlen, 2=Neutral | Heizkreis-Ventilposition |
| **valve_state_storage_heating_cooling** | 1111 | Ventil Speicher Heiz/Kühl | Enum | 0=Heizen, 1=Kühlen, 2=Neutral | Speicher-Ventilposition |
| **valve_state_main_heating_water** | 1112 | Hauptventil Heiz/WW | Enum | 0=Heizen, 1=WW, 2=Neutral | Hauptventil-Position |
| **valve_state_source_heating_cooling** | 1113 | Ventil Quelle Heiz/Kühl | Enum | 0=Heizen, 1=Kühlen, 2=Neutral | Quellenventil-Position |
| **valve_state_solar_heating_water** | 1114 | Solarventil Heiz/WW | Enum | 0=Heizen, 1=WW, 2=Neutral | Solarventil-Position |
| **valve_state_solar_storage_source** | 1115 | Solarventil Speicher/Quelle | Enum | 0=Speicher, 1=Quelle, 2=Neutral | Solar-Ventilposition |
| **valve_state_isc_heating_cooling** | 1116 | ISC-Ventil Heiz/Kühl | Enum | 0=Heizen, 1=Kühlen, 2=Neutral | ISC-Ventilposition |
| **valve_state_isc_bypass** | 1117 | ISC-Bypassventil | Enum | 0=Offen, 1=Teilweise, 2=Geschlossen | Bypass-Ventilposition |

### 3.6 Sonstige Statuswerte

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **pump_circulation** | 1118 | Zirkulationspumpe | - | Int16 | Status der Zirkulationspumpe |
| **status_bivalence** | 1124 | Bivalenz-Status | UInt16 | Status des Bivalenz-Systems |

### 3.7 Bivalenz-Temperaturen

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **temp_second_source_bivalence_1** | 1120 | 2. Quelle Bivalenz 1 | °C | Int16 | -50 | 50 | Temperaturgrenze Bivalenz 1 |
| **temp_second_source_bivalence_2** | 1121 | 2. Quelle Bivalenz 2 | °C | Int16 | -50 | 50 | Temperaturgrenze Bivalenz 2 |
| **temp_third_source_bivalence_1** | 1122 | 3. Quelle Bivalenz 1 | °C | Int16 | -50 | 50 | Temperaturgrenze Bivalenz 1 |
| **temp_third_source_bivalence_2** | 1123 | 3. Quelle Bivalenz 2 | °C | Int16 | -30 | 40 | Temperaturgrenze Bivalenz 2 |

---

## 4. Kaskaden-Steuerung (1200-1231)

### 4.1 Kaskaden-Stufen

| Register | Adresse | Name | Typ | Beschreibung |
|----------|---------|------|-----|-------------|
| **cascade_available_stages_heating** | 1147 | Verfügbare Stufen Heizung | UInt16 | Anzahl verfügbarer Heizstufen |
| **cascade_available_stages_cooling** | 1148 | Verfügbare Stufen Kühlung | UInt16 | Anzahl verfügbarer Kühlstufen |
| **cascade_available_stages_water** | 1149 | Verfügbare Stufen WW | UInt16 | Anzahl verfügbarer WW-Stufen |
| **cascade_running_stages_heating** | 1150 | Laufende Stufen Heizung | UInt16 | Anzahl aktiver Heizstufen |
| **cascade_running_stages_cooling** | 1151 | Laufende Stufen Kühlung | UInt16 | Anzahl aktiver Kühlstufen |
| **cascade_running_stages_water** | 1152 | Laufende Stufen WW | UInt16 | Anzahl aktiver WW-Stufen |

### 4.2 Kaskaden-Temperaturen

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **cascade_request_heating_temp** | 1200 | Kaskade Heizanforderung | °C | Float32 | Angeforderte Heiztemperatur |
| **cascade_request_cooling_temp** | 1202 | Kaskade Kühl-Anforderung | °C | Float32 | Angeforderte Kühltemperatur |
| **cascade_temp_request_water** | 1204 | Kaskade WW-Anforderung | °C | Float32 | Angeforderte WW-Temperatur |
| **cascade_temp_flow_avg_heating** | 1206 | Kaskade Mittelwert Heizung | °C | Float32 | Gemittelte Vorlauftemperatur Heizung |
| **cascade_temp_flow_avg_cooling** | 1208 | Kaskade Mittelwert Kühlung | °C | Float32 | Gemittelte Vorlauftemperatur Kühlung |
| **cascade_avg_flow_temp_c_water** | 1210 | Kaskade Mittelwert WW | °C | Float32 | Gemittelte Vorlauftemperatur WW |

### 4.3 Kaskaden-Leistung (schreibbar!)

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **cascade_min_power_heating** | 1220 | Kaskade Min-Leistung Heiz | % | UInt16 | 0 | 100 | Minimale Leistung Heizung (%) |
| **cascade_max_power_heating** | 1221 | Kaskade Max-Leistung Heiz | % | UInt16 | 0 | 100 | Maximale Leistung Heizung (%) |
| **cascade_min_power_cooling** | 1222 | Kaskade Min-Leistung Kühl | % | UInt16 | 0 | 100 | Minimale Leistung Kühlung (%) |
| **cascade_max_power_cooling** | 1223 | Kaskade Max-Leistung Kühl | % | UInt16 | 0 | 100 | Maximale Leistung Kühlung (%) |
| **cascade_min_power_water** | 1224 | Kaskade Min-Leistung WW | % | UInt16 | 0 | 100 | Minimale Leistung WW (%) |
| **cascade_max_power_water** | 1225 | Kaskade Max-Leistung WW | % | UInt16 | 0 | 100 | Maximale Leistung WW (%) |

### 4.4 Kaskaden-Bivalenz-Grenzen

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **cascade_bivalence_heating_parallel** | 1226 | Bivalenz Heiz Parallel | °C | Int16 | Parallel-Bivalenz-Grenze Heizung |
| **cascade_bivalence_heating_alternative** | 1227 | Bivalenz Heiz Alternativ | °C | Int16 | Alternativ-Bivalenz-Grenze Heizung |
| **cascade_bivalence_cooling_parallel** | 1228 | Bivalenz Kühl Parallel | °C | Int16 | Parallel-Bivalenz-Grenze Kühlung |
| **cascade_bivalence_cooling_alternative** | 1229 | Bivalenz Kühl Alternativ | °C | Int16 | Alternativ-Bivalenz-Grenze Kühlung |
| **cascade_bivalence_water_parallel** | 1230 | Bivalenz WW Parallel | °C | Int16 | Parallel-Bivalenz-Grenze WW |
| **cascade_bivalence_water_alternative** | 1231 | Bivalenz WW Alternativ | °C | Int16 | Alternativ-Bivalenz-Grenze WW |

---

## 5. Heizkreise (1350-1650)

Jeder Heizkreis (A-G) hat die folgenden Register. Der Offset berechnet sich wie folgt:
- Heizkreis A: Offset +0
- Heizkreis B: Offset +2
- Heizkreis C: Offset +4
- ...
- Heizkreis G: Offset +12

### 5.1 Heizkreis-Temperaturen

| Register | Adresse (HK A) | Name | Einheit | Typ | Beschreibung |
|----------|---------------|------|---------|-----|-------------|
| **temp_flow_current_circuit_a** | 1350 | Vorlauf Ist | °C | Float32 | Aktuelle Vorlauftemperatur |
| **temp_room_circuit_a** | 1364 | Raumtemperatur | °C | Float32 | Aktuelle Raumtemperatur |
| **temp_flow_target_circuit_a** | 1378 | Vorlauf Soll | °C | Float32 | Sollwert Vorlauftemperatur |

### 5.2 Heizkreis-Modus (schreibbar!)

| Register | Adresse (HK A) | Name | Typ | Werte | Beschreibung |
|----------|---------------|------|-----|-------|-------------|
| **mode_circuit_a** | 1393 | Betriebsart | Enum | 0=Auto, 1=Reduziert, 2=Normal, 3=Aus | Heizkreis-Betriebsart |

**CircuitMode Enum:**
```
0: AUTO - Automatischer Betrieb
1: REDUCED - Reduzierter Betrieb (Night Setback)
2: NORMAL - Normalbetrieb (Comfort)
3: OFF - Ausgeschaltet
```

### 5.3 Heizkreis-Solltemperaturen (schreibbar!)

| Register | Adresse (HK A) | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------------|------|---------|-----|-----|-----|-------------|
| **temp_room_target_heating_normal_circuit_a** | 1401 | Raum-Soll Normal | °C | Float32 | -10 | 80 | Normale Raumtemperatur (Komfort) |
| **temp_room_target_heating_eco_circuit_a** | 1415 | Raum-Soll Eco | °C | Float32 | -10 | 80 | Reduzierte Raumtemperatur (Absenkung) |
| **curve_circuit_a** | 1429 | Heizkurve | - | Float32 | - | - | Heizkurvensteigung |
| **temp_threshold_heating_circuit_a** | 1442 | Heizgrenze | °C | UInt16 | -10 | 80 | Außentemperatur-Grenze für Heizen |
| **temp_flow_target_constant_circuit_a** | 1449 | Konstante Vorlauf-Soll | °C | UInt16 | 5 | 95 | Fester Vorlauf-Sollwert |
| **temp_room_target_cooling_normal_circuit_a** | 1457 | Kühl-Soll Normal | °C | Float32 | -10 | 80 | Normale Kühltemperatur |
| **temp_room_target_cooling_eco_circuit_a** | 1471 | Kühl-Soll Eco | °C | Float32 | -10 | 80 | Reduzierte Kühltemperatur |
| **temp_threshold_cooling_circuit_a** | 1484 | Kühl-Grenze | °C | UInt16 | -10 | 80 | Außentemperatur-Grenze für Kühlen |
| **temp_flow_target_cooling_circuit_a** | 1491 | Kühl-Vorlauf-Soll | °C | UInt16 | 5 | 95 | Kühl-Vorlauf-Sollwert |

### 5.4 Heizkreis-Aktivmodus (schreibbar!)

| Register | Adresse (HK A) | Name | Typ | Werte | Beschreibung |
|----------|---------------|------|-----|-------|-------------|
| **mode_active_circuit_a** | 1498 | Aktiver Modus | Enum | 0=Heizen, 1=Kühlen, 2=WW, 3=Pool | Aktueller Betriebsmodus |

**ActiveCircuitMode Enum:**
```
0: HEATING - Heizen aktiv
1: COOLING - Kühlen aktiv
2: WATER - Warmwasserbereitung aktiv
3: POOL - Poolheizung aktiv
```

### 5.5 Heizkurve (schreibbar!)

| Register | Adresse (HK A) | Name | Einheit | Typ | Beschreibung |
|----------|---------------|------|---------|-----|-------------|
| **curve_offset_a** | 1505 | Heizkurven-Offset | °C | UInt16 | Parallelverschiebung der Heizkurve |

---

## 6. Smart Grid / Externe Steuerung (1690-1722)

### 6.1 Externe Sensoren

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **temp_external_outdoor** | 1690 | Ext. Außentemp. | °C | Float32 | Externe Außentemperatur (schreibbar!) |
| **temp_external_humidity** | 1692 | Ext. Feuchte | % | Float32 | Externe Luftfeuchtigkeit (schreibbar!) |
| **temp_external_request_heating** | 1694 | Ext. Heizanforderung | °C | UInt16 | Externe Heizanforderung (schreibbar!) |
| **temp_external_request_cooling** | 1695 | Ext. Kühl-Anforderung | °C | UInt16 | Externe Kühl-Anforderung (schreibbar!) |

### 6.2 GLT-Steuerung (Gebäudeleittechnik)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **temp_request_glt_heizen** | 1696 | GLT Heizanforderung | °C | Float32 | Von GLT angeforderte Heiztemperatur (schreibbar!) |
| **temp_request_glt_kuehlen_100** | 1698 | GLT Kühl-Anforderung (x100) | °C | Float32 | Von GLT angeforderte Kühltemperatur (skaliert x100, schreibbar!) |
| **request_pump_ground_water_external** | 1714 | GLT Grundwasserpumpe | UInt16 | Externe Anforderung Grundwasserpumpe (schreibbar!) |
| **request_pump_ground_water_max_external** | 1715 | GLT Max. Grundwasserpumpe | UInt16 | Externe Maximalwert Grundwasserpumpe (schreibbar!) |

### 6.3 Speicher-Sollwerte für GLT (schreibbar!)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **temp_heat_storage_glt** | 1716 | Pufferspeicher-Soll GLT | °C | Float32 | Von GLT angeforderter Speicher-Sollwert |
| **temp_cold_storage_glt** | 1718 | Kaltsp.-Soll GLT | °C | Float32 | Von GLT angeforderter Kaltsp.-Sollwert |
| **temp_water_heater_bottom_target_glt** | 1720 | WW-unten-Soll GLT | °C | Float32 | Von GLT angeforderter WW-Sollwert unten |
| **temp_water_heater_top_target_glt** | 1722 | WW-oben-Soll GLT | °C | Float32 | Von GLT angeforderter WW-Sollwert oben |

---

## 7. Energiezähler (1748-1799)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **energy_heat_heating** | 1748 | Wärmemenge Heizen | kWh | Float32 | Gesamte Wärmemenge für Heizen |
| **energy_heat_total** | 1750 | Wärmemenge gesamt | kWh | Float32 | Gesamte erzeugte Wärmemenge |
| **energy_heat_total_cooling** | 1752 | Wärmemenge Kühlen | kWh | Float32 | Wärmemenge für Kühlung |
| **energy_heat_total_water** | 1754 | Wärmemenge WW | kWh | Float32 | Wärmemenge für Warmwasser |
| **energy_heat_total_defrost** | 1756 | Wärmemenge Abtauung | kWh | Float32 | Energie für Abtauung |
| **energy_heat_total_passive_cooling** | 1758 | Passive Kühlung | kWh | Float32 | Passive Kühlung |
| **energy_heat_total_solar** | 1760 | Solar-Wärme | kWh | Float32 | Aus Solar gewonnene Wärme |
| **energy_heat_total_electric** | 1762 | Elektro-Heizung | kWh | Float32 | Elektrische Heizleistung (Heizstab) |
| **energy_heat_total_flow_sensor** | 4128 | Durchflussmenge | kWh | Float32 | Energie nach Durchflusssensor |

---

## 8. Leistungsaufnahme (1790-1820)

| Register | Adresse | Name | Einheit | Typ | Min | Beschreibung |
|----------|---------|------|---------|-----|-----|-------------|
| **power_current** | 1790 | Aktuelle Leistung | kW | Float32 | 0 | Aktuelle elektrische Leistungsaufnahme |
| **power_current_solar** | 1792 | PV-Leistung aktuell | kW | Float32 | - | Aktuelle PV-Erzeugung |
| **power_current_draw** | 4122 | Leistungsaufnahme | kW | Float32 | 0 | Aktuelle Gesamtleistungsaufnahme |
| **power_thermal** | 4126 | Thermische Leistung | kW | Float32 | - | Aktuelle thermische Leistung |

---

## 9. Solar (1850-1899)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **temp_solar_collector** | 1850 | Solarkollektor | °C | Float32 | Temperatur im Solarkollektor |
| **temp_solar_collector_return** | 1852 | Solarrücklauf | °C | Float32 | Temperatur im Solarrücklauf |
| **temp_solar_charge** | 1854 | Solarladung | °C | Float32 | Temperatur am Solarlade_sensor |
| **mode_solar** | 1856 | Solar-Modus | Enum | Solar-Betriebsart |
| **temp_solar_reference** | 1857 | Solar-Referenz | °C | Float32 | Referenztemperatur für Solar |

**SolarMode Enum:**
```
0: OFF - Ausgeschaltet
1: AUTO - Automatischer Betrieb
2: MANUAL - Manueller Betrieb
3: BOOST - Boost-Modus
```

---

## 10. Eis-Speicher-Kühler (ISC) (1870-1874)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **temp_isc_charge_cooling** | 1870 | ISC-Ladekühlung | °C | Float32 | Temperatur bei ISC-Ladekühlung |
| **temp_isc_recooling** | 1872 | ISC-Nachkühlung | °C | Float32 | Temperatur bei ISC-Nachkühlung |
| **mode_isc** | 1874 | ISC-Modus | BitField | ISC-Betriebsmodus (Flags) |

**IscMode BitField:**
```
Bit 0: Cooling Active
Bit 1: Charging Active
Bit 2: Recooling Active
Bit 3: Storage Active
```

---

## 11. Diagnose (1999)

| Register | Adresse | Name | Typ | Beschreibung |
|----------|---------|------|-----|-------------|
| **acknowledge_faults** | 1999 | Fehler quittieren | UInt16 | Schreiben quittiert Fehler |

---

## 12. Anforderungs-Register (schreibbar!) (1710-1713)

| Register | Adresse | Name | Typ | Beschreibung |
|----------|---------|------|-----|-------------|
| **request_heating** | 1710 | Heizung anfordern | Binary | TRUE = Heizen anfordern |
| **request_cooling** | 1711 | Kühlen anfordern | Binary | TRUE = Kühlen anfordern |
| **request_water** | 1712 | WW anfordern | Binary | TRUE = Warmwasser anfordern |
| **request_water_once** | 1713 | WW einmal anfordern | Binary | TRUE = Einmalige WW-Bereitung |

---

## 13. Zonenmodule (2000+)

Für jede Zone (0-9) sind folgende Register verfügbar:

**Basisadresse = 2000 + (Zone × 65)**

### 13.1 Zone-Modus

| Register | Offset | Name | Typ | Beschreibung |
|----------|--------|------|-----|-------------|
| **mode_zone_X** | +0 | Zonenmodus | Enum | Modus der Zone |

**ZoneMode Enum:**
```
0: OFF - Aus
1: AUTO - Automatisch
2: MANUAL - Manuell
3: VACATION - Urlaubsmodus
```

### 13.2 Raum-Parameter (je Zone bis zu 9 Räume)

Für jeden Raum (1-9) in einer Zone sind folgende Register verfügbar:

**Offset pro Raum = 2 + (Raum × 7)**

| Register | Offset | Name | Einheit | Typ | Beschreibung |
|----------|--------|------|---------|-----|-------------|
| **temp_room_zone_X_room_Y** | +0 | Raumtemperatur | °C | Float32 | Aktuelle Raumtemperatur |
| **temp_target_zone_X_room_Y** | +2 | Raum-Solltemperatur | °C | Float32 | Sollwert (schreibbar!) |
| **humidity_zone_X_room_Y** | +4 | Raumfeuchte | % | UInt16 | Relative Luftfeuchtigkeit |
| **mode_zone_X_room_Y** | +5 | Raummodus | Enum | Raum-Modus (schreibbar!) |
| **relay_zone_X_room_Y** | +6 | Relais | UInt16 | Relais-Status |

**RoomMode Enum:**
```
0: OFF - Aus
1: AUTO - Automatisch
2: MANUAL - Manuell
3: COMFORT - Komfort
4: ECO - Eco
5: ABSENT - Abwesend
```

### 13.3 Zone-Entfeuchter

| Register | Offset | Name | Typ | Beschreibung |
|----------|--------|------|-----|-------------|
| **dehumidifier_zone_X** | +1 | Entfeuchter | UInt16 | Status des Entfeuchters |

### 13.4 Zone-Relais

| Register | Offset | Name | Typ | Beschreibung |
|----------|--------|------|-----|-------------|
| **relay_zone_X_room_9** | +64 | Relais Raum 9 | UInt16 | Relais-Status Raum 9 |

---

## Zusammenfassung der schreibbaren Register

### Temperatur-Sollwerte (gesetzt durch User/Smart Home)
- `temp_water_target` (1032) - Warmwasser-Solltemperatur
- `temp_water_switch_on` (1033) - WW-Einschalttemperatur
- `temp_water_switch_off` (1034) - WW-Ausschalttemperatur
- `temp_room_target_heating_normal_circuit_A-G` (1401+) - Raum-Soll Normal
- `temp_room_target_heating_eco_circuit_A-G` (1415+) - Raum-Soll Eco
- `temp_room_target_cooling_normal_circuit_A-G` (1457+) - Kühl-Soll Normal
- `temp_room_target_cooling_eco_circuit_A-G` (1471+) - Kühl-Soll Eco
- `temp_target_zone_X_room_Y` - Zonen-Raum-Sollwerte

### Betriebsarten-Steuerung
- `status_system` (1005) - Systemstatus (Heizen/Kühlen/Standby)
- `mode_circuit_A-G` (1393+) - Heizkreis-Modus
- `mode_active_circuit_A-G` (1498+) - Aktiver Modus
- `mode_zone_X` - Zonenmodus
- `mode_zone_X_room_Y` - Raummodus

### Kaskaden-Leistung
- `cascade_min_power_heating` (1220) - Minimale Heizleistung %
- `cascade_max_power_heating` (1221) - Maximale Heizleistung %
- `cascade_min_power_cooling` (1222) - Minimale Kühlleistung %
- `cascade_max_power_cooling` (1223) - Maximale Kühlleistung %
- `cascade_min_power_water` (1224) - Minimale WW-Leistung %
- `cascade_max_power_water` (1225) - Maximale WW-Leistung %

### Smart Grid / PV-Steuerung
- `power_solar_surplus` (74) - PV-Überschuss
- `power_solar_production` (78) - PV-Produktion
- `power_use_house` (82) - Hausverbrauch
- `power_drain_battery` (84) - Batterieentladung
- `charge_state_battery` (86) - Batterie-SoC

### Externe Steuerung
- `temp_external_outdoor` (1690) - Externe Außentemperatur
- `temp_external_request_heating` (1694) - Externe Heizanforderung
- `temp_external_request_cooling` (1695) - Externe Kühl-Anforderung

### GLT-Steuerung
- `temp_request_glt_heizen` (1696) - GLT Heizanforderung
- `temp_request_glt_kuehlen_100` (1698) - GLT Kühl-Anforderung
- `request_pump_ground_water_external` (1714) - GLT Grundwasserpumpe
- `request_pump_ground_water_max_external` (1715) - GLT Maximalwert

### Anforderungs-Register
- `request_heating` (1710) - Heizung anfordern (Binary)
- `request_cooling` (1711) - Kühlen anfordern (Binary)
- `request_water` (1712) - Warmwasser anfordern (Binary)
- `request_water_once` (1713) - Warmwasser einmal anfordern (Binary)

### Diagnose
- `acknowledge_faults` (1999) - Fehler quittieren

---

## Tipps für die Integration

### Empfohlene Lesezyklen
- **Temperaturen und Leistung**: Alle 1-5 Sekunden
- **Energiezähler**: Alle 60 Sekunden
- **Status und Fehler**: Alle 10 Sekunden
- **Zonen**: Alle 5-10 Sekunden

### Bulk-Reading optimieren
Die IDM Navigator unterstützt optimiertes Bulk-Reading:
- Blöcke mit konsekutiven Adressen werden in einem Request gelesen
- Bei "Illegal Data Address" Fehlern werden einzelne Register gelesen
- Konfiguration der Zonen und Heizkreise reduziert Requests

### Wichtige Hinweise
1. **Nicht alle Register sind schreibbar!** Prüfe `supported_features` im Code
2. **Einige Register sind EEPROM-sensitiv** - nicht zu oft schreiben!
3. **System-Register (1005)** nur ändern, wenn du weißt was du tust
4. **Fehler quittieren** nur nach Analyse der Fehlerursache

---

**Version**: 1.0
**Letztes Update**: 31.01.2026
**Projekt**: [idm-metrics-collector](https://github.com/Xerolux/idm-metrics-collector)
**Maintainer**: Xerolux
