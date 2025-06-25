# ARIMA Trading Strategie mit Backtesting (Windows)

Dieses Projekt implementiert eine vollständige ARIMA-basierte Trading-Strategie für SPY (SPDR S&P 500 ETF) mit automatischem Backtesting und Performance-Analyse. **Optimiert für Windows-Systeme.**

## ⚠️ WICHTIGER HINWEIS FÜR WINDOWS-NUTZER ⚠️

**Bevor Sie beginnen:** Conda erfordert unter Windows spezielle Behandlung:
- Öffnen Sie IMMER ein neues PowerShell-Fenster als Administrator, bevor Sie mit conda arbeiten
- Nach dem Erstellen einer neuen Umgebung: PowerShell komplett schließen und neues Fenster öffnen
- Erst dann können Sie die Umgebung aktivieren

## Beschreibung

Das Projekt besteht aus zwei Hauptkomponenten:

1. **ARIMA-Modellierung** (`arima_modeling.py`): Grundlegende Zeitreihenprognose
2. **Trading-Strategie mit Backtesting** (`backtesting.py`): Vollständige Implementierung einer ARIMA-basierten Trading-Strategie

Die Strategie nutzt ARIMA-Konfidenzintervalle zur Signalgenerierung: Long-Positionen bei Kursen unter der prognostizierten Untergrenze und Short-Positionen bei Kursen über der Obergrenze.

## Features

- **Automatische ARIMA-Modellierung**: Verwendung von `auto_arima` für optimale Parameterfindung
- **Modulare Visualisierung**: Separate `plotting.py` mit wiederverwendbaren Plot-Funktionen
- **Automatisches Speichern von Plots**: Alle Visualisierungen werden automatisch im `plots/` Unterordner gespeichert
- **Dual-Plot-Visualisierung**: Kombinierte Darstellung von Gesamtkursverlauf und detaillierter Prognose
- **Zuverlässige Datenquelle**: Standardmäßig Yahoo Finance (über `yfinance`), mit Fallback auf FRED (`pandas_datareader`) und Alpha Vantage
- **Mehrere Datenquellen**: `yfinance`, FRED (Federal Reserve, via `pandas_datareader`), Alpha Vantage, mit Fallback auf synthetische Daten
- **Kostenlose APIs**: Funktioniert mit kostenlosen API-Schlüsseln
- **Trading-Signale**: Basierend auf ARIMA-Konfidenzintervallen
- **Backtesting**: Vollständige Performance-Analyse mit der `backtesting` Bibliothek
- **Umfassende Visualisierungen**: Automatische Erstellung und Speicherung von:
  - Performance-Dashboard (4-Panel-Übersicht)
  - Detaillierte Preisdiagramme mit gleitenden Durchschnitten
  - Trading-Signal-Visualisierungen
  - Returns-Verteilungsanalyse
- **Risk Management**: Konfigurierbare Kommissionen und Trading-Parameter
- **Performance-Metriken**: Detaillierte Statistiken und Kennzahlen
- **Windows-optimiert**: Spezielle Behandlung für Windows-Umgebungen
- **Modularer Aufbau**: Zentrale utils.py für alle Datenoperationen und plotting.py für Visualisierungen
- **Sichere API-Konfiguration**: .env-Datei für API-Schlüssel
- **Dynamische Datumsberechnung**: Automatische Anpassung an den gestrigen Tag als Datenende

## Installation (Windows)

**Voraussetzungen:**

- Windows 10/11
- Python 3.8 oder höher
- PowerShell oder Command Prompt

## 🚀 Schnellstart für Windows-Nutzer

1. **Repository klonen/herunterladen**
   ```powershell
   git clone <repository-url>
   cd arima
   ```
   
   *Oder ZIP-Datei herunterladen und entpacken*

2. **Virtuelle Umgebung erstellen (WICHTIG: Python 3.11 verwenden)**
   ```powershell
   # Python 3.11 verwenden (empfohlen für beste Kompatibilität)
   python3.11 -m venv venv
   # Falls python3.11 nicht verfügbar ist:
   # py -3.11 -m venv venv
   
   .\venv\Scripts\Activate.ps1
   ```
   
   *Bei Problemen mit PowerShell Execution Policy:*
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

   **⚠️ WICHTIG**: Python 3.13 hat Kompatibilitätsprobleme mit `pmdarima`. Verwenden Sie Python 3.11 für beste Ergebnisse!

