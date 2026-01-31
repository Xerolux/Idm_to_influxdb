# NIBE S-Serie Modbus-Register

Detaillierte Dokumentation der Modbus-Register für NIBE S-Serie Wärmepumpen (S1155, S1255, S2125, S2145, S2255, S3125, S3155, S3255, S3455).

Letzte Aktualisierung: 31.01.2026

## Grundlagen

### Modbus-Konfiguration
- **Protokoll**: Modbus RTU (RS485) oder TCP (mit Modbus40 Gateway)
- **Baud Rate**: 9600, 19200 (Standard), 38400
- **Data Bits**: 8
- **Stop Bits**: 1
- **Parity**: None
- **Unit ID / Slave ID**: 1-8 (konfigurierbar)
- **Maximale Register pro Sekunde**: 100

### Kommunikation
- **Modbus40**: Kommunikationseinheit für TCP/IP Anbindung
- **SMO S40**: Integriertes Steuermodul mit Modbus-Schnittstelle
- **Maximale Slaves**: 8 im Modbus-Netzwerk

---

## Wichtige Register-Bereiche

### 1. Systemstatus (Adresse 0-99)

| Register | Adresse | Name | Einheit | Typ | Lesen | Schreiben | Beschreibung |
|----------|---------|------|---------|-----|-------|-----------|-------------|
| **SystemOperatingMode** | 0 | Betriebsart | - | UInt16 | ✅ | ❌ | 0=Standby, 1=Heizen, 2=Kühlen, 3=WW, 4=Pool |
| **SystemStatus** | 1 | Systemstatus | - | UInt16 | ✅ | ❌ | Bit-Field für verschiedene Status |
| **FanStatus** | 2 | Lüfterstatus | - | UInt16 | ✅ | ❌ | 0=Aus, 1=An, 2=Auto |
| **CompressorStatus** | 3 | Verdichterstatus | - | UInt16 | ✅ | ❌ | 0=Aus, 1=An (Stufe 1), 2=An (Stufe 2) |
| **AuxHeaterStatus** | 4 | Zusatzheizer | - | UInt16 | ✅ | ❌ | Status des elektrischen Heizstab |
| **BrinePumpStatus** | 5 | Solepumpe | - | UInt16 | ✅ | ❌ | 0=Aus, 1=An |
| **AlarmStatus** | 6 | Alarmstatus | - | UInt16 | ✅ | ❌ | 0=Kein Alarm, >0=Alarm |
| **WarningStatus** | 7 | Warnstatus | - | UInt16 | ✅ | ❌ | Warnungen vorhanden |

### 2. Temperaturen (Adresse 100-299)

| Register | Adresse | Name | Einheit | Typ | Skalierung | Beschreibung |
|----------|---------|------|---------|-----|-----------|-------------|
| **OutdoorTemp** | 100 | Außentemperatur | °C | Int16 | 0.1 | Gemessene Außentemperatur |
| **SupplyTemp** | 101 | Vorlauftemperatur | °C | Int16 | 0.1 | Aktuelle Vorlauftemperatur |
| **ReturnTemp** | 102 | Rücklauftemperatur | °C | Int16 | 0.1 | Aktuelle Rücklauftemperatur |
| **HotWaterChargeTemp** | 103 | WW-Ladetemperatur | °C | Int16 | 0.1 | Temperatur im WW-Speicher oben |
| **HotWaterTopTemp** | 104 | WW oben | °C | Int16 | 0.1 | Temperatur im WW-Speicher unten |
| **BrineInTemp** | 105 | Sole-Eintritt | °C | Int16 | 0.1 | Soletemperatur Verdampfer-Eingang |
| **BrineOutTemp** | 106 | Sole-Austritt | °C | Int16 | 0.1 | Soletemperatur Verdampfer-Ausgang |
| **CondenserTemp** | 107 | Verflüssiger | °C | Int16 | 0.1 | Verflüssigertemperatur |
| **EvaporatorTemp** | 108 | Verdampfer | °C | Int16 | 0.1 | Verdampfertemperatur |
| **ExchangerTemp** | 109 | Wärmetauscher | °C | Int16 | 0.1 | Temperatur Plattenwärmetauscher |
| **AirTemp** | 110 | Lufttemperatur | °C | Int16 | 0.1 | Temperatur Luftansaugung |
| **RoomTemp** | 111 | Raumtemperatur | °C | Int16 | 0.1 | Interne Raumtemperatur |
| **ExhaustTemp** | 112 | Abgastemperatur | °C | Int16 | 0.1 | Temperatur Abluft |
| **DHWTemp** | 113 | DHW-Temperatur | °C | Int16 | 0.1 | Warmwasser-Temperatur (DHW) |
| **CollectorTemp** | 114 | Kollektor | °C | Int16 | 0.1 | Solarkollektor-Temperatur |
| **PoolTemp** | 115 | Pooltemperatur | °C | Int16 | 0.1 | Pool-Wassertemperatur |

