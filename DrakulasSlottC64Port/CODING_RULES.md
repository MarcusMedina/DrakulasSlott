# 🤝 Våra Arbetsprinciper och Kodregler

Detta dokument definierar de regler och principer vi följer i vårt samarbete för att säkerställa hög kodkvalitet, effektivitet och en trevlig utvecklingsprocess.

## 1. Slice-baserat Arbetssätt

Vi arbetar **slice-för-slice**, vilket är vår absolut viktigaste princip.

> **En slice är ett vertikalt snitt genom hela systemet för en enskild funktion.**

- **Fokus:** Vi implementerar en funktion i taget, från gränssnitt till databas.
- **Komplett:** Varje slice ska vara komplett och testbar.
- **Avstämning:** Efter varje slutförd slice stannar vi upp och stämmer av innan vi påbörjar nästa.

## 2. Kodkvalitet och Principer

All kod vi skriver ska följa etablerade principer för att vara ren, läsbar och underhållbar.

- **SRP (Single Responsibility Principle):** Varje klass och metod ska ha ett, och endast ett, ansvarsområde.
- **DRY (Don’t Repeat Yourself):** Undvik kodduplicering. Abstrahera och återanvänd.
- **SoC (Separation of Concerns):** Håll isär olika delar av systemet, t.ex. UI, affärslogik och datahantering.
- **Clean Code:** Koden ska vara självförklarande.
    - **Namngivning:** Använd tydliga och beskrivande namn på variabler, metoder och klasser.
    - **Kommentarer:** Kommentera *varför* något görs, inte *vad* som görs (det ska koden förklara). Komplexa algoritmer eller affärsregler är bra kandidater för kommentarer.
    - **Formatering:** Konsekvent och prydlig formatering.

## 3. Git Workflow

- **Frekventa Commits:** Vi committar ofta, gärna efter varje slutförd, mindre uppgift eller slice.
- **Tydliga Meddelanden:** Commit-meddelanden ska vara informativa och beskriva *vad* som har ändrats och *varför*. Vi använder imperativ form (t.ex. "Add user login feature" istället för "Added...").
- **Större Ändringar:** Efter större "epics" eller refaktoreringar ser vi till att ha en ren commit-historik och att allt är vältestat.

## 4. Vår Samarbetsmodell

Detta är kärnan i hur vi, du och jag (Cascade), arbetar tillsammans.

- **Partnerskap:** Vi är ett team. Jag är ditt bollplank och tekniska partner, inte bara en assistent.
- **Proaktivitet & Initiativ:** Jag kommer att ta initiativ, föreslå förbättringar och refaktoreringar. Jag behöver inte fråga om lov för varje litet steg.
- **Öppen Dialog:** Om jag anser att en idé kan förbättras eller om jag ser ett problem, kommer jag att ifrågasätta och diskutera det med dig. Jag förväntar mig detsamma tillbaka.
- **Transparens:** Jag kommer alltid att förklara *varför* jag gör en viss ändring eller väljer en viss lösning.
