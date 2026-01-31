# Alpha Innotec / Stiebel Eltron Modbus-Register

Detaillierte Dokumentation der Modbus-Register für Stiebel Eltron und Alpha Innotec Wärmepumpen mit ISG Web-Steuerung.

Letzte Aktualisierung: 31.01.2026

## Grundlagen

### Modbus-Konfiguration
- **Protokoll**: Modbus TCP über ISG Web
- **Port**: 502 (Standard)
- **Unit ID**: 1
- **Byte Order**: Big-Endian
- **Word Order**: Big-Endian

### ISG Web
- **ISG Web**: Integrierte Steuerung mit Web-Oberfläche
- **Modbus**: TCP/IP-Schnittstelle für Gebäudeautomation
- **Zugriff**: Lokal oder über Internet (Cloud)

---

## Wichtige Register-Bereiche

### 1. Systemstatus (ISG Adressen)

| Register | ISG-Adresse | Name | Einheit | Typ | Beschreibung |
|----------|-------------|------|---------|-----|-------------|
| **Status** | 0 | Systemstatus | - | UInt16 | Hauptstatus der Wärmepumpe |
| **OperationMode** | 1 | Betriebsart | - | UInt16 | 0=Heizen, 1=Kühlen, 2=WW, 3=Standby |
| **CompressorStatus** | 2 | Verdichterstatus | - | UInt16 | Bit-Field für Verdichter-Stufen |
| **FanStatus** | 3 | Lüfterstatus | - | UInt16 | Lüfterstatus |
| **DefrostStatus** | 4 | Abtaustatus | - | UInt16 | Abtau-Status |
| **AlarmStatus** | 5 | Alarmstatus | - | UInt16 | Bit-Field für Alarme |

### 2. Temperaturen (ISG Adressen)

| Register | ISG-Adresse | Name | Einheit | Typ | Skalierung | Beschreibung |
|----------|-------------|------|---------|-----|-----------|-------------|
| **OutdoorTemp** | 100 | Außentemperatur | °C | Float32 | 1.0 | Gemessene Außentemperatur |
| **SupplyTemp** | 101 | Vorlauftemperatur | °C | Float32 | 1.0 | Aktuelle Vorlauftemperatur |
| **ReturnTemp** | 102 | Rücklauftemperatur | °C | Float32 | 1.0 | Aktuelle Rücklauftemperatur |
| **DHWTemp** | 103 | Warmwasser | °C | Float32 | 1.0 | Warmwasser-Temperatur |
| **DHWChargeTemp** | 104 | WW-Ladetemp. | °C | Float32 | 1.0 | Temperatur WW-Speicher oben |
| **DHWBottomTemp** | 105 | WW unten | °C | Float32 | 1.0 | Temperatur WW-Speicher unten |
| **SourceTempIn** | 106 | Quellen-Eingang | °C | Float32 | 1.0 | Wärmequelle Eingang |
| **SourceTempOut** | 107 | Quellen-Ausgang | °C | Float32 | 1.0 | Wärmequelle Ausgang |
| **RoomTemp** | 108 | Raumtemperatur | °C | Float32 | 1.0 | Interne Raumtemperatur |
| **Humidity** | 109 | Luftfeuchtigkeit | % | Float32 | 1.0 | Relative Luftfeuchtigkeit |

### 3. Leistung und Energie (ISG Adressen)

| Register | ISG-Adresse | Name | Einheit | Typ | Beschreibung |
|----------|-------------|------|---------|-----|-------------|
| **CurrentPower** | 200 | Aktuelle Leistung | kW | Float32 | Aktuelle elektrische Leistung |
| **ThermalPower** | 202 | Thermische Leistung | kW | Float32 | Aktuelle thermische Leistung |
| **EnergyHeating** | 204 | Wärme Heizen | kWh | Float32 | Gesamte Wärmemenge Heizen |
| **EnergyCooling** | 206 | Wärme Kühlen | kWh | Float32 | Gesamte Wärmemenge Kühlen |
| **EnergyDHW** | 208 | Wärme WW | kWh | Float32 | Gesamte Wärmemenge Warmwasser |
| **EnergyTotal** | 210 | Wärme gesamt | kWh | Float32 | Gesamt erzeugte Wärmemenge |
| **PowerConsumption** | 212 | Verbrauch | kWh | Float32 | Elektrische Arbeit gesamt |

### 4. Sollwerte (schreibbar!) (ISG Adressen)