3. **Python-Version überprüfen**
   ```powershell
   python --version
   # Sollte Python 3.11.x anzeigen
   ```

4. **Pakete installieren**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

### Alternative: Conda Installation (Empfohlen für Windows)

Conda ist oft stabiler unter Windows:

**⚠️ WICHTIG FÜR WINDOWS-NUTZER:**
1. Öffnen Sie IMMER ein neues PowerShell-Fenster als Administrator, bevor Sie mit conda arbeiten
2. Nach der Umgebungserstellung: PowerShell komplett schließen und neues Fenster öffnen!

```powershell
# 1. Miniconda herunterladen: https://docs.conda.io/en/latest/miniconda.html
# 2. Nach der Installation: PowerShell komplett schließen und neues als Administrator öffnen!

# 3. Conda-Umgebung erstellen (in einem NEUEN PowerShell-Fenster als Admin)
conda create -n arima-env python=3.11

# 4. ⚠️ WICHTIG: PowerShell komplett schließen und NEUES Fenster öffnen!
# 5. Dann erst aktivieren:
conda activate arima-env

# 6. ✅ Prüfen ob Umgebung aktiviert ist (sollte "(arima-env)" im Prompt zeigen)
conda info --envs

# Hauptpakete über Conda installieren (backtesting ist nicht verfügbar)
conda install -c conda-forge pmdarima matplotlib pandas numpy scipy

# Alpha Vantage und Backtesting-Paket separat über pip installieren
pip install alpha-vantage backtesting pandas-datareader python-dotenv
```

**⚠️ Wichtige Hinweise:**

- **IMMER ein neues PowerShell-Fenster öffnen** bevor Sie mit conda arbeiten
- Das `backtesting` und `alpha-vantage` Paket sind nicht über conda-forge verfügbar und müssen über pip installiert werden
- Nach `conda activate arima-env` erscheint keine Bestätigungsmeldung - das ist normal!
- Sie sollten `(arima-env)` am Anfang Ihres PowerShell-Prompts sehen
- Falls nicht sichtbar: `conda info --envs` zeigt alle verfügbaren Umgebungen an

### 🔑 Alpha Vantage API-Schlüssel (Kostenlos)

**Wichtig**: Für beste Ergebnisse sollten Sie einen kostenlosen Alpha Vantage API-Schlüssel erhalten:

1. Gehen Sie zu: https://www.alphavantage.co/support/#api-key
2. Registrieren Sie sich kostenlos (nur E-Mail erforderlich)
3. Kopieren Sie Ihren kostenlosen API-Schlüssel
4. **Öffnen Sie die `.env` Datei im Projektordner**
5. **Ersetzen Sie `your_api_key_here` mit Ihrem echten API-Schlüssel:**
   ```env
   ALPHA_VANTAGE_API_KEY=IHR_ECHTER_API_SCHLÜSSEL
   ```

**Kostenlose Limits**: 5 Anfragen pro Minute, 500 pro Tag - mehr als ausreichend für dieses Projekt!

**Sicherheit**: Die `.env` Datei wird automatisch von Git ignoriert und nicht öffentlich geteilt.

## Verwendung

### 1. Einfache ARIMA-Modellierung

Das Grundmodell ausführen:

```powershell
python arima_modeling.py
```

**Häufiger Fehler:** `ModuleNotFoundError: No module named 'alpha_vantage'`
**Lösung:** Pakete installieren mit: `pip install alpha-vantage pmdarima pandas numpy pandas-datareader`

**API-Schlüssel**: Das Skript funktioniert mit dem Demo-Schlüssel, aber für beste Ergebnisse sollten Sie einen kostenlosen API-Schlüssel von Alpha Vantage verwenden.

Das Skript wird:

- Alpha Vantage API verwenden (keine Rate-Limiting-Probleme wie bei Yahoo Finance)
- Bei API-Problemen auf FRED (Federal Reserve Daten) ausweichen
- Falls alle APIs fehlschlagen, synthetische SPY-ähnliche Daten generieren
- Ein optimales ARIMA-Modell fitten
- Eine 5-Perioden-Prognose erstellen
- Die prognostizierte Preisspanne ausgeben

### 2. Trading-Strategie mit Backtesting

Die vollständige Trading-Strategie ausführen:

```powershell
python arima_backtesting.py
```

Die Backtesting-Strategie implementiert folgende Logik:

- **Datenbereich**: SPY-Daten von 2020-01-01 bis 2025-06-01
- **Modell**: Automatisches ARIMA (max_p=3, max_q=3, ohne Saisonalität)
- **Signalgenerierung**:
  - **Long-Signal**: Wenn aktueller Kurs unter der prognostizierten Untergrenze liegt
  - **Short-Signal**: Wenn aktueller Kurs über der prognostizierten Obergrenze liegt
  - **Neutral**: Wenn Kurs innerhalb der prognostizierten Range liegt
- **Backtesting-Parameter**:
  - Startkapital: $10,000
  - Kommission: 0.1% pro Trade
  - Hedging: Aktiviert
  - Exclusive Orders: Aktiviert

Das Backtesting gibt detaillierte Performance-Statistiken aus, einschließlich:

- Gesamtrendite
- Sharpe Ratio
- Maximum Drawdown
- Anzahl Trades
- Win-Rate
- Weitere Risiko- und Performance-Metriken


## ⚠️ Fehlerbehebung (Troubleshooting)

### Häufige Probleme und Lösungen

**1. Alpha Vantage API-Probleme**
```text
KeyError: 'Error Message'
```

- **Problem**: API-Schlüssel ungültig oder API-Limit erreicht
- **Lösung**: Kostenlosen API-Schlüssel von https://www.alphavantage.co/support/#api-key holen
- **Fallback**: Das Skript wechselt automatisch zu FRED oder synthetischen Daten

**2. Keine Internetverbindung**

- **Problem**: Keine Verbindung zu externen APIs möglich
- **Lösung**: Das Skript generiert automatisch synthetische SPY-ähnliche Daten
- **Vorteil**: Funktioniert auch offline für Demonstrationszwecke

**3. Fehlende Pakete**
```text
ModuleNotFoundError: No module named 'alpha_vantage'
```

- **Lösung**: Alle benötigten Pakete installieren:
  ```powershell
  pip install alpha-vantage pmdarima pandas numpy pandas-datareader yfinance backtesting matplotlib scipy
  ```

**4. pmdarima Installation unter Windows**
```
ERROR: Failed building wheel for pmdarima
```
- **Lösung**: Verwenden Sie conda statt pip:
  ```powershell
  conda install -c conda-forge pmdarima
  ```

**5. Sklearn Deprecation Warnings**
- **Problem**: Warnungen über veraltete sklearn Parameter
- **Auswirkung**: Nur Warnungen, Funktionalität nicht beeinträchtigt
- **Lösung**: Ignorieren Sie diese Warnungen - sie sind harmlos


## Konfiguration

### ARIMA-Modellierung (`arima_modeling.py`)

Folgende Parameter können angepasst werden:

- **Ticker-Symbol**: Standard ist "SPY", kann zu anderen Aktien/ETFs geändert werden
- **Zeitraum**: Start- und Enddatum der historischen Daten
- **Prognosehorizont**: Anzahl der zu prognostizierenden Perioden (`n_periods`)
- **ARIMA-Parameter**: `max_p`, `max_q`, `information_criterion`

### Backtesting (`arima_backtesting.py`)

Anpassbare Parameter:

- **Ticker-Symbol**: Standard ist "SPY"
- **Zeitraum**: Daterange für Backtesting (aktuell: 2020-2025)
- **Startkapital**: `init_cash` (Standard: $10,000)
- **Kommissionen**: `commission` (Standard: 0.1%)
- **ARIMA-Parameter**: `max_p`, `max_q` (Standard: je 3)
- **Prognosehorizont**: `n_periods` für Signalgenerierung (Standard: 5)

## Abhängigkeiten (Windows-optimiert)

**Für das Basis-ARIMA-Modell (`arima_modeling.py`):**

- `yfinance`: Standard-Datenquelle (Yahoo Finance, kostenlos und zuverlässig)
- `pandas-datareader`: Fallback für FRED-Daten (Federal Reserve)
- `alpha-vantage`: Zusätzlicher Fallback (API-Schlüssel empfohlen, aber nicht zwingend)
- `python-dotenv`: Laden von Umgebungsvariablen aus .env Datei
- `pmdarima`: Automatische ARIMA-Modellierung (kann unter Windows komplex zu installieren sein)
- `pandas`: Datenmanipulation und -analyse
- `numpy`: Numerische Berechnungen
- `matplotlib`: Plotting und Visualisierungen

