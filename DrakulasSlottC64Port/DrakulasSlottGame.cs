using System.Drawing;
using Console = Colorful.Console;

namespace DrakulasSlottC64Port;

/// <summary>
/// Ren OOP-port av det svenska C64-textäventyret "Drakulas Slott".
/// All data och spellogik härrör direkt från BASIC-källkoden.
/// </summary>
public class DrakulasSlottGame
{
    // ── Rumsnamn (1-indexerade, rum 1..18) ──────────────────────────────────
    private static readonly string[] RoomNames =
    [
        "",
        "HALLEN",                   // 1
        "LÄSRUMMET",                // 2
        "BIBLOTEKET",               // 3
        "VAPEN KAMMAREN",           // 4
        "TORNET",                   // 5
        "LÄGRE TORNET",             // 6
        "KAPELLET",                 // 7
        "ELDSTADEN AV TEGEL",       // 8  (name changes to EN SÖNDERSLAGEN ELDSTAD)
        "DEN GÖMDA KORRIDOREN",     // 9
        "DEN HEMLIGA PASSAGEN",     // 10
        "EN UNDERJORDISK SJÖ",      // 11
        "EN BÅT",                   // 12
        "ALKEMISTENS LABRATORIUM",  // 13
        "FÖRVARINGS RUMMET",        // 14
        "TAKSKÄGGET",               // 15
        "GALLERIET",                // 16
        "SIDO RUMMET",              // 17
        "WAMPYRERNAS GRAV",         // 18
    ];

    // ── Objektnamn O[1..28]: 1-6=riktningar, 7-28=föremål ──────────────────
    // Föremål i O[7..28] motsvarar itemindex 1..22 (O[7]=item1=SLÄGGA osv.)
    private readonly string[] _o =
    [
        "",
        "NORR",              // 1  riktning N
        "SÖDER",             // 2  riktning S
        "ÖST",               // 3  riktning E
        "VÄST",              // 4  riktning W
        "UPP",               // 5  riktning U
        "NER",               // 6  riktning D
        "SLÄGGA",            // 7  item 1  → L[1]
        "KLOCKA",            // 8  item 2  → L[2]
        "REP",               // 9  item 3  → L[3]
        "PERGAMENT RULLE",   // 10 item 4  → L[4]
        "YXA",               // 11 item 5  → L[5]
        "ÅROR",              // 12 item 6  → L[6]
        "NYCKEL",            // 13 item 7  → L[7]
        "HELIGT VATTEN",     // 14 item 8  → L[8]
        "OLJE FLASKA",       // 15 item 9  → L[9]
        "LÅDA",              // 16 item 10 → L[10]  (blir TRÄPÅLAR)
        "HINK",              // 17 item 11 → L[11]
        "FACKLA",            // 18 item 12 → L[12]
        "SPIKAR",            // 19 item 13 → L[13]
        "GOBELÄNG",          // 20 item 14 → L[14]
        "BÅT",               // 21 item 15 → L[15]
        "ROSTIG DÖRR",       // 22 item 16 → L[16]  (blir ÖPPEN DÖRR)
        "STÄNGD KISTA",      // 23 item 17 → L[17]  (blir VAMPYR I KISTA)
        "ELD I ELDSTADEN",   // 24 item 18 → L[18]  (blir ASKA)
        "BOKHYLLA",          // 25 item 19 → L[19]
        "SKYLT",             // 26 item 20 → L[20]
        "BALKONG",           // 27 item 21 → L[21]
        "ELDSTAD AV TEGEL",  // 28 item 22 → L[22]  (blir EN SÖNDERSLAGEN ELDSTAD)
    ];

    // ── Föremålens platser L[1..22]: 0=bärs av spelaren, N=rumsnummer ───────
    private readonly int[] _l = new int[23];

    // ── Karta P[rum 1..18][riktning 1..6]: destinationsrum (0=stängd) ───────
    // Riktning: 1=N, 2=S, 3=E(ÖST), 4=W(VÄST), 5=U(UPP), 6=D(NER)
    private readonly int[,] _p = new int[19, 7];