| Register | ISG-Adresse | Name | Einheit | Typ | Min | Max | Beschreibung |
|----------|-------------|------|---------|-----|-----|-----|-------------|
| **SetpointRoomTemp** | 300 | Raum-Soll | °C | Float32 | 15 | 25 | Raumtemperatur (schreibbar!) |
| **SetpointDHWTemp** | 301 | WW-Soll | °C | Float32 | 45 | 65 | Warmwasser-Soll (schreibbar!) |
| **SetpointSupplyTemp** | 302 | Vorlauf-Soll | °C | Float32 | 20 | 70 | Vorlauf-Soll (schreibbar!) |
| **CurveHeating** | 303 | Heizkurve | - | Float32 | 0.2 | 2.5 | Heizkurve (schreibbar!) |
| **CurveCooling** | 304 | Kühlkurve | - | Float32 | 0.2 | 2.5 | Kühlkurve (schreibbar!) |
| **SetbackTemp** | 305 | Absenktemp. | °C | Float32 | 10 | 20 | Nachtabsenkung (schreibbar!) |

### 5. Betriebsarten (schreibbar!) (ISG Adressen)

| Register | ISG-Adresse | Name | Typ | Werte | Beschreibung |
|----------|-------------|------|-----|-------|-------------|
| **OperationMode** | 400 | Betriebsart | UInt16 | 0=Heizen, 1=Kühlen, 2=WW, 3=Auto | Hauptbetriebsart (schreibbar!) |
| **DHWMode** | 401 | WW-Modus | UInt16 | 0=Auto, 1=Manuell, 2=Boost | WW-Modus (schreibbar!) |
| **CoolingMode** | 402 | Kühlmodus | UInt16 | 0=Aus, 1=Auto, 2=Manuell | Kühlbetrieb (schreibbar!) |
| **SilentMode** | 403 | Silent-Modus | UInt16 | 0=Aus, 1=Ein, 2=Auto | Silent-/Nachtmodus (schreibbar!) |
| **VacationMode** | 404 | Urlaubsmodus | UInt16 | 0=Aus, 1=Ein | Urlaubsmodus (schreibbar!) |
| **PartyMode** | 405 | Party-Modus | UInt16 | 0=Aus, 1=Ein | Party-Modus (schreibbar!) |

### 6. Pumpen und Ventile (ISG Adressen)

| Register | ISG-Adresse | Name | Typ | Beschreibung |
|----------|-------------|------|-----|-------------|
| **CircPumpStatus** | 500 | Umwälzpumpe | UInt16 | 0=Aus, 1=An |
| **CircPumpSpeed** | 501 | Pumpendrehzahl | UInt16 | Umwälzpumpen-Drehzahl |
| **SourcePumpStatus** | 502 | Quellenpumpe | UInt16 | Status Quellenpumpe |
| **BrinePumpStatus** | 503 | Solepumpe | UInt16 | Status Solepumpe |
| **ValveHeating** | 504 | Ventil Heizen | UInt16 | Ventilstatus Heizung |
| **ValveCooling** | 505 | Ventil Kühlen | UInt16 | Ventilstatus Kühlung |
| **ValveDHW** | 506 | Ventil WW | UInt16 | Ventilstatus Warmwasser |
| **ValveSolar** | 507 | Ventil Solar | UInt16 | Ventilstatus Solar |

### 7. Solar-Register (ISG Adressen)

| Register | ISG-Adresse | Name | Einheit | Typ | Beschreibung |
|----------|-------------|------|---------|-----|-------------|
| **SolarTempCollector** | 600 | Kollektortemp. | °C | Float32 | Solarkollektor-Temperatur |
| **SolarTempReturn** | 601 | Solar-Rücklauf | °C | Float32 | Solar-Rücklauftemperatur |
| **SolarStatus** | 602 | Solar-Status | UInt16 | 0=Aus, 1=Laden, 2=Entladen |
| **SolarPower** | 603 | Solar-Leistung | kW | Float32 | Aktuelle Solarleistung |
| **SolarEnergy** | 604 | Solar-Energie | kWh | Float32 | Gesamte Solar-Energie |

### 8. Smart Grid / PV-Integration (ISG Adressen)

| Register | ISG-Adresse | Name | Einheit | Typ | Lesen | Schreiben | Beschreibung |
|----------|-------------|------|---------|-----|-------|-----------|-------------|
| **SGReadyStatus** | 700 | SG-Ready | UInt16 | ✅ | ❌ | Smart Grid Ready Status |
| **PowerLimit** | 701 | Leistungsbegrenzung | % | UInt16 | ✅ | ✅ | Max-Leistung (schreibbar!) |
| **PVAvailablePower** | 702 | PV-Verfügbar | kW | Float32 | ✅ | ❌ | Verfügbare PV-Leistung |
| **GridPower** | 703 | Netzleistung | kW | Float32 | ✅ | ❌ | Netzbezug/-einspeisung |
| **PriceSignal** | 704 | Preissignal | UInt16 | ✅ | ❌ | Strompreis-Signal |
| **OperatingModeSG** | 705 | SG-Betriebsart | UInt16 | ✅ | ✅ | Smart Grid Modus (schreibbar!) |

