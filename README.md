# SunEclipse Balies (HACS)

Custom Home Assistant integratie voor `https://www.suneclipse.nl/balies.json`.

Repository: `https://github.com/evanr91/suneclipse-hacs`

- Polling elke 15 seconden
- Sensoren voor `balies`, `max-balies`, `load`
- Extra status-sensor met formaat: `balies/max-balies - load`

## Installeren via HACS

1. Open HACS in Home Assistant.
2. Ga naar **Integrations**.
3. Kies **Custom repositories**.
4. Voeg deze repository toe als type **Integration**.
5. Installeer **SunEclipse Balies**.
6. Herstart Home Assistant.
7. Ga naar **Instellingen > Apparaten en diensten > Integratie toevoegen**.
8. Kies **SunEclipse Balies** en rond de setup af.

Standaard URL is:

`https://www.suneclipse.nl/balies.json`

## Entities

Na installatie krijg je deze entities:

- `sensor.suneclipse_balies_balies`
- `sensor.suneclipse_balies_max_balies`
- `sensor.suneclipse_balies_load`
- `sensor.suneclipse_balies_status`

## Lovelace voorbeelden (standaard Home Assistant)

Onderstaand voorbeeld gebruikt alleen standaard cards en geeft 3 uur live-data.

- **Balies-grafiek:** toont zowel `balies` als `max-balies`, zodat de as automatisch tot de maximale capaciteit schaalt.
- **Load-grafiek:** losse grafiek voor `load`.

```yaml
type: vertical-stack
cards:
  - type: history-graph
    title: Balies laatste 3 uur
    hours_to_show: 3
    refresh_interval: 15
    entities:
      - entity: sensor.suneclipse_balies_balies
        name: Balies
      - entity: sensor.suneclipse_balies_max_balies
        name: Max balies
  - type: history-graph
    title: Load laatste 3 uur
    hours_to_show: 3
    refresh_interval: 15
    entities:
      - entity: sensor.suneclipse_balies_load
        name: Load
  - type: entity
    entity: sensor.suneclipse_balies_status
    name: Sun Eclipse status
```

Losse voorbeelden (standaard Home Assistant):

**Alleen Balies grafiek**

```yaml
type: history-graph
title: Balies laatste 3 uur
hours_to_show: 3
refresh_interval: 15
entities:
  - entity: sensor.suneclipse_balies_balies
    name: Balies
  - entity: sensor.suneclipse_balies_max_balies
    name: Max balies
```

**Alleen Load grafiek**

```yaml
type: history-graph
title: Load laatste 3 uur
hours_to_show: 3
refresh_interval: 15
entities:
  - entity: sensor.suneclipse_balies_load
    name: Load
```

## Lovelace voorbeeld (advanced chart)

Als je meer controle wilt over styling en assen, kun je `apexcharts-card` gebruiken (via HACS Frontend).

```yaml
type: custom:apexcharts-card
update_interval: 15s
header:
  show: true
  title: Sun Eclipse laatste 3 uur
graph_span: 3h
span:
  end: minute
now:
  show: true
  color: "#888888"
  label: Nu
yaxis:
  - id: load
    opposite: true
    decimals: 2
    min: 0
    max: 25
  - id: balies
    decimals: 0
    min: 0
series:
  - entity: sensor.suneclipse_balies_max_balies
    name: Max balies
    type: line
    yaxis_id: balies
    color: "#9e9e9e"
    stroke_width: 1
    curve: stepline
    show:
      in_legend: false
      legend_value: false
  - entity: sensor.suneclipse_balies_balies
    name: Balies
    type: line
    yaxis_id: balies
    color: "#f5a623"
    stroke_width: 2
    show:
      legend_value: true
  - entity: sensor.suneclipse_balies_load
    name: Load
    type: column
    yaxis_id: load
    color: "#0292d1"
    show:
      legend_value: true
```

Voor een server met 4 cores is `load = 3.5` een nette bovengrens om aan te houden.

## Opmerking over historie

Voor grafieken over tijd moet Home Assistant Recorder ingeschakeld zijn (standaard meestal al actief).