    // ── Rumsnamn (kan ändras under spel, t.ex. rum 8) ───────────────────────
    private readonly string[] _d = new string[19];

    // ── Spelstatus ───────────────────────────────────────────────────────────
    private int _room = 1;   // nuvarande rum
    private int _c = 0;      // antal burna föremål
    private int _t1 = 0;     // minuter (0-59)
    private int _t2 = 20;    // timmar (börjar 20:00)
    private int _fi = 0;     // FI: eld tänd (1=ja)
    private int _oi = 0;     // OI: dörr oljad (1=ja)
    private int _ta = 0;     // TA: gobeläng föll (1=ja)
    private string _tgp = ""; // TGP$: vad repet är bundet vid

    // Substantivsöksträng (första 2 tecknen av varje O[1..28])
    private string _os = "";

    // ── Verbsöksträng (W$ i BASIC) ──────────────────────────────────────────
    private const string VerbString = "GÅTASELÄSLÖPBIFLDÖOLRO";

    public void Run()
    {
        InitData();
        ShowSplash();

        Console.BackgroundColor = Color.DarkBlue;
        Console.ForegroundColor = Color.Yellow;
        Console.Clear();
        Console.WriteLine("\n            DRAKULAS SLOTT\n");

        while (true)
        {
            ShowRoom();

            Console.Write("\nVAD SKALL JAG GÖRA ");
            string fullInput = (Console.ReadLine() ?? "").ToUpper().Trim();
            Console.WriteLine();

            // Parsa verb (A$) och substantiv (B$)
            string a = fullInput.Length >= 2 ? fullInput[..2] : fullInput;
            string b = "";
            int sp = fullInput.IndexOf(' ');
            if (sp >= 0 && fullInput.Length > sp + 2)
                b = fullInput.Substring(sp + 1, 2);

            // Tidsutveckling
            _t1++;
            if (_t1 >= 60) { _t1 = 0; _t2++; }

            // B$-alias i rätt ordning (matchar BASIC raderna 400-445)
            if (b == "DÖ") b = "RO";   // DÖRR → ROSTIG DÖRR
            if (b == "FL") b = "OL";   // FLASKA → OLJE FLASKA

            // Tidsgräns (line 405)
            if (_t2 >= 24)
            {
                Console.WriteLine("VAMPYREN HAR RYMT - DIN TID ÄR UTE !");
                break;
            }

            // Specialfall: DÖDA VAMPYR i rum 18 – FÖRE VA→HE-alias (line 415)
            if (a == "DÖ" && b == "VA" && _room == 18)
            {
                if (KillVampire()) break;
                continue;
            }

            if (b == "KI") b = "ST";   // KISTA → STÄNGD KISTA

            // SIMMA (line 430-432)
            if (a == "SI")
            {
                if (_room == 11) { Console.WriteLine("DU DRUNKNADE I DET ISKALLA VATTNET"); break; }
                Console.WriteLine("JAG SER INGET VATTEN");
                continue;
            }

            // GÅ TAKSKÄGG i GALLERIET (line 435)
            if (a == "GÅ" && b == "TA" && _room == 16)
            {
                _room = 15;
                continue;
            }

            if (b == "VA") b = "HE";   // VATTEN → HELIGT VATTEN (line 437)

            // HJÄLP (line 440)
            if (a == "HJ") { ShowHelp(); continue; }

            // TRÄPÅLAR-alias (line 445)
            if ((b == "TR" || b == "PÅ") && _o[16] == "TRÄPÅLAR") b = "LÅ";

            // INVENTERA (line 480)
            if (a == "IN") { ShowInventory(); continue; }

            int f = FindVerb(a);
            int s = FindNoun(b);

            if (f < 1) { Console.WriteLine("JAG FÖRSTÅR INTE !"); continue; }

            bool gameOver = false;
            switch (f)
            {
                case 1: gameOver = DoGo(s, b); break;        // GÅ
                case 2: DoTake(s); break;                     // TA
                case 3: DoLook(s); break;                     // SE
                case 4: DoLay(s, b); break;                   // LÄGGA
                case 5: DoHit(s); break;                      // SLÅ
                case 6: DoOpen(s); break;                     // ÖPPNA
                case 7: DoTie(s); break;                      // BINDA
                case 8: DoMove(s, b); break;                  // FLYTTA
                case 9: gameOver = DoKillCommand(s); break;   // DÖDA
                case 10: DoOil(s); break;                     // OLJA
                case 11: DoRow(); break;                      // RO
                default: Console.WriteLine("JAG FÖRSTÅR INTE !"); break;
            }

            if (gameOver) break;
        }

        ShowEndScreen();
    }

