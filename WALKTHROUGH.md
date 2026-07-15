# Drakulas Slott — Komplett Lösningsguide

Spelet börjar i **HALLEN** (rum 1) kl 20:00. Du har till midnatt (24:00) på dig.
Varje kommando tar en minut. Du har gott om tid om du följer denna guide.

---

## Karta

```
             WAMPYRERNAS GRAV (18)
                     |N
             SIDO RUMMET (17)
                     |N  [dörr, behöver OLJE FLASKA]
             GALLERIET (16)
                  /  |
          [båt] /    |GÅ TAKSKÄGG
               /     |
         EN BÅT (12) TAKSKÄGGET (15)
               |S      |U
  UNDERJORDISK SJÖ (11)  (nås via båten)
               |S
   HEMLIGA PASSAGEN (10)
               |S  [mur, behöver SLÄGGA]
   ELDSTADEN AV TEGEL (8)
               |GÅ ELDSTADEN  [eld, behöver HELIGT VATTEN i LÄSRUMMET]
        LÄSRUMMET (2) — W — HALLEN (1) — E — BIBLOTEKET (3) — E — VAPEN KAMMAREN (4) — E — TORNET (5)
                                                  |D [FLYTTA BOKHYLLA]                         |GÅ BALKONG
                                    DEN GÖMDA KORRIDOREN (9)                          LÄGRE TORNET (6)
                                               |N                                           |S
                                  ALKEMISTENS LABRATORIUM (13)                        KAPELLET (7)
                                               |N                                        |D
                                   FÖRVARINGS RUMMET (14) — U — LÄSRUMMET (2)    VAPEN KAMMAREN (4)
```

---

## Föremål och var de finns

| Föremål | Rum | Behövs för |
|---------|-----|-----------|
| SLÄGGA | TORNET (5) | Slå sönder muren + ta spikar |
| KLOCKA | HALLEN (1) | Inget (se: visar tid) |
| REP | DEN GÖMDA KORRIDOREN (9) | Klättra ner från tornet |
| PERGAMENT RULLE | BIBLOTEKET (3) | Tips (valfritt) |
| YXA | VAPEN KAMMAREN (4) | Slå sönder lådan → träpålar |
| ÅROR | LÄGRE TORNET (6) | Ro båten |
| NYCKEL | KAPELLET (7) | Öppna kistan |
| HELIGT VATTEN | KAPELLET (7) | Tända elden (kräver HINK) |
| OLJE FLASKA | ALKEMISTENS LABRATORIUM (13) | Olja dörren i SIDO RUMMET |
| LÅDA → TRÄPÅLAR | FÖRVARINGS RUMMET (14) | Döda vampyren |
| HINK | FÖRVARINGS RUMMET (14) | Bära HELIGT VATTEN |
| FACKLA | ELDSTADEN AV TEGEL (8) | Lysa i mörka rum |
| SPIKAR | TAKSKÄGGET (15) | Lösgöra gobeläng |
| GOBELÄNG | GALLERIET (16) | Öppna passage till SIDO RUMMET |
| BÅT | UNDERJORDISK SJÖ (11) | Transport till GALLERIET |

---

## Steg-för-steg lösning

### Del 1 — Hämta rep, olja och hink

```
GÅ ÖST              → BIBLOTEKET
FLYTTA BOKHYLLA      → AHA! Hemlig passage öppnas (NER)
GÅ NER               → DEN GÖMDA KORRIDOREN
TA REP
GÅ NORR              → ALKEMISTENS LABRATORIUM
TA OLJE FLASKA
GÅ NORR              → FÖRVARINGS RUMMET
TA HINK
```

### Del 2 — Hämta yxa och slå sönder lådan

Lådan är i samma rum — slå sönder den nu medan du har yxan nära.

```
GÅ UPP               → LÄSRUMMET (genväg uppåt!)
GÅ ÖST               → HALLEN
GÅ ÖST               → BIBLOTEKET
GÅ ÖST               → VAPEN KAMMAREN
TA YXA
GÅ NER               → DEN GÖMDA KORRIDOREN   [via bokhyllegången]

(Alternativ väg: GÅ VÄST → BIBLOTEKET → GÅ NER)

GÅ NORR              → ALKEMISTENS LABRATORIUM
GÅ NORR              → FÖRVARINGS RUMMET
SLÅ LÅDA             → MED VAD? YXA            → DU SLOG SÖNDER LÅDAN TILL NÅGRA TRÄPÅLAR
TA TRÄPÅLAR
LÄGGA YXA            → (du behöver den inte mer)
```

### Del 3 — Slägga, rep till balkong, åror och nyckel

