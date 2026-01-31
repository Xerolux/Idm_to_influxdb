# Bosch / Buderus Modbus-Register

Detaillierte Dokumentation der Modbus-Register für Bosch Compress und Buderus Logamatic Wärmepumpen-Steuerungen.

Letzte Aktualisierung: 31.01.2026

## Grundlagen

### Modbus-Konfiguration
- **Protokoll**: Modbus TCP über Logamatic 5000 / Control 8000
- **Port**: 502 (Standard)
- **Unit ID**: 1
- **Byte Order**: Big-Endian
- **Word Order**: Big-Endian

### Kommunikation
- **EMS (Energy Management System)**: Primäres Protokoll für Bosch/Buderus
- **Logamatic 5000**: Steuerung mit integriertem Modbus TCP Gateway (ab Version 1.3.x)
- **Control 8000**: Modulare Steuerung mit Modbus TCP Support
- **EMS-ESP**: Open-Source Gateway für EMS zu Modbus-Konvertierung

### Wichtiger Hinweis
**Bosch/Buderus Wärmepumpen verwenden primär das EMS-Protokoll, kein direktes Modbus!**
Für Modbus-Zugriff wird eines der folgenden Gateways benötigt:
- Logamatic 5000 / Control 8000 Controller (integriertes Modbus TCP)
- EMS-ESP Gateway (EMS → Modbus Konvertierung)
- KNX Gateway mit Modbus-Support

---

## Wichtige Register-Bereiche (Logamatic 5000 / Control 8000)

### 1. Systemstatus (Adresse 0-99)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **Status** | 0 | Systemstatus | - | UInt16 | Hauptstatus der Heizungsanlage |
| **OperatingMode** | 1 | Betriebsart | - | UInt16 | 0=Standby, 1=Heizen, 2=WW, 3=Kühlen |
| **ErrorState** | 2 | Fehlerzustand | - | UInt16 | 0=Kein Fehler, >0=Fehler aktiv |
| **WarningState** | 3 | Warnzustand | - | UInt16 | Warnungs-Flags |

### 2. Temperaturen (Adresse 100-299)

| Register | Adresse | Name | Einheit | Typ | Skalierung | Beschreibung |
|----------|---------|------|---------|-----|-----------|-------------|
| **OutdoorTemp** | 100 | Außentemperatur | °C | Int16 | 0.1 | Gemessene Außentemperatur (T1) |
| **SupplyTemp** | 102 | Vorlauftemperatur | °C | Int16 | 0.1 | Aktuelle Vorlauftemperatur (T0) |
| **ReturnTemp** | 103 | Rücklauftemperatur | °C | Int16 | 0.1 | Aktuelle Rücklauftemperatur (TC0) |
| **DHWTemp** | 104 | Warmwasser | °C | Int16 | 0.1 | Warmwasser-Temperatur (TW1) |
| **DHWTempTop** | 105 | WW oben | °C | Int16 | 0.1 | Warmwasser-Temperatur oben (TW2) |
| **FlowTemp** | 106 | Heizkreis-Vorlauf | °C | Int16 | 0.1 | Vorlauf Heizkreis 1 |
| **ReturnTempHC** | 107 | Heizkreis-Rücklauf | °C | Int16 | 0.1 | Rücklauf Heizkreis 1 |
| **RoomTemp1** | 108 | Raumtemperatur 1 | °C | Int16 | 0.1 | Raumtemperatur HK 1 |
| **RoomTemp2** | 109 | Raumtemperatur 2 | °C | Int16 | 0.1 | Raumtemperatur HK 2 |
| **BrineInTemp** | 110 | Sole-Eintritt | °C | Int16 | 0.1 | Soletemperatur Eingang (TB0) |
| **BrineOutTemp** | 111 | Sole-Austritt | °C | Int16 | 0.1 | Soletemperatur Ausgang (TB1) |
| **CondenserTemp** | 112 | Verflüssiger | °C | Int16 | 0.1 | Verflüssigertemperatur (TC3) |
| **EvaporatorTemp** | 113 | Verdampfer | °C | Int16 | 0.1 | Verdampfertemperatur |
| **HotGasTemp** | 114 | Heißgas | °C | Int16 | 0.1 | Heißgastemperatur (TR6) |

### 3. Leistung und Energie (Adresse 300-399)

| Register | Adresse | Name | Einheit | Typ | Beschreibung |
|----------|---------|------|---------|-----|-------------|
| **CurrentPower** | 300 | Aktuelle Leistung | kW | Float32 | Aktuelle elektrische Leistung |
| **ThermalPower** | 302 | Thermische Leistung | kW | Float32 | Aktuelle thermische Leistung |
| **EnergyHeating** | 304 | Wärme Heizen | kWh | Float32 | Gesamte Wärmemenge Heizen |
| **EnergyCooling** | 306 | Wärme Kühlen | kWh | Float32 | Gesamte Wärmemenge Kühlen |
| **EnergyDHW** | 308 | Wärme WW | kWh | Float32 | Gesamte Wärmemenge Warmwasser |
| **EnergyTotal** | 310 | Wärme gesamt | kWh | Float32 | Gesamt erzeugte Wärmemenge |