    // ── Rumsvisning ──────────────────────────────────────────────────────────
    private void ShowRoom()
    {
        Console.WriteLine($"\nJAG ÄR I {_d[_room]}");

        // Mörker: rum 10,11,12,18 är mörka utan fackla (L[12]=0 = bärs)
        bool dark = _l[12] != 0 && (_room is 10 or 11 or 12 or 18);
        if (dark)
        {
            Console.WriteLine("DET ÄR MÖRKT JAG KAN INTE SE");
            return;
        }

        Console.Write("JAG SER ");
        bool saw = false;
        for (int x = 1; x <= 22; x++)
        {
            if (_l[x] == _room) { Console.Write($" *{_o[x + 6]}"); saw = true; }
        }
        Console.WriteLine(saw ? "" : "INGENTING");

        Console.Write("\nSYNLIGA UTGÅNGAR - ");
        for (int x = 1; x <= 6; x++)
            if (_p[_room, x] > 0) Console.Write($"{_o[x]}* ");
        Console.WriteLine();
    }

    // ── GÅ ───────────────────────────────────────────────────────────────────
    private bool DoGo(int s, string b)
    {
        // Vanlig riktning (S=1..6)
        if (s >= 1 && s <= 6)
        {
            if (_p[_room, s] > 0) { _room = _p[_room, s]; return false; }
            // (ingen explicit feltext i BASIC för stängda utgångar i GÅ-hanteraren)
        }

        // GÅ ELDSTADEN (EL) från LÄSRUMMET (line 540-560)
        if (b == "EL" && _room == 2)
        {
            if (_fi == 0) { Console.WriteLine("DU BRÄNDES TILL DÖDS"); return true; }
            _room = 8; return false;
        }

        // GÅ BALKONG (BA) från TORNET (line 570-590)
        if (_room == 5 && b == "BA")
        {
            if (_tgp == "BA") { _room = 6; return false; }
            Console.WriteLine("DU FÖLL OCH DOG"); return true;
        }

        // GÅ BÅT (BÅ) när båten är i rummet (line 600)
        if (_l[15] == _room && b == "BÅ") { _room = 12; return false; }

        Console.WriteLine("KAN INTE");
        return false;
    }

    // ── TA ───────────────────────────────────────────────────────────────────
    private void DoTake(int s)
    {
        if (s < 7) { Console.WriteLine("JAG FÖRSTÅR INTE !"); return; }
        if (_c >= 6) { Console.WriteLine("JAG BÄR FÖR MYCKET"); return; }

        // S=14: HELIGT VATTEN – kräver HINK (line 660-680)
        if (s == 14)
        {
            Console.Write("I VAD ");
            string cnt = ReadShort();
            if (cnt == "HI" && _l[11] == 0 && _l[8] == _room)
            {
                _l[8] = 0; _c++;
            }
            else Console.WriteLine("KAN INTE");
            return;
        }

        // S=20: GOBELÄNG – kräver att spikar lossats (line 695-710)
        if (s == 20)
        {
            if (_l[14] != _room) { Console.WriteLine("JAG SER DEN INTE"); return; }
            if (_ta == 1)
            {
                _l[14] = 0; _c++;
                Console.WriteLine("AHA!");
                _p[16, 1] = 17; // Öppnar väg från GALLERIET till SIDO RUMMET
            }
            else Console.WriteLine("DEN ÄR FASTSPIKAD VID TAKSKÄGGET");
            return;
        }

        // S=19: SPIKAR – kräver SLÄGGA, fäller gobelängen (line 720-730)
        if (s == 19)
        {
            if (_l[13] == _room && _l[1] == 0)
            {
                _ta = 1; Console.WriteLine("GOBELÄNGEN FÖLL");
                _l[13] = 0; _c++;
            }
            else if (_l[1] != 0) Console.WriteLine("INGEN SLÄGGA");
            else Console.WriteLine("JAG SER DEN INTE");
            return;
        }

        // Föremål S=21..28 kan inte tas (line 750)
        if (s > 20) { Console.WriteLine("KAN INTE"); return; }

        // Vanlig plockning (line 760-780)
        if (_l[s - 6] == _room) { _l[s - 6] = 0; _c++; }
        else Console.WriteLine("JAG SER DEN INTE");
    }