### 3. Energiezähler (Adresse 300-399)

| Register | Adresse | Name | Einheit | Typ | Skalierung | Beschreibung |
|----------|---------|------|---------|-----|-----------|-------------|
| **ProducedHeating** | 300 | Erzeugte Wärme | kWh | UInt32 | 1 | Gesamte erzeugte Wärmemenge |
| **ProducedCooling** | 302 | Erzeugte Kühlung | kWh | UInt32 | 1 | Gesamte Kühlleistung |
| **ProducedDHW** | 304 | Erzeugtes WW | kWh | UInt32 | 1 | Gesamte Warmwassermenge |
| **ProducedPool** | 306 | Erzeugter Pool | kWh | UInt32 | 1 | Gesamte Poolwärme |
| **ProducedTotal** | 308 | Erzeugt gesamt | kWh | UInt32 | 1 | Gesamt erzeugte Energie |
| **ConsumedHeating** | 310 | Verbrauch Heizen | kWh | UInt32 | 1 | Energieverbrauch Heizen |
| **ConsumedCooling** | 312 | Verbrauch Kühlen | kWh | UInt32 | 1 | Energieverbrauch Kühlen |
| **ConsumedDHW** | 314 | Verbrauch WW | kWh | UInt32 | 1 | Energieverbrauch Warmwasser |
| **ConsumedPool** | 316 | Verbrauch Pool | kWh | UInt32 | 1 | Energieverbrauch Pool |
| **ConsumedTotal** | 318 | Verbrauch gesamt | kWh | UInt32 | 1 | Gesamt Energieverbrauch |
| **PowerProduced** | 320 | Aktuelle Leistung | kW | UInt16 | 0.1 | Aktuelle erzeugte Leistung |
| **PowerConsumed** | 321 | Aktuelle Verbrauchsleistung | kW | UInt16 | 0.1 | Aktuelle Leistungsaufnahme |

### 4. Betriebsstunden (Adresse 400-499)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **OperatingTimeCompressor** | 400 | Verdichter-Laufzeit | h | UInt32 | Gesamtlaufzeit Verdichter |
| **OperatingTimeBrinePump** | 402 | Solepumpen-Laufzeit | h | UInt32 | Gesamtlaufzeit Solepumpe |
| **OperatingTimeAuxHeater** | 404 | Heizstab-Laufzeit | h | UInt32 | Laufzeit elektrischer Heizstab |
| **OperatingTimeCircPump** | 406 | Umwälzpumpe | h | UInt32 | Laufzeit Umwälzpumpe Heizkreis |
| **OperatingTimeFan** | 408 | Lüfter | h | UInt32 | Laufzeit Lüfter |
| **StartCountCompressor** | 410 | Verdichter-Starts | - | UInt32 | Anzahl Verdichter-Starts |

### 5. Sollwerte (schreibbar!) (Adresse 500-599)

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **SetpointSupplyTemp** | 500 | Vorlauf-Soll | °C | Int16 | 10 | 60 | Sollwert Vorlauftemperatur (schreibbar!) |
| **SetpointRoomTemp** | 501 | Raum-Soll | °C | Int16 | 15 | 25 | Sollwert Raumtemperatur (schreibbar!) |
| **SetpointDHWTemp** | 502 | WW-Soll | °C | Int16 | 40 | 65 | Sollwert Warmwasser (schreibbar!) |
| **SetpointPoolTemp** | 503 | Pool-Soll | °C | Int16 | 20 | 35 | Sollwert Pooltemperatur (schreibbar!) |
| **SetpointCoolingTemp** | 504 | Kühl-Soll | °C | Int16 | 15 | 30 | Sollwert Kühlung (schreibbar!) |
| **CurveHeating** | 505 | Heizkurve | - | UInt16 | 0.1 | 2.5 | Heizkurvensteigung (schreibbar!) |
| **CurveCooling** | 506 | Kühlkurve | - | UInt16 | 0.1 | 2.5 | Kühlkurvensteigung (schreibbar!) |
| **OffsetHeating** | 507 | Heizkurven-Offset | K | Int16 | -5 | +5 | Parallelverschiebung Heizkurve (schreibbar!) |
| **OffsetCooling** | 508 | Kühlkurven-Offset | K | Int16 | -5 | +5 | Parallelverschiebung Kühlkurve (schreibbar!) |