**Zusätzlich für das Backtesting (`arima_backtesting.py`):**

- `backtesting`: Backtesting-Framework für Trading-Strategien
- `scipy`: Wissenschaftliche Berechnungen

**Für Visualisierungen (`plotting.py`):**

- `matplotlib`: Hauptbibliothek für alle Plots und Diagramme
- `pandas`: Für Datums- und Zeitreihenbearbeitung in Plots

## Ausgabe

### ARIMA-Modellierung Ausgabe (`arima_modeling.py`)

Das Skript zeigt detaillierte Informationen über den gesamten Prozess:

**Bei erfolgreicher Datenübertragung und Modellierung:**
```text
Starting ARIMA modeling for SPY...
Successfully loaded 357 data points from 2024-01-02 to 2025-06-24
Price range: $445.23 - $578.91
Fitting ARIMA model...
Best ARIMA model: (2, 1, 1)

=== ARIMA Forecast Results ===
Current price (2025-06-24): $565.43
Forecast horizon: 5 periods
Predicted range: $558.12 – $572.87
Average forecast: $565.49

Detailed 5-day forecast:
Day 1 (2025-06-25): $565.78 (Range: $558.12 - $573.44)
Day 2 (2025-06-26): $565.89 (Range: $556.77 - $575.01)
Day 3 (2025-06-27): $565.95 (Range: $555.34 - $576.56)
Day 4 (2025-06-28): $566.01 (Range: $553.89 - $578.13)
Day 5 (2025-06-29): $566.07 (Range: $552.42 - $579.72)

Creating price data visualization...
Dual forecast plot saved to: plots/arima_forecast_dual_20250625_185110.png
```

**Neue Visualisierung:**
Das Skript erstellt jetzt eine zweistufige Visualisierung mit englischen Beschriftungen:
- **Oberer Plot**: "SPY Complete Price History" - Gesamter SPY Kursverlauf über den gesamten Zeitraum
- **Unterer Plot**: "SPY Price History - Last 30 Days + 5-Day Forecast" - Detailansicht der letzten 30 Tage plus 5-Tage ARIMA-Prognose mit Konfidenzintervall

**Automatisches Speichern:**
Alle Plots werden automatisch im `plots/` Unterordner gespeichert:
- `plots/arima_forecast_dual_YYYY-MM-DD_HHMMSS.png` - Hauptprognose-Visualisierung (Dual-Plot)
- Der Ordner `plots/` wird automatisch erstellt, falls er nicht existiert

**Plot-Beschriftungen (Englisch):**
- Titel: "SPY Complete Price History" und "SPY Price History - Last 30 Days + 5-Day Forecast"
- Legenden: "Complete SPY Price History", "Historical Prices (last 30 days)", "ARIMA Forecast", "95% Confidence Interval"
- Achsenbeschriftungen: "Price ($)" und "Date"

**Bei API-Problemen/Fallback:**
```text
Starting ARIMA modeling for SPY...
Using demo API key. For production use, get your free API key from: https://www.alphavantage.co/support/#api-key
Downloading SPY data from Alpha Vantage...
Error downloading data from Alpha Vantage: API rate limit exceeded
Trying to download S&P 500 data from FRED...
Successfully downloaded 357 data points from FRED
...

Creating price data visualization...
Dual forecast plot saved to: plots/arima_forecast_dual_20250625_185110.png
```

Die prognostizierte Spanne basiert auf den Konfidenzintervallen der 5-Perioden-Prognose.

### Backtesting-Ausgabe (`arima_backtesting.py`)

Das Backtesting-Skript gibt umfassende Performance-Statistiken aus und erstellt automatisch detaillierte Visualisierungen, z.B.:

```text
Start                     2020-01-02 00:00:00
End                       2025-05-30 00:00:00
Duration                   1943 days 00:00:00
Exposure Time [%]                    85.23
Equity Final [$]                  12543.21
Equity Peak [$]                   13102.45
Return [%]                           25.43
Buy & Hold Return [%]                18.76
Return (Ann.) [%]                     4.67
Volatility (Ann.) [%]                12.34
Sharpe Ratio                         0.378
Sortino Ratio                        0.521
Calmar Ratio                         0.243
Max. Drawdown [%]                   -19.21
Avg. Drawdown [%]                    -3.45
Max. Drawdown Duration        156 days 00:00:00
Avg. Drawdown Duration         23 days 00:00:00
# Trades                               145
Win Rate [%]                         52.41
Best Trade [%]                        8.67
Worst Trade [%]                      -6.23
Avg. Trade [%]                        0.16
Max. Trade Duration            15 days 00:00:00
Avg. Trade Duration             5 days 00:00:00
Profit Factor                         1.23
Expectancy [%]                        0.21
SQN                                   0.84
```

**Automatische Visualisierungen:**
Das Backtesting erstellt und speichert automatisch mehrere Visualisierungen im `plots/` Ordner:

1. **Performance-Dashboard** (`arima_backtest_results_YYYY-MM-DD_HHMMSS.png`):
   - 4-Panel-Übersicht mit SPY-Preis und Trading-Signalen
   - Portfolio-Equity-Kurve
   - Returns-Verteilungshistogramm
   - Performance-Metriken-Zusammenfassung

2. **Detaillierte Preisdiagramme** (`spy_recent_price_YYYY-MM-DD_HHMMSS.png`):
   - Letzte 6 Monate SPY-Kursentwicklung
   - 20-Tage und 50-Tage gleitende Durchschnitte
   - Hochauflösende Darstellung der aktuellen Marktlage

3. **Performance-Bericht** (`arima_backtest_report_YYYY-MM-DD_HHMMSS.txt`):
   - Textuelle Zusammenfassung aller wichtigen Kennzahlen
   - Strategie-Parameter und Zeitraum
   - Geeignet für Dokumentation und Berichte

**Ordnerstruktur:**
```
plots/
├── arima_forecast_dual_20250625_185110.png
├── arima_backtest_results_20250625_185004.png
├── spy_recent_price_20250625_185010.png
└── arima_backtest_report_20250625_185013.txt
```

## 📈 Plot-Interpretation - Anleitung zum Verstehen der Visualisierungen

### 1. ARIMA Forecast Plots (arima_modeling.py)

#### Dual-Plot Visualisierung (`arima_forecast_dual_*.png`)

**Oberer Plot - Gesamtkursverlauf:**

- **Blaue Linie**: SPY Kursverlauf über den gesamten Analysezeitraum
- **Plot-Titel**: "SPY Complete Price History"
- **Zweck**: Kontext für langfristige Trends und Marktphasen
- **Interpretation**:
  - Aufwärtstrends zeigen Bullenmärkte
  - Abwärtstrends zeigen Bärenmärkte  
  - Seitwärtsbewegungen zeigen Konsolidierungsphasen
  - Volatilität ist durch Schwankungsbreite erkennbar

**Unterer Plot - Detailprognose:**

- **Blaue Linie**: Historische Kurse der letzten 30 Tage (Label: "Historical Prices (last 30 days)")
- **Rote gestrichelte Linie mit Punkten**: 5-Tage ARIMA-Prognose (Label: "ARIMA Forecast")
- **Rote Schattierung**: 95% Konfidenzintervall der Prognose (Label: "95% Confidence Interval")
- **Plot-Titel**: "SPY Price History - Last 30 Days + 5-Day Forecast"
- **Achsenbeschriftungen**: Y-Achse "Price ($)", X-Achse "Date"

**Interpretationshilfen:**

- **Enge Konfidenzintervalle**: Hohe Modellsicherheit, stabile Prognose
- **Breite Konfidenzintervalle**: Höhere Unsicherheit, volatile Marktlage
- **Prognose oberhalb letzter Kurse**: Modell erwartet Kursanstieg
- **Prognose unterhalb letzter Kurse**: Modell erwartet Kursrückgang
- **Trend der Prognose**: Zeigt erwartete kurzfristige Richtung

**Trading-Signale ableiten:**

- Aktueller Kurs unter unterer Konfidenzgrenze → Potentielles Long-Signal
- Aktueller Kurs über oberer Konfidenzgrenze → Potentielles Short-Signal
- Kurs innerhalb Konfidenzintervall → Kein klares Signal

### 2. Backtesting Performance Dashboard (`arima_backtest_results_*.png`)

#### Panel 1: SPY Price with ARIMA Trading Signals (Oben Links)