### 4. Sollwerte (schreibbar!) (Adresse 500-599)

| Register | Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|---------|------|---------|-----|-----|-----|-------------|
| **SetpointRoomTemp1** | 500 | Raum-Soll HK1 | °C | Int16 | 15 | 25 | Raumtemperatur HK1 (schreibbar!) |
| **SetpointRoomTemp2** | 501 | Raum-Soll HK2 | °C | Int16 | 15 | 25 | Raumtemperatur HK2 (schreibbar!) |
| **SetpointDHWTemp** | 502 | WW-Soll | °C | Int16 | 45 | 65 | Warmwasser-Soll (schreibbar!) |
| **SetpointSupplyTemp** | 503 | Vorlauf-Soll | °C | Int16 | 20 | 70 | Vorlauf-Sollwert (schreibbar!) |
| **CurveHeating** | 504 | Heizkurve | - | Float32 | 0.2 | 2.5 | Heizkurvensteigung (schreibbar!) |
| **CurveOffset** | 505 | Heizkurven-Offset | K | Float32 | -5 | +5 | Parallelverschiebung (schreibbar!) |

### 5. Betriebsarten (schreibbar!) (Adresse 600-699)

| Register | Adresse | Name | Typ | Werte | Beschreibung |
|----------|---------|------|-----|-------|-------------|
| **OperatingMode** | 600 | Betriebsart | UInt16 | 0=Auto, 1=Heizen, 2=WW, 3=Kühlen, 4=Standby | Hauptbetriebsart (schreibbar!) |
| **DHWMode** | 601 | WW-Modus | UInt16 | 0=Auto, 1=Manuell, 2=Boost | WW-Modus (schreibbar!) |
| **CoolingMode** | 602 | Kühlmodus | UInt16 | 0=Aus, 1=Auto, 2=Manuell | Kühlbetrieb (schreibbar!) |
| **HolidayMode** | 603 | Urlaubsmodus | UInt16 | 0=Aus, 1=Ein | Urlaubsmodus (schreibbar!) |

### 6. Pumpen und Ventile (Adresse 700-799)

| Register | Adresse | Name | Typ | Beschreibung |
|----------|---------|------|-----|-------------|
| **CircPumpStatus** | 700 | Umwälzpumpe | UInt16 | 0=Aus, 1=An |
| **CircPumpSpeed** | 701 | Pumpendrehzahl | % | UInt16 | Umwälzpumpen-Drehzahl |
| **BrinePumpStatus** | 702 | Solepumpe | UInt16 | Status der Solepumpe |
| **ValveHeating** | 703 | Ventil Heizen | UInt16 | Ventilstatus Heizung |
| **ValveDHW** | 704 | Ventil WW | UInt16 | Ventilstatus Warmwasser |
| **DiverterValve** | 705 | 3-Wege-Ventil | UInt16 | 0=Heizen, 1=WW |

### 7. Warmwasser-Steuerung (Adresse 800-899)

| Register | Adresse | Name | Einheit | Typ | Lesen | Schreiben | Beschreibung |
|----------|---------|------|---------|-----|-------|-----------|-------------|
| **DHWTemperature** | 800 | WW-Temperatur | °C | Int16 | ✅ | ❌ | Aktuelle WW-Temperatur |
| **DHWSetpoint** | 801 | WW-Soll | °C | Int16 | ✅ | ✅ | 45-65 | Sollwert (schreibbar!) |
| **DHWStatus** | 802 | WW-Status | - | UInt16 | ✅ | ❌ | 0=Bereit, 1=Laden |
| **DHWBoostTime** | 803 | Boost-Zeit | h | UInt16 | ✅ | ✅ | Startzeit (schreibbar!) |
| **DHWTempTop** | 804 | WW-Temperatur oben | °C | Int16 | ✅ | ❌ | Oberer Sensor (TW2) |

### 8. Smart Grid / PV-Integration (Adresse 900-999)

| Register | Adresse | Name | Einheit | Typ | Lesen | Schreiben | Beschreibung |
|----------|---------|------|---------|-----|-------|-----------|-------------|
| **SGReadyStatus** | 900 | SG-Ready | - | UInt16 | ✅ | ❌ | Smart Grid Ready Status |
| **PowerLimit** | 901 | Leistungsbegrenzung | % | UInt16 | ✅ | ✅ | Max-Leistung (schreibbar!) |
| **PVAvailablePower** | 902 | PV-Verfügbar | kW | Float32 | ✅ | ❌ | Verfügbare PV-Leistung |
| **GridPower** | 903 | Netzleistung | kW | Float32 | ✅ | ❌ | Netzbezug/-einspeisung |
| **OperatingModeSG** | 904 | SG-Betriebsart | - | UInt16 | ✅ | ✅ | Smart Grid Modus (schreibbar!) |