    // ── SE ───────────────────────────────────────────────────────────────────
    private void DoLook(int s)
    {
        // Inget substantiv eller riktning: visa om inget
        if (s == 0 || s <= 6) return; // GOTO 250 i BASIC

        // S=26: SKYLT
        if (s == 26)
        {
            Console.WriteLine(_room == 1 ? "VAMPYREN VAKNAR VID MIDNATT" : "JAG SER DEN INTE");
            return;
        }

        // S=7,9: SLÄGGA/REP – ingen text (line 865 → 330)
        if (s < 10 && s != 8) return;

        // S=8: KLOCKA (line 865-869)
        if (s == 8)
        {
            if (_l[2] != 0) Console.WriteLine("DEN HAR JAG INTE");
            else Console.WriteLine($"{_t2} : {_t1}");
            return;
        }

        // S=10..25 och S=27,28 (line 850)
        if (_l[4] == 0) Console.WriteLine("ALLA UTGÅNGAR ÄR INTE SYNLIGA");
        else Console.WriteLine("DEN HAR JAG INTE");
    }

    // ── LÄGGA ────────────────────────────────────────────────────────────────
    private void DoLay(int s, string b)
    {
        // Bränn HELIGT VATTEN i LÄSRUMMET (line 870)
        if (s == 14 && _l[8] == 0 && _room == 2)
        {
            _o[24] = "ASKA"; _fi = 1; _l[8] = 99; _c--;
            return;
        }

        if (string.IsNullOrEmpty(b) || s < 7) { Console.WriteLine("VA ??"); return; }
        if (_l[s - 6] != 0) { Console.WriteLine("DEN HAR JAG INTE"); return; }

        _l[s - 6] = _room; _c--;
    }

    // ── SLÅ ──────────────────────────────────────────────────────────────────
    private void DoHit(int s)
    {
        bool canHitBox      = s == 16 && _l[10] == _room && _l[5] == 0; // LÅDA i rum, YXA bärs
        bool canHitFirewall = s == 28 && _l[1] == 0 && _room == 8;      // ELDSTAD i rum 8, SLÄGGA bärs

        if (!canHitBox && !canHitFirewall) { Console.WriteLine("INGENTING HÄNDE"); return; }

        Console.Write("MED VAD ");
        string tool = ReadShort();

        if (canHitBox && tool == "YX")
        {
            _o[16] = "TRÄPÅLAR";
            Console.WriteLine("DU SLOG SÖNDER LÅDAN TILL NÅGRA TRÄPÅLAR");
        }
        else if (canHitFirewall && tool == "SL")
        {
            _o[28] = "EN SÖNDERSLAGEN ELDSTAD";
            _p[8, 1] = 10;           // Öppnar norrpassage från rum 8 till rum 10
            _d[8] = _o[28];          // Rumsnamnet ändras
        }
        else Console.WriteLine("INGENTING HÄNDE");
    }

    // ── ÖPPNA ────────────────────────────────────────────────────────────────
    private void DoOpen(int s)
    {
        // ÖPPNA KISTA i rum 18 med NYCKEL (line 950)
        if (s == 23 && _room == 18 && _l[7] == 0)
        {
            _o[23] = "VAMPYR I KISTA";
            return;
        }

        // ÖPPNA DÖRR i SIDO RUMMET med olja + NYCKEL (line 960)
        if (_room == 17 && s == 22 && _oi == 1 && _l[7] == 0)
        {
            _o[22] = "ÖPPEN DÖRR";
            _p[17, 1] = 18;
            return;
        }

        Console.WriteLine("INGENTING HÄNDE");
    }