- **Plot-Titel**: "SPY Price with ARIMA Trading Signals"
- **Blaue Linie**: SPY Kursverlauf über Backtesting-Zeitraum (Label: "SPY Close Price")
- **Grüne Punkte/Pfeile**: Buy-Signale (Label: "Buy Signals")
- **Rote Punkte/Pfeile**: Sell-Signale (Label: "Sell Signals")
- **Y-Achse**: "Price ($)"

**Interpretation:**

- **Häufigkeit der Signale**: Zeigt Aktivität der Strategie
- **Timing der Signale**: Qualität der Ein- und Ausstiegspunkte
- **Signal-Clustering**: Bereiche mit vielen Signalen = volatile Marktphasen
- **Signal-Qualität**: Visuelle Bewertung ob Signale bei Extremen auftreten

#### Panel 2: Portfolio Equity Curve (Oben Rechts)

- **Plot-Titel**: "Portfolio Equity Curve"
- **Grüne Linie**: Portfoliowert über Zeit (Label: "Portfolio Value")
- **Graue gestrichelte Linie**: Anfangskapital (Label: "Initial Capital")
- **Y-Achse**: "Portfolio Value ($)"

**Interpretation:**

- **Steigender Trend**: Profitable Strategie
- **Glatte Kurve**: Konstante Performance
- **Volatile Kurve**: Risikoreiche Performance
- **Drawdowns**: Verlustphasen (Abstand zum vorherigen Höchststand)
- **Endwert vs. Buy & Hold**: Vergleich zur passiven Anlagestrategie

**Bewertungskriterien:**

- Equity-Kurve oberhalb Startlinie = Gewinn
- Stetige Aufwärtsbewegung = Gute Strategie
- Große Schwankungen = Hohe Volatilität
- Lange Verlustphasen = Hohe Drawdowns

#### Panel 3: Daily Returns Distribution (Unten Links)

- **Plot-Titel**: "Daily Returns Distribution"
- **Blaues Histogramm**: Verteilung der täglichen Renditen
- **Rote gestrichelte Linie**: Durchschnittsrendite (Label: "Mean: X.XXX%")
- **X-Achse**: "Daily Return (%)", **Y-Achse**: "Frequency"

**Interpretation:**

- **Normalverteilung**: Gesunde Renditeverteilung
- **Rechtsschiefe**: Mehr große Gewinne als Verluste (positiv)
- **Linksschiefe**: Mehr große Verluste als Gewinne (negativ)
- **Fat Tails**: Extreme Ereignisse häufiger als erwartet
- **Durchschnitt nahe Null**: Geringe durchschnittliche Tagesrendite normal
- **Breite Verteilung**: Hohe Volatilität

#### Panel 4: Performance Metrics Summary (Unten Rechts)

**Wichtigste Kennzahlen verstehen:**

- **Total Return**: Gesamtrendite über Backtesting-Zeitraum
  - >0% = Gewinn, <0% = Verlust
  - Vergleich mit Buy & Hold Return wichtig

- **Sharpe Ratio**: Risikoadjustierte Rendite
  - >1.0 = Sehr gut
  - 0.5-1.0 = Gut  
  - <0.5 = Schwach
  - <0 = Verluste

- **Max Drawdown**: Größter Verlust vom Höchststand
  - <-10% = Akzeptabel
  - -10% bis -20% = Moderat
  - >-20% = Hoch riskant

- **Win Rate**: Prozentsatz profitabler Trades
  - >60% = Sehr gut
  - 50-60% = Gut
  - <50% = Schwach (kann durch große Gewinne kompensiert werden)

### 3. Detaillierte Preisdiagramme (`spy_recent_price_*.png`)

**Plot-Informationen:**
- **Plot-Titel**: "SPY Recent Price Action (Last ~6 Months)"
- **X-Achse**: "Date", **Y-Achse**: "Price ($)"

**Hauptelemente:**

- **Blaue Linie**: SPY Kursverlauf (letzte 6 Monate) - Label: "SPY Close Price"
- **Orange Linie**: 20-Tage gleitender Durchschnitt - Label: "20-day MA"
- **Rote Linie**: 50-Tage gleitender Durchschnitt - Label: "50-day MA"

**Technische Analyse:**

- **Kurs über beiden MAs**: Aufwärtstrend
- **Kurs unter beiden MAs**: Abwärtstrend  
- **MA-Kreuzungen**: Trendwechsel-Signale
- **20-MA über 50-MA**: Bullisher Trend
- **20-MA unter 50-MA**: Bärischer Trend