**Smart Grid Betriebsmodi (Register 904):**
- 0: Normaler Betrieb
- 1: Leistungsreduktion
- 2: PV-Optimierter Betrieb
- 3: Sperrmodus

---

## EMS-Protokoll Register (Compress 7000i, 7800i, etc.)

Die meisten Bosch Compress Wärmepumpen verwenden das proprietäre EMS-Protokoll. Für Modbus-Zugriff muss ein Gateway (z.B. EMS-ESP) verwendet werden.

### Wichtige EMS-Typen (für EMS-ESP)

| EMS-Typ | Name | Beschreibung |
|---------|------|-------------|
| **0x10** | HeatPump | Wärmepumpen-Hauptgerät |
| **0x11** | HeatPump-Cooling | Kühlung |
| **0x12** | HeatPump-Pool | Poolheizung |
| **0x16** | Solar | Solar-Modul |
| **0x17** | Controller | Steuerung (RC300, RC310) |
| **0x18** | Gateway | Gateway (KM200, KM100) |
| **0x19** | Connect | EasyConnect |
| **0x20** | HeatPump | Wärmepumpe (neu) |
| **0x21** | Hybrid | Hybrid-Wärmepumpe |
| **0x23** | HeatPump | Wärmepumpe (neueste Generation) |
| **0x26** | HeatPump-Aux | Zusatzheizer |
| **0x27** | HPModule | Erweitertes HP-Modul |
| **0x29** | Pool | Pool-Modul |
| **0x2A** | Solar | Solar-Modul (neu) |
| **0x34** | Boiler | Warmwasserspeicher |
| **0x38** | MixingModule | Mischmodul (MM100) |
| **0x48** | Controller | RC300, RC310 |
| **0x49** | Remote | Fernbedienung |
| **0x57** | Switch | Schalter |
| **0x59** | Wireless | Funkmodul |
| **0x9B** | HeatPump | Wärmepumpe (ext) |

### EMS-Register (Beispiele für Compress 7000i/7800i)

**Temperaturen:**
- **TB0**: Sole-Eintrittstemperatur (Brine In)
- **TB1**: Sole-Austrittstemperatur (Brine Out)
- **TC0**: Rücklauftemperatur (Return)
- **TC1**: Vorlauftemperatur (Supply)
- **TC3**: Verflüssigertemperatur (Condenser)
- **T0**: Heizkreis-Vorlauf
- **T1**: Außentemperatur
- **TW1**: Warmwassertemperatur
- **TW2**: Warmwasser oben
- **TR1**: Kompressortemperatur
- **TR6**: Heißgastemperatur
- **JR0**: Niederdruck
- **JR1**: Hochdruck

---

## Wichtige Hinweise

### Bosch vs. Buderus
- **Bosch Compress** und **Buderus Logamatic** verwenden die gleiche Technologie
- Beide Marken gehören zur Bosch Thermotechnology
- EMS-Protokoll ist bei beiden identisch

### Modbus vs. EMS
- **Direkter Modbus-Zugriff**: Nur mit Logamatic 5000/Control 8000 Controller
- **EMS-Protokoll**: Standard für Bosch Compress und Buderus Wärmepumpen
- **Gateway erforderlich**: EMS-ESP, KM200, oder ähnliches für Modbus-Konvertierung

### Schreibbare Register
Die wichtigsten schreibbaren Register sind:
- ✅ **500-505**: Raum-, WW-, Vorlauf-Sollwerte, Heizkurven
- ✅ **600-603**: Betriebsarten, Urlaubsmodus
- ✅ **801, 803**: Warmwasser-Soll und Boost-Zeit
- ✅ **901, 904**: Smart Grid-Leistungsbegrenzung und Modus

### Fehler-Codes (Bosch Compress 7000i/7800i)