    // ── BINDA ────────────────────────────────────────────────────────────────
    private void DoTie(int s)
    {
        // Kräver REP (item 3) och att det bärs (L[3]=0), S=9 (line 1000)
        if (_l[3] != 0 || s != 9) { Console.WriteLine("KAN INTE"); return; }

        Console.Write("I VAD ");
        string target = ReadShort();
        _tgp = target;
    }

    // ── FLYTTA ───────────────────────────────────────────────────────────────
    private void DoMove(int s, string b)
    {
        // Ledtråd om olja (line 1030)
        if (b == "OL" || b == "FL")
        {
            Console.WriteLine("MENAR DU ATT JAG BÖR OLJA DEN ?");
            return;
        }

        // FLYTTA BOKHYLLA (S=25) i BIBLOTEKET → avslöjar hemlig passage (line 1035-1040)
        if (s == 25 && _room == 3)
        {
            Console.WriteLine("AHA!");
            _p[3, 6] = 9; // NER från BIBLOTEKET till DEN GÖMDA KORRIDOREN
            return;
        }

        Console.WriteLine("KAN INTE");
    }

    // ── DÖDA (via verb-switch) ───────────────────────────────────────────────
    private bool DoKillCommand(int s)
    {
        // S=23 (KISTA), rum 18, vampyren ligger i kistan (line 1050)
        if (s == 23 && _room == 18 && _o[23] == "VAMPYR I KISTA")
            return KillVampire();

        Console.WriteLine("INGENTING HÄNDE");
        return false;
    }

    // Gemensam logik för att döda vampyren (från både line 415 och 1050)
    private bool KillVampire()
    {
        Console.Write("MED VAD ");
        string weapon = ReadShort();

        if ((weapon == "TR" || weapon == "PÅ") && _l[10] == 0 && _o[16] == "TRÄPÅLAR")
        {
            Console.WriteLine("GRATULERAR ! - DU HAR DÖDAT VAMPYREN");
            return true;
        }

        Console.WriteLine("DU GJORDE FEL ! VAMPYREN VAKNADE OCH DÖDADE DIG");
        return true;
    }

    // ── OLJA ────────────────────────────────────────────────────────────────
    private void DoOil(int s)
    {
        // OLJA DÖRR (S=22) eller OLJA NER (S=6) i SIDO RUMMET med OLJE FLASKA (line 1100-1110)
        if (_l[9] == 0 && _room == 17 && (s == 22 || s == 6))
        {
            _oi = 1;
            _o[22] = "ÖPPEN DÖRR";
            _p[17, 1] = 18;
            return;
        }

        Console.WriteLine("KAN INTE");
    }

    // ── RO ───────────────────────────────────────────────────────────────────
    private void DoRow()
    {
        // Kräver att vara i båten (rum 12) och ha ÅROR (L[6]=0) (line 1120-1140)
        if (_room != 12 || _l[6] != 0) { Console.WriteLine("KAN INTE"); return; }

        Console.WriteLine("DU HAR ROTT MED BÅTEN TILL ANDRA SIDAN");

        // Flytta alla föremål som var i rum 12 till rum 16
        for (int x = 1; x <= 22; x++)
            if (_l[x] == 12) _l[x] = 16;

        _l[15] = 16; // Båten är nu i GALLERIET
        _room = 16;
    }

    // ── Inventarie ───────────────────────────────────────────────────────────
    private void ShowInventory()
    {
        Console.WriteLine("JAG BÄR FÖLJANDE SAKER");
        int count = 0;
        for (int x = 1; x <= 22; x++)
        {
            if (_l[x] == 0) { Console.WriteLine(_o[x + 6]); count++; }
        }
        if (count == 0) Console.WriteLine("INGENTING");
    }