### 6. Smart Grid / PV-Integration (Adresse 600-699)

| Register | Adresse | Name | Einheit | Typ | Lesen | Schreiben | Beschreibung |
|----------|---------|------|---------|-----|-------|-----------|-------------|
| **MaxPowerLimit** | 600 | Max-Leistungsbegrenzung | % | UInt16 | ✅ | ✅ | Maximale Leistung in % (schreibbar!) |
| **ActualPowerLimit** | 601 | Aktuelle Leistungsbegrenzung | % | UInt16 | ✅ | ❌ | Aktuell gesetzte Begrenzung |
| **PVAvailablePower** | 602 | PV-Verfügbar | kW | UInt16 | 0.1 | ✅ | ❌ | Verfügbare PV-Leistung |
| **GridImportPower** | 603 | Netzbezug | kW | UInt16 | 0.1 | ✅ | ❌ | Aktuelle Netzbezug-Leistung |
| **GridExportPower** | 604 | Netzeinspeisung | kW | UInt16 | 0.1 | ✅ | ❌ | Aktuelle Netzeinspeisung |
| **BatterySOC** | 605 | Batterie-SoC | % | UInt16 | ✅ | ❌ | Batterie-Ladezustand |
| **SGReadyStatus** | 606 | SG-Ready Status | - | UInt16 | ✅ | ❌ | Smart Grid Ready Status |
| **PriceSignal** | 607 | Preissignal | - | UInt16 | ✅ | ❌ | Strompreis-Signal (0=Niedrig, 1=Hoch) |
| **OperatingModeSG** | 608 | Betriebsart SG | - | UInt16 | ✅ | ✅ | Smart Grid Betriebsmodus (schreibbar!) |

**Smart Grid Betriebsmodi (Register 608):**
- 0: Normaler Betrieb
- 1: Leistungsbegrenzt aktiv
- 2: PV-Überschuss-Modus
- 3: Sperrmodus (keine Heizung)
- 4: Boost-Modus

### 7. Ventilator-Steuerung (Adresse 700-799)

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **FanSpeedSetpoint** | 700 | Lüfter-Drehzahl Soll | % | UInt16 | 0 | 100 | Sollwert Lüfterdrehzahl (schreibbar!) |
| **FanSpeedActual** | 701 | Lüfter-Drehzahl Ist | % | UInt16 | - | - | Aktuelle Lüfterdrehzahl |
| **FanMode** | 702 | Lüftermodus | - | UInt16 | ✅ | ✅ | 0=Auto, 1=Manuell (schreibbar!) |
| **MinOutdoorTempCooling** | 703 | Min. Außentemp. Kühlung | °C | Int16 | -10 | 20 | Minimale Außentemperatur für Kühlung (schreibbar!) |
| **MaxOutdoorTempHeating** | 704 | Max. Außentemp. Heizen | °C | Int16 | 10 | 35 | Maximale Außentemperatur für Heizen (schreibbar!) |

### 8. Warmwasser-Steuerung (Adresse 800-899)

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **DHWMode** | 800 | WW-Modus | - | UInt16 | ✅ | ✅ | 0=Auto, 1=Manuell (schreibbar!) |
| **DHWSetpoint** | 801 | WW-Solltemperatur | °C | Int16 | ✅ | ✅ | 40 | 65 | Sollwert (schreibbar!) |
| **DHWTemperature** | 802 | WW-Isttemperatur | °C | Int16 | ✅ | ❌ | Aktuelle WW-Temperatur |
| **DHWComfortMode** | 803 | WW-Komfortmodus | - | UInt16 | ✅ | ✅ | 0=Eco, 1=Komfort, 2=Luxus (schreibbar!) |
| **DHWChargingStatus** | 804 | WW-Ladestatus | - | UInt16 | ✅ | ❌ | 0=Idle, 1=Charging, 2=Completed |
| **DHWBoostTime** | 805 | Boost-Startzeit | h | UInt16 | ✅ | ✅ | Stunde für Boost-Funktion (schreibbar!) |
| **DHWBoostDuration** | 806 | Boost-Dauer | min | UInt16 | ✅ | ✅ | Boost-Laufzeit (schreibbar!) |
| **DHWExtraWater** | 807 | Extra-Wasser | l | UInt16 | ✅ | ✅ | Zusätzliches WW-Volumen (schreibbar!) |

### 9. Alarme und Fehler (Adresse 900-999)

