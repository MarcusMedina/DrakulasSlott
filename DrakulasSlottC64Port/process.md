# Konverteringsplan: Drakulas Slott

Detta dokument beskriver planen för att konvertera C64-spelet "Drakulas Slott" till en modern C#-applikation.

## Steg 1: Direkt översättning (1:1)

Målet i detta första steg är att skapa en C#-version som är så lik originalets BASIC-kod som möjligt, nästan rad för rad.

- **Struktur:** Vi kommer att efterlikna BASIC-kodens `GOTO`-struktur, troligtvis med hjälp av `switch`-satser eller `while`-loopar med en "program-pekare".
- **Data:** All speldata från `DATA`-satserna kommer att läggas in direkt i C#-koden i form av arrayer och listor.
- **Fokus:** Prioriteten är att få en fungerande version av spelet som beter sig exakt som originalet. Ingen refaktorering eller modernisering av kodstrukturen kommer att ske i detta skede.
- Gosubs blir metoder med antingen många parametrar eller så gör vi alla variabler globala

## Steg 2: Refaktorering och modernisering

När den direkta översättningen är klar och fungerar korrekt, påbörjar vi refaktoreringen. 
- Sentence case för texten istället för all Caps som det är nu.
- Snyggare GUI med Colorful.Console
- **Objektorientering:** Vi kommer att introducera klasser för `Room`, `GameObject`, `Player`, etc. för att skapa en tydlig och robust domänmodell.
- **Kodkvalitet:** "Spaghettikoden" från steg 1 kommer att skrivas om till ren, läsbar och underhållbar C#-kod som följer moderna principer som SRP och DRY.
- **Spellogik:** Logiken kommer att separeras från datan och delas upp i mindre, hanterbara metoder.

## Steg 3: Webbversion

Som ett sista steg kommer vi att ta den refaktorerade C#-koden och bygga en modern webbapplikation av spelet.

- **Teknik:** Vi kan använda tekniker som Blazor eller ASP.NET Core för att skapa ett webbaserat gränssnitt.
- **Användarupplevelse:** Spelet kommer att presenteras i ett grafiskt gränssnitt i webbläsaren istället för enbart text i en konsol.
- **Alternativ version kan vara i PHP då min webbhost är en apache :P**

Steg 4:

- CI/CD testning och deployment via Github Actions
- FTP deployment till webbserver marcusmedina.pro/draculasslott

Steg 5:
Engelsk version