    // ── Hjälp ────────────────────────────────────────────────────────────────
    private static void ShowHelp()
    {
        Console.WriteLine("\nVÄDERSTRÄCKEN ÄR:");
        Console.WriteLine(" NORR, SÖDER, ÖST, VÄST, NER, UPP");
        Console.WriteLine("\nVERBEN ÄR:");
        Console.WriteLine(" GÅ, TA, SE, LÄGGA, SLÅ, ÖPPNA, BINDA, FLYTTA");
        Console.WriteLine(" DÖDA, OLJA, RO, SIMMA");
    }

    // ── Verbsökning ──────────────────────────────────────────────────────────
    private static int FindVerb(string a)
    {
        for (int x = 0; x < VerbString.Length - 1; x += 2)
            if (VerbString.Substring(x, 2) == a) return x / 2 + 1;
        return 0;
    }

    // ── Substantivsökning ────────────────────────────────────────────────────
    private int FindNoun(string b)
    {
        if (b.Length < 2) return 0;
        for (int x = 0; x < _os.Length - 1; x += 2)
            if (_os.Substring(x, 2) == b) return x / 2 + 1;
        return 0;
    }

    // ── Hjälpmetod: läs 2-teckens svar ──────────────────────────────────────
    private static string ReadShort()
    {
        string s = (Console.ReadLine() ?? "").ToUpper().Trim();
        return s.Length >= 2 ? s[..2] : s;
    }

    // ── Splash-skärm ─────────────────────────────────────────────────────────
    private static void ShowSplash()
    {
        Console.BackgroundColor = Color.DarkBlue;
        Console.ForegroundColor = Color.Yellow;
        Console.Clear();
        Console.WriteLine("╭─────────────────────────────────────────────────────────╮");
        Console.WriteLine("│                   DRAKULAS SLOTT                        │");
        Console.WriteLine("├─────────────────────────────────────────────────────────┤");
        Console.WriteLine("│ Genre     : Text Adventure / Äventyrsspel               │");
        Console.WriteLine("│ Original  : Commodore 64, 19xx, Public Domain           │");
        Console.WriteLine("│ C#-port   : Marcus Medina, NionIT                       │");
        Console.WriteLine("├─────────────────────────────────────────────────────────┤");
        Console.WriteLine("│         Tryck ENTER för att börja spelet...             │");
        Console.WriteLine("╰─────────────────────────────────────────────────────────╯");
        Console.ReadLine();
        Console.Clear();
    }

    private static void ShowEndScreen()
    {
        Console.WriteLine("\n\nTryck ENTER för att avsluta.");
        Console.ReadLine();
    }