**Support und Resistance:**

- **MA-Linien als Support**: Kurs prallt von unten ab
- **MA-Linien als Resistance**: Kurs prallt von oben ab
- **Durchbrüche**: Bestätigung von Trendwechseln

### 4. Performance-Berichte (`arima_backtest_report_*.txt`)

**Wichtige Abschnitte:**

**Zeitserie-Metriken:**
- **Start/End**: Backtesting-Zeitraum
- **Duration**: Gesamtdauer der Analyse  
- **Exposure Time**: Prozent der Zeit mit offenen Positionen

**Rendite-Metriken:**
- **Return [%]**: Absolute Gesamtrendite
- **Return (Ann.) [%]**: Annualisierte Rendite
- **Buy & Hold Return**: Vergleichsrendite bei Kaufen-und-Halten

**Risiko-Metriken:**
- **Volatility (Ann.)**: Jährliche Schwankungsbreite
- **Max. Drawdown**: Größter Verlust
- **Calmar Ratio**: Rendite/Max-Drawdown-Verhältnis

**Trading-Metriken:**
- **# Trades**: Anzahl der Trades
- **Avg. Trade Duration**: Durchschnittliche Haltedauer
- **Profit Factor**: Verhältnis Gewinne/Verluste

### 5. Interpretations-Checkliste für Trading-Entscheidungen

**✅ Positive Signale:**
- Sharpe Ratio > 0.5
- Win Rate > 50%
- Profit Factor > 1.0
- Max Drawdown < -15%
- Equity Curve steigend
- Konfidenzintervalle eng

**⚠️ Warnsignale:**
- Sharpe Ratio < 0
- Win Rate < 45%
- Max Drawdown > -25%
- Viele aufeinanderfolgende Verluste
- Sehr breite Konfidenzintervalle
- Equity Curve seitwärts/fallend

**📊 Marktkontext bewerten:**
- Aktuelle Marktphase (Bull/Bear/Seitwärts)
- Volatilität der letzten Wochen
- Position der MAs relativ zum Kurs
- Nähe zu historischen Höchst-/Tiefstständen

### 6. Häufige Interpretationsfehler vermeiden

**❌ Typische Fehler:**
- Einzelne Metriken übergewichten
- Konfidenzintervalle als Garantie verstehen
- Backtesting-Performance als Zukunftsgarantie sehen
- Drawdowns unterschätzen
- Transaktionskosten ignorieren

**✅ Richtige Herangehensweise:**
- Mehrere Metriken zusammen betrachten
- Risiko-Rendite-Verhältnis bewerten
- Marktkontext einbeziehen
- Worst-Case-Szenarien berücksichtigen
- Regelmäßige Modell-Updates einplanen

## Erweiterte Nutzung

Das Projekt kann erweitert werden um:

- **Erweiterte Visualisierungen**: Zusätzliche Plot-Typen in `plotting.py` (Residuenanalyse, Korrelogramme)
- Modelldiagnostik und Residuenanalyse
- Saisonale ARIMA-Modelle (SARIMA)
- Parameter-Optimierung für die Trading-Strategie
- Risiko-Management-Features (Stop-Loss, Take-Profit)
- Multi-Asset-Backtesting
- Walk-Forward-Analyse
- Export der Prognoseergebnisse und Backtesting-Berichte
- **Interaktive Plots**: Integration von Plotly für interaktive Visualisierungen
- **Custom Plot-Funktionen**: Erweiterung der `plotting.py` um weitere Analyse-Tools

## 📊 Visualisierungen und Plot-Management

### Automatisches Speichern

Alle Visualisierungen werden automatisch gespeichert:

- **Ordner**: `plots/` (wird automatisch erstellt)
- **Dateinamen**: Timestamped für eindeutige Identifikation
- **Formate**: Hochauflösende PNG-Dateien (300 DPI)
- **Berichte**: Zusätzliche Textdateien mit Performance-Zusammenfassungen

### Plot-Typen

**ARIMA-Modellierung (`arima_modeling.py`):**
- Dual-Plot mit Gesamtkursverlauf und Prognose-Detail
- Single-Forecast-Plot für einfache Darstellung