```
GÅ UPP               → LÄSRUMMET
GÅ ÖST               → HALLEN
GÅ ÖST               → BIBLOTEKET
GÅ ÖST               → VAPEN KAMMAREN
GÅ ÖST               → TORNET
TA SLÄGGA
BINDA REP            → I VAD? BALKONG           → Repet är nu fastbundet
GÅ BALKONG           → LÄGRE TORNET
TA ÅROR
GÅ SÖDER             → KAPELLET
LÄGGA REP            → (repet är redan bundet, du kan lämna det)
TA HELIGT VATTEN     → I VAD? HINK              → taget med hinken
LÄGGA HINK           → (hinken behövs inte mer)
TA NYCKEL
```

> **Tips:** Bär aldrig mer än 6 saker. Lämna saker du är klar med.

### Del 4 — Tänd elden, ta facklan, slå sönder muren

```
GÅ NER               → VAPEN KAMMAREN
GÅ VÄST              → BIBLOTEKET
GÅ VÄST              → HALLEN
GÅ VÄST              → LÄSRUMMET
LÄGGA HELIGT VATTEN  → ASKA uppstår, elden tänds!
GÅ ELDSTADEN         → ELDSTADEN AV TEGEL      (nu när elden brinner)
TA FACKLA
SLÅ ELDSTADEN        → MED VAD? SLÄGGA         → Muren faller! Ny utgång norrut.
```

### Del 5 — Genom underjorden till galleriet

*Rum 10, 11 och 12 är mörka — facklan skyddar dig.*

```
GÅ NORR              → DEN HEMLIGA PASSAGEN    (mörkt, men facklan lyser)
GÅ NORR              → EN UNDERJORDISK SJÖ     (mörkt)
GÅ BÅT               → EN BÅT                  (du kliver ombord)
RO                   → GALLERIET               (du har rott till andra sidan!)
```

### Del 6 — Lösning i galleriet (gobelänggåtan)

```
GÅ TAKSKÄGG          → TAKSKÄGGET              (speciell rörelse nedåt)
TA SPIKAR            → GOBELÄNGEN FÖLL!        (behöver SLÄGGA)
GÅ UPP               → GALLERIET
LÄGGA SPIKAR         → (behövs inte mer)
TA GOBELÄNG          → AHA! Norrutgång öppnas!
GÅ NORR              → SIDO RUMMET
```

### Del 7 — Olja dörren och döda vampyren

```
OLJA DÖRR            → Dörren öppnas mot WAMPYRERNAS GRAV!
GÅ NORR              → WAMPYRERNAS GRAV        (mörkt, men facklan lyser)
ÖPPNA KISTA          → (behöver NYCKEL) → VAMPYR I KISTA!
DÖDA VAMPYR          → MED VAD? TRÄPÅLAR       → GRATULERAR! DU HAR DÖDAT VAMPYREN!
```

---

## Pussel-förklaringar

### Bokhyllan (BIBLOTEKET)
`FLYTTA BOKHYLLA` — avslöjar en hemlig nedgång till korridoren under slottet.

### Repet (TORNET)
`BINDA REP` → frågar *i vad* → skriv `BALKONG` → repet säkras. Sedan `GÅ BALKONG` tar dig ner till LÄGRE TORNET.

### Det heliga vattnet (KAPELLET)
Du kan inte bara ta HELIGT VATTEN med händerna — du behöver hinken.
`TA HELIGT VATTEN` → frågar *i vad* → skriv `HINK`. Hinken måste bäras.

### Elden (LÄSRUMMET)
`LÄGGA HELIGT VATTEN` i LÄSRUMMET skapar ASKA och tänder en osynlig eld.
Därefter fungerar `GÅ ELDSTADEN` som en ny utgång från LÄSRUMMET.

### Muren (ELDSTADEN AV TEGEL)
`SLÅ ELDSTADEN` → frågar *med vad* → skriv `SLÄGGA`. Släggan slår igenom tegelmuren.

### Lådan → Träpålar (FÖRVARINGS RUMMET)
`SLÅ LÅDA` → frågar *med vad* → skriv `YXA`. Lådan splittras till träpålar — vampyrens bane.

### Gobeläng-spikar-gåtan (TAKSKÄGGET / GALLERIET)
Gobeläng sitter fastsatt i taket. Du måste:
1. Gå ner till TAKSKÄGGET: `GÅ TAKSKÄGG` (från GALLERIET)
2. Ta spikarna (med släggan) → gobeläng rasar ner till GALLERIET
3. Gå upp och ta gobeläng → norrutgång öppnas

### Dörren (SIDO RUMMET)
`OLJA DÖRR` med OLJE FLASKA i fickan — dörren mot WAMPYRERNAS GRAV öppnas.

---

## Mörka rum

Rum **10, 11, 12 och 18** är mörka utan FACKLA. Utan den ser du ingenting och kan inte navigera.
Ta facklan i ELDSTADEN AV TEGEL innan du går norrut.

---

## Tidsfristen

Klockan går från 20:00. Vampyren rymmer vid midnatt (24:00) — **game over**.
Du har 240 kommandon på dig. Den här guiden kräver ca 55–60 steg. Ingen stress.