    // ── Datainitalisering ────────────────────────────────────────────────────
    private void InitData()
    {
        // Kopierar statiska rumsnamn till _d (som kan ändras under spelets gång)
        for (int i = 0; i < RoomNames.Length; i++) _d[i] = RoomNames[i];

        // Föremålens startplatser L[1..22] (från BASIC DATA-rader 162-201)
        _l[1] = 5;   // SLÄGGA        → TORNET
        _l[2] = 1;   // KLOCKA        → HALLEN
        _l[3] = 9;   // REP           → DEN GÖMDA KORRIDOREN
        _l[4] = 3;   // PERGAMENT RULLE → BIBLOTEKET
        _l[5] = 4;   // YXA           → VAPEN KAMMAREN
        _l[6] = 6;   // ÅROR          → LÄGRE TORNET
        _l[7] = 7;   // NYCKEL        → KAPELLET
        _l[8] = 7;   // HELIGT VATTEN → KAPELLET
        _l[9] = 13;  // OLJE FLASKA   → ALKEMISTENS LABRATORIUM
        _l[10] = 14; // LÅDA          → FÖRVARINGS RUMMET
        _l[11] = 14; // HINK          → FÖRVARINGS RUMMET
        _l[12] = 8;  // FACKLA        → ELDSTADEN AV TEGEL
        _l[13] = 15; // SPIKAR        → TAKSKÄGGET
        _l[14] = 16; // GOBELÄNG      → GALLERIET
        _l[15] = 11; // BÅT           → EN UNDERJORDISK SJÖ
        _l[16] = 17; // ROSTIG DÖRR   → SIDO RUMMET
        _l[17] = 18; // STÄNGD KISTA  → WAMPYRERNAS GRAV
        _l[18] = 2;  // ELD I ELDSTADEN → LÄSRUMMET
        _l[19] = 3;  // BOKHYLLA      → BIBLOTEKET
        _l[20] = 1;  // SKYLT         → HALLEN
        _l[21] = 5;  // BALKONG       → TORNET
        _l[22] = 2;  // ELDSTAD AV TEGEL → LÄSRUMMET

        // Karta P[rum][riktning] (från BASIC DATA-rader 210-230)
        // N=1, S=2, E(ÖST)=3, W(VÄST)=4, U(UPP)=5, D(NER)=6

        // Rum 1: HALLEN
        _p[1, 3] = 3; _p[1, 4] = 2;   // E→BIBLOTEKET, W→LÄSRUMMET

        // Rum 2: LÄSRUMMET
        _p[2, 3] = 1;                  // E→HALLEN

        // Rum 3: BIBLOTEKET
        _p[3, 3] = 4; _p[3, 4] = 1;   // E→VAPEN KAMMAREN, W→HALLEN
        // _p[3,6] sätts till 9 när bokhyllan flyttas (DEN GÖMDA KORRIDOREN)

        // Rum 4: VAPEN KAMMAREN
        _p[4, 3] = 5; _p[4, 4] = 3;   // E→TORNET, W→BIBLOTEKET

        // Rum 5: TORNET
        _p[5, 4] = 4;                  // W→VAPEN KAMMAREN

        // Rum 6: LÄGRE TORNET
        _p[6, 2] = 7; _p[6, 5] = 5;   // S→KAPELLET, U→TORNET

        // Rum 7: KAPELLET
        _p[7, 1] = 6; _p[7, 6] = 4;   // N→LÄGRE TORNET, D→VAPEN KAMMAREN

        // Rum 8: ELDSTADEN AV TEGEL
        _p[8, 2] = 2;                  // S→LÄSRUMMET
        // _p[8,1] sätts till 10 när eldstaden slås sönder (DEN HEMLIGA PASSAGEN)

        // Rum 9: DEN GÖMDA KORRIDOREN
        _p[9, 1] = 13; _p[9, 5] = 3;  // N→ALKEMISTENS LABRATORIUM, U→BIBLOTEKET

        // Rum 10: DEN HEMLIGA PASSAGEN
        _p[10, 1] = 11; _p[10, 2] = 8; // N→EN UNDERJORDISK SJÖ, S→ELDSTADEN AV TEGEL

        // Rum 11: EN UNDERJORDISK SJÖ
        _p[11, 2] = 10;                // S→DEN HEMLIGA PASSAGEN

        // Rum 12: EN BÅT (att sitta i)
        _p[12, 2] = 11;               // S→EN UNDERJORDISK SJÖ (ta sig ur båten)

        // Rum 13: ALKEMISTENS LABRATORIUM
        _p[13, 1] = 14; _p[13, 2] = 9; // N→FÖRVARINGS RUMMET, S→DEN GÖMDA KORRIDOREN

        // Rum 14: FÖRVARINGS RUMMET
        _p[14, 2] = 13; _p[14, 5] = 2; // S→ALKEMISTENS LABRATORIUM, U→LÄSRUMMET

        // Rum 15: TAKSKÄGGET
        _p[15, 5] = 16;               // U→GALLERIET

        // Rum 16: GALLERIET (inga standardutgångar, GÅ TAKSKÄGG via specialfall)
        // _p[16,1] sätts till 17 när gobelängen tas ned (SIDO RUMMET)

        // Rum 17: SIDO RUMMET
        _p[17, 1] = 16;               // N→GALLERIET (ändras till 18 när dörren öppnas)

        // Rum 18: WAMPYRERNAS GRAV
        _p[18, 1] = 17;               // N→SIDO RUMMET

        // Bygg substantivsöksträng Os$ (2 tecken per objekt, O[1..28])
        _os = "";
        for (int i = 1; i <= 28; i++)
            _os += _o[i].Length >= 2 ? _o[i][..2] : _o[i].PadRight(2);
    }
}