**Backtesting (`arima_backtesting.py`):**
- 4-Panel Performance-Dashboard
- Detaillierte Preisdiagramme mit technischen Indikatoren
- Performance-Textberichte

### Organisation der Plots

```
plots/
├── arima_forecast_dual_20250625_185110.png      # ARIMA Prognose (Dual-Plot)
├── arima_backtest_results_20250625_185004.png   # Backtesting Dashboard
├── spy_recent_price_20250625_185010.png         # Detaillierte Preisanalyse
└── arima_backtest_report_20250625_185013.txt    # Performance-Bericht
```

**Alle Plots werden im gleichen `plots/` Ordner gespeichert mit:**
- **Zeitstempel**: Format `YYYY-MM-DD_HHMMSS` für chronologische Sortierung
- **Eindeutige Dateinamen**: Verschiedene Analysetypen sind durch Präfixe unterscheidbar
- **Automatische Erstellung**: Der `plots/` Ordner wird beim ersten Plot automatisch erstellt

**Vorteile:**
- Vollständige Nachverfolgbarkeit aller Analysen
- Einfacher Vergleich verschiedener Zeitpunkte
- Professionelle Dokumentation für Berichte
- Keine manuellen Speichervorgänge erforderlich

## Strategiebeschreibung

Die implementierte ARIMA-Trading-Strategie basiert auf der Mean-Reversion-Hypothese:

1. **Modelltraining**: Ein ARIMA-Modell wird auf historische SPY-Kursdaten gefittet
2. **Prognoseerstellung**: Das Modell erstellt 5-Perioden-Prognosen mit Konfidenzintervallen
3. **Signalgenerierung**:
   - **Long-Position**: Wenn der aktuelle Kurs unter der prognostizierten Untergrenze liegt (Annahme: Kurs wird zur Mitte zurückkehren)
   - **Short-Position**: Wenn der aktuelle Kurs über der prognostizierten Obergrenze liegt (Annahme: Kurs wird zur Mitte zurückkehren)
   - **Kein Trade**: Wenn der Kurs innerhalb der prognostizierten Range liegt

4. **Risiko-Management**: Kommissionen von 0.1% pro Trade simulieren realistische Handelskosten

## Dateiübersicht

- `arima_modeling.py`: Grundlegende ARIMA-Modellierung und Prognoseerstellung (verwendet utils.py und plotting.py)
- `arima_backtesting.py`: Vollständige Trading-Strategie mit Backtesting (verwendet utils.py und plotting.py)
- `plotting.py`: **Erweiterte Visualisierungs-Bibliothek** - Alle Plot-Funktionen für ARIMA-Analysen
  - `create_dual_plot()` - Kombinierte Darstellung: Gesamtkursverlauf + detaillierte Prognose
  - `create_single_forecast_plot()` - Einfache Prognose-Visualisierung (konfigurierbar)
  - `create_backtest_visualization()` - Umfassende Backtesting-Visualisierungen (4-Panel-Dashboard)
  - `create_recent_price_chart()` - Detaillierte Preisdiagramme mit gleitenden Durchschnitten
  - **Automatisches Speichern**: Alle Funktionen speichern Plots automatisch im `plots/` Ordner
- `utils.py`: **Zentrale Datei** - Alle Datendownload-Funktionen und Verarbeitungslogik
  - `get_spy_data()` - Hauptfunktion mit automatischen Fallback-Optionen
  - `download_data_with_alpha_vantage()` - Alpha Vantage API-Integration mit .env Support
  - `download_data_alternative_free_sources()` - FRED als kostenlose Alternative
  - `generate_synthetic_spy_data()` - Synthetische Daten-Generierung
  - `prepare_data_for_backtesting()` - OHLC-Formatierung für Backtesting
- `requirements.txt`: Liste aller benötigten Python-Pakete (mit Alpha Vantage und python-dotenv)
- `.env`: Konfigurationsdatei für API-Schlüssel (sicher und nicht in Git)
- `.gitignore`: Git-Ignore-Datei (schützt .env vor versehentlicher Veröffentlichung)
- `plots/`: **Automatisch erstellter Ordner** für alle gespeicherten Visualisierungen
  - Enthält timestamped PNG-Dateien und Textberichte
  - Wird automatisch beim ersten Plot erstellt
- `README_DE.md`: Deutsche Dokumentation
- `README_EN.md`: Englische Dokumentation