| Fehler-Code | Beschreibung | Typ |
|-------------|-------------|-----|
| **5201** | Außentemperatur T1 offen | Info |
| **5202** | Außentemperatur T1 Kurzschluss | Info |
| **5203** | Außentemperatur T1 defekt | Alarm |
| **5204** | Vorlauftemperatur T0 offen | Info |
| **5205** | Vorlauftemperatur T0 Kurzschluss | Info |
| **5206** | Vorlauftemperatur T0 defekt | Alarm |
| **5237** | Warmwasser TW1 offen | Info |
| **5238** | Warmwasser TW1 Kurzschluss | Info |
| **5239** | Warmwasser TW1 defekt | Alarm |
| **5246** | Überhitzungsschutz E2 ausgelöst | Alarm |
| **5271** | Heizkreis 1 hohe Vorlauftemperatur | Alarm |
| **5276** | Druck im Solekreis zu niedrig | Alarm |
| **5294** | Kondensationswächter ausgelöst | Info |
| **5295** | Kondensationswächter Alarm | Alarm |
| **5298** | Hochdruck JR1 Warnung | Info |
| **5299** | Hochdruck JR1 Alarm | Alarm |
| **5310** | Heißgas TR6 zu hoch | Info |
| **5311** | Heißgas TR6 zu hoch Alarm | Alarm |
| **5507** | MR1 Hochdruck Warnung | Info |
| **5508** | MR1 Hochdruck Alarm | Alarm |
| **5514** | Verdichtungsdruck JR0 zu niedrig | Info |
| **5547** | Sole-Eintritt TB0 zu niedrig | Info |
| **5549** | Sole-Eintritt TB0 zu niedrig Alarm | Alarm |
| **5563** | Hohe Temperaturdifferenz TB0-TB1 | Info |
| **5565** | Hohe Temperaturdifferenz TB0-TB1 Alarm | Alarm |
| **5917** | Keine Kommunikation Heizungspumpe PC0 | Alarm |
| **5918** | Durchfluss Heizungspumpe PC0 zu niedrig | Alarm |
| **6219** | Wartung fällig (Kunde) | Info |
| **6220** | Wartung fällig (Installateur) | Info |

---

## Modelle mit Modbus/EMS

### Bosch Compress Serie
- **Compress 2000 AWF**: Luft/Wasser
- **Compress 3000 AWF**: Luft/Wasser (neuer)
- **Compress 6000 AWF**: Luft/Wasser (leistungsfähig)
- **Compress 7000i**: Sole/Wasser
- **Compress 7000i AW**: Luft/Wasser
- **Compress 7800i**: Sole/Wasser (Top-Modell)
- **Compress 7800i AW**: Luft/Wasser (Top-Modell)

### Buderus Logamatic
- **Logamatic 5000**: Mit Modbus TCP Gateway (ab Version 1.3.x)
- **Control 8000**: Modulare Steuerung mit Modbus
- **RC300**: EMS-Steuerung (kein direkter Modbus)
- **RC310**: EMS-Steuerung (kein direkter Modbus)

### Bosch/Buderus Modelle
- **Logatherm**: Serie für Luft/Wasser und Sole/Wasser
- **Supra**: Serie für High-Performance Wärmepumpen
- **Geo**: Serie für Geothermie

### Gateways für Modbus
- **Logamatic 5000**: Integriertes Modbus TCP Gateway
- **Control 8000**: Integriertes Modbus TCP Gateway
- **KM200**: LAN-Gateway mit EMS-Zugang
- **EMS-ESP**: Open-Source EMS → Modbus Gateway
- **KNX Gateway**: Mit Modbus-Support

---

## Nützliche Links

- [Bosch Compress 7000i Dokumentation](https://www.bosch-thermotechnology.com)
- [Buderus Logamatic 5000 Manual](https://www.manualslib.com/manual/2142722/Bosch-Buderus-Logamatic-5000-Series.html)
- [EMS-ESP Project](https://github.com/emsesp/EMS-ESP32)
- [Loxone Buderus Library](https://library.loxone.com/detail/buderus-logamatic-5000-1445/overview)
- [Bosch Control 8000 Technical Guide](https://www.bosch-industrial.com/global/en/ocs/commercial-industrial/control-8000-system-and-boiler-control-unit-758987-p/)
- [EVCC Bosch Heat Pump Integration](https://docs.evcc.io/en/docs/devices/heating)
- [Home Assistant Bosch Integration](https://community.home-assistant.io/t/bosch-compress-heat-pump-integration/115579)

---

## Empfehlung für die Integration

### Für Direct Modbus-Zugriff
Verwende **Logamatic 5000** oder **Control 8000** Controller mit integriertem Modbus TCP Gateway.

### Für EMS-Protokoll
Verwende **EMS-ESP** Gateway für Konvertierung von EMS zu Modbus oder MQTT.

### Für Home Assistant
- [Bosch-home-assistant-bosch-custom-component](https://github.com/bosch-thermostat/home-assistant-bosch-custom-component)
- [EMS-ESP Home Assistant Integration](https://github.com/emsesp/EMS-ESP32)

### Für Loxone
- [Buderus Logamatic 5000 Template](https://library.loxone.com/detail/buderus-logamatic-5000-1445/overview)

---

**Version**: 1.0
**Letztes Update**: 31.01.2026
**Maintainer**: Xerolux
**Projekt**: [idm-metrics-collector](https://github.com/Xerolux/idm-metrics-collector)