### 9. Fehler und Alarme (ISG Adressen)

| Register | ISG-Adresse | Name | Typ | Beschreibung |
|----------|-------------|------|-----|-------------|
| **ErrorCode** | 800 | Fehler-Code | UInt16 | Aktueller Fehler-Code |
| **ErrorText** | 801-810 | Fehlertext | String | Fehlerbeschreibung |
| **WarningCode** | 811 | Warn-Code | UInt16 | Warnungs-Code |
| **WarningText** | 812-821 | Warn-Text | String | Warnungsbeschreibung |
| **ResetError** | 899 | Fehler quittieren | UInt16 | Schreiben quittiert Fehler |

---

## ISG Web Besonderheiten

### ISG Web Adressierung
- Die Adressen oben sind **ISG-intern** (nicht Modbus-Adressen!)
- ISG verwendet eigene Adressierung für interne Variablen
- Modbus-Zugriff erfolgt über Mapping-Tabelle

### Typische ISG zu Modbus Mapping
```
ISG 0 → Modbus 1000 (Systemstatus)
ISG 100 → Modbus 1100 (Temperaturen)
ISG 200 → Modbus 1200 (Leistung)
ISG 300 → Modbus 1300 (Sollwerte)
ISG 400 → Modbus 1400 (Betriebsarten)
```

**Hinweis**: Die genaue Adressierung kann je nach ISG-Version variieren!

### Schreibbare Register
Die wichtigsten schreibbaren Register sind:
- ✅ **300-305**: Raum-, WW-, Vorlauf-Sollwerte
- ✅ **400-405**: Betriebsarten (Heizen, Kühlen, Silent, Vacation, Party)
- ✅ **701, 705**: Smart Grid-Leistungsbegrenzung und Modus

### Luxtronik-Besonderheiten
- Alpha Innotec verwendet die gleiche ISG-Technologie wie Stiebel Eltron
- Die Register sind daher identisch
- Luxtronik-Steuerung ist in den meisten Alpha Innotec Modellen integriert

---

## Modelle mit ISG Web Modbus

### Stiebel Eltron
- **WPL A Serie**: WPL 07 A, WPL 13 A, WPL 15 A, WPL 25 A
- **WPL 20 Serie**: WPL 20 A, WPL 25 I
- **WPL 12 Trend**: Ältere Modelle mit ISG
- **WPL 25**: Neueste Serie

### Alpha Innotec
- **SW-Serie**: SW 90, SW 120, SW 140, SW 191
- **Rückgewinnung**: SWR, SWR-H, SWR-L
- **Div-serie**: DIV 14, DIV 24, DIV 34
- **Kompakt-Serie**: Alle Alpha Innotec Modelle haben ISG

---

## Nützliche Links

- [Stiebel Eltron Modbus](https://www.stiebel-eltron.ch/de/home/produkte-loesungen/erneuerbare_energien/regelung_energiemanagement/modbus.html)
- [Stiebel Eltron Modbus Anleitung](https://www.stiebel-eltron.ch/content/dam/ste/ch/de/downloads/kundenservice/smart-home/Modbus/Modbus%20Bedienungsanleitung.pdf)
- [Alpha Innotec Luxtronik](https://www.alpha-innotec.com/en/products/accessories/control/luxtronik)
- [Loxone WPL12 Trend](https://www.loxforum.com/forum/projektforen/loxberry/allgemeines-aa/321181-stiebel-eltron-wc3a4rmpe-wpl-20a-mit-isg-daten-auslesen-und-speichern)
- [TeCalor Modbus](https://www.tecalor.de/content/dam/tec/de/downloads/Modbus_Bedienungsanleitung.pdf)

---

## Hinweis

Die exakten Modbus-Adressen für ISG Web sind herstellerabhängig und können je nach Modell und Software-Version variieren. Es wird empfohlen:
1. ISG Web Dokumentation prüfen
2. Mit Modbus-Scanner die verfügbaren Register prüfen
3. Hersteller-Support kontaktieren

---

**Version**: 1.0
**Letztes Update**: 31.01.2026
**Maintainer**: Xerolux
**Projekt**: [idm-metrics-collector](https://github.com/Xerolux/idm-metrics-collector)