| Register | Adresse | Name | Typ | Beschreibung |
|----------|---------|------|-----|-------------|
| **AlarmCode** | 900 | Alarm-Code | UInt16 | Aktueller Alarm-Code |
| **AlarmCount** | 901 | Alarm-Anzahl | UInt16 | Anzahl aktiver Alarme |
| **WarningCode** | 902 | Warn-Code | UInt16 | Warnungs-Code |
| **WarningCount** | 903 | Warn-Anzahl | UInt16 | Anzahl Warnungen |
| **AlarmTop1Code** | 904 | Top-Alarm 1 | UInt16 | Höchster Prioritäts-Alarm |
| **AlarmTop2Code** | 905 | Top-Alarm 2 | UInt16 | Zweithöchster Prioritäts-Alarm |
| **AlarmTop3Code** | 906 | Top-Alarm 3 | UInt16 | Dritthöchster Prioritäts-Alarm |
| **ResetAlarms** | 999 | Alarm quittieren | UInt16 | Schreiben quittiert Alarme |

### 10. PV-Überschuss-Steuerung (EME20 Modul)

Das EME20 Modul ermöglicht PV-Überschuss-Steuerung. Funktioniert über die Smart Grid Register:

| Register | Adresse | Name | Beschreibung |
|----------|---------|------|-------------|
| **MaxPowerLimit** | 600 | Leistungsbegrenzung | Auf 100% = normal, <100% = begrenzt |
| **OperatingModeSG** | 608 | Betriebsart | Auf 2 = PV-Überschuss-Modus |

**Konfiguration für PV-Überschuss:**
1. Register 608 auf Wert 2 setzen (PV-Überschuss-Modus)
2. Register 600 auf gewünschten Maximalwert setzen (z.B. 50%)
3. Die Wärmepumpe reduziert Leistung bei PV-Verfügbarkeit

---

## Wichtige Hinweise

### Adressierung
- Alle Adressen sind **Holding Registers** (Function 03)
- Input Registers (Function 04) werden nicht verwendet
- Register können je nach Modell variieren

### Datentypen
- **UInt16**: Unsigned 16-Bit Integer (0-65535)
- **Int16**: Signed 16-Bit Integer (-32768 bis 32767)
- **UInt32**: Unsigned 32-Bit Integer (0-4294967295)
- Skalierung beachten (z.B. 0.1 für Temperaturen)

### Schreibbare Register
Die wichtigsten schreibbaren Register sind:
- ✅ **500-508**: Solltemperaturen, Heizkurven
- ✅ **600**: Maximalleistung (Smart Grid)
- ✅ **608**: Smart Grid Betriebsmodus
- ✅ **700-704**: Lüftersteuerung
- ✅ **800-807**: Warmwasser-Steuerung

### Diagnose
- Register 900-906 für Alarmüberwachung
- Register 999 zum Quittieren von Alarmen
- NIBE MyUplink für detaillierte Fehleranalyse

---

## NIBE Modelle mit Modbus

| Modell | Serie | Modbus | Bemerkungen |
|-------|-------|--------|-------------|
| **S1155** | S-Serie | Optional | Modbus40 erforderlich |
| **S1255** | S-Serie | Optional | Modbus40 erforderlich |
| **S2125** | S-Serie | Optional | Modbus40 erforderlich |
| **S2145** | S-Serie | Optional | Modbus40 erforderlich |
| **S2255** | S-Serie | Optional | Modbus40 erforderlich |
| **S3125** | S-Serie | Optional | Modbus40 erforderlich |
| **S3155** | S-Serie | Optional | Modbus40 erforderlich |
| **S3255** | S-Serie | Optional | Modbus40 erforderlich |
| **S3455** | S-Serie | Optional | Modbus40 erforderlich |

### Modbus40 Modul
- Ermöglicht TCP/IP Anbindung
- Bis zu 8 Slaves möglich
- Maximal 100 Register pro Sekunde

---

## Nützliche Links

- [NIBE Modbus S-Series Documentation](https://installer.nibe.eu/download/18.47aa975e18a8b43315f342b/1696946128872/Modbus%20Register%20S-Series.pdf)
- [NIBE Modbus Register PDF](https://nibe.ua/document_search/file?test=/files/3/documents/MODBUS%20S%20%D1%81%D0%B5%D1%80%D0%B8%D1%8F%20(en).pdf)
- [Home Assistant NIBE Modbus](https://community.home-assistant.io/t/modbus-configuration-for-nibe-s-series-heatpumps/400422)
- [GitHub: nibe-s1255-modbus](https://github.com/henningms/nibe-s1255-modbus)
- [Loxone NIBE S-Series](https://api.library.loxone.com/downloader/file/1885/Modbus%20S-Series.pdf)

---

**Version**: 1.0
**Letztes Update**: 31.01.2026
**Maintainer**: Xerolux
**Projekt**: [idm-metrics-collector](https://github.com/Xerolux/idm-metrics-collector)
