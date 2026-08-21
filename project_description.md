---
name: "Drakulasslott"
description: "C#-port av det klassiska svenska C64-textäventyret Drakulasslott"
type: game
language: C#
status: active
owner: marcus
tags: [game, c64, textadventure, csharp, retro, swedish]
---

## Vad det är

En modern C#/.NET 10-port av det svenska Commodore 64-textäventyret "Drakulasslott" (Drakulas slott),
ursprungligen publicerat som public domain. Spelet kör speldatan (förbehandlade `.txt`-filer) genom
en inbyggd `FakeBasic`-emulator som simulerar C64 BASIC-beteende och PETSCII-teckenhantering,
med färgad konsolutmatning via `Colorful.Console`.

## Stack

C# / .NET 10, `Colorful.Console` NuGet-paket.

## Status och noter

Aktivt underhållet — senaste commit 2026-07-15. Pågående arbete: fixa BASIC-semantikbuggar
och färdigställa en genomspelningsguide (walkthrough).
