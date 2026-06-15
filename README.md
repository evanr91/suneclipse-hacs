# SunEclipse Balies (HACS)

Custom Home Assistant integratie voor `https://www.suneclipse.nl/balies.json`.

Repository: `https://github.com/evanr91/suneclipse-hacs`

- Polling elke 60 seconden
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

## Lovelace voorbeeld

Gebruik onderstaande cards om:

- 48 uur geschiedenis te tonen van `balies` + `load` in 1 grafiek
- een losse status-card te tonen met `balies/max-balies - load`

```yaml
type: vertical-stack
cards:
  - type: history-graph
    title: SunEclipse laatste 48 uur
    hours_to_show: 48
    refresh_interval: 60
    entities:
      - entity: sensor.suneclipse_balies_balies
        name: Balies
      - entity: sensor.suneclipse_balies_load
        name: Load
  - type: entity
    entity: sensor.suneclipse_balies_status
    name: SunEclipse status
```

## Opmerking over historie

Voor een 48-uurs grafiek moet Home Assistant Recorder ingeschakeld zijn (standaard meestal al actief).
