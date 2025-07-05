using System.Drawing;
using System.IO;
using Console = Colorful.Console;

namespace DrakulasSlottC64Port;

public class DrakulasSlottGame
{
    private const string LogFileName = "gamelog.txt";

    // BASIC: 100 DIM D$(18),O$(28),L(22),P(18, 6)
    // Vi använder 1-baserad indexering för att efterlikna BASIC, så vi gör arrayerna en större.
    // BUGGFIX: _p måste vara [21, 7] för att rymma rum 19 och 20 för vampyren.
    private readonly string[] _d = new string[19]; // Rumsnamn
    private readonly string[] _o = new string[29]; // Objekts- och kommandonamn
    private readonly int[] _l = new int[23]; // Objektens placering (0 = hos spelaren)
    private readonly int[,] _p = new int[21, 7]; // Karta/utgångar

    private int _playerL = 1; // Spelarens nuvarande rum
    private int _playerL2 = 1; // Spelarens förra rum

    private readonly string _w = "GÅTASELÄSLÖPANHJ"; // Verb-lista för kommandon i switch-satsen.

    private string _oCommandString = string.Empty; // Substantiv-lista för parsning

    private int _t1 = 0; // Minuter
    private int _t2 = 20; // Timmar (startar kl 20)

    private string _a = string.Empty; // Parsat verb
    private string _b = string.Empty; // Parsat substantiv
    private int _f = 0; // Index för verbet
    private int _s = 0; // Index för substantivet

    private int _c = 0; // Antal föremål som spelaren bär
    private int _fi = 0; // Flagga för elden (FI)
    private int _oi = 0; // Flagga för oljad dörr (OI)
    private int _v = 19; // Vampyrens position (V)
    private int _bi = 0; // Antal bett (BI)

    private readonly Random _random = new();

    #region Logging & Console Wrappers

    private void Log(string message)
    {
        File.AppendAllText(LogFileName, $"[{DateTime.Now:HH:mm:ss}] {message}\n");
    }

    private void Print(string text, Color? color = null, bool newLine = true)
    {
        Log($"OUT: {text}");
        if (color.HasValue)
        {
            if (newLine) Console.WriteLine(text, color.Value);
            else Console.Write(text, color.Value);
        }
        else
        {
            if (newLine) Console.WriteLine(text);
            else Console.Write(text);
        }
    }

    private string ReadAndLogLine()
    {
        string input = Console.ReadLine() ?? "";
        Log($"INP: {input}");
        return input.ToUpper();
    }

    private void ClearLog()
    {
        if (File.Exists(LogFileName))
        {
            File.Delete(LogFileName);
        }
    }

    #endregion

    public void Run()
    {
        InitializeData();
        ClearLog();

        Console.BackgroundColor = Color.Blue;
        Console.ForegroundColor = Color.Yellow;
        Console.Clear();

        Print("\n\n            DRAKULAS SLOTT");

        while (true)
        {
            Log("-- TURN START --");
            Log($"STATE: PlayerL={_playerL}, T1={_t1}, T2={_t2}, V={_v}, BI={_bi}, C={_c}, FI={_fi}, OI={_oi}");

            Print($"\nJAG ÄR I {_d[_playerL]}");
            _playerL2 = _playerL;

            bool isDark = _l[12] != 0 && (_playerL == 10 || _playerL == 11 || _playerL == 12 || _playerL == 18);
            if (isDark)
            {
                Print("DET ÄR MÖRKT JAG KAN INTE SE");
            }
            else
            {
                string objectsString = "JAG SER ";
                int visibleObjectsCount = 0;
                for (int x = 1; x <= 22; x++)
                {
                    if (_l[x] == _playerL2)
                    {
                        objectsString += $" *{_o[x + 6]}";
                        visibleObjectsCount++;
                    }
                }
                if (visibleObjectsCount == 0) objectsString += "INGENTING";
                Print(objectsString);

                string exitsString = "\nSYNLIGA UTGÅNGAR - ";
                for (int x = 1; x <= 6; x++)
                {
                    if (_p[_playerL, x] > 0) exitsString += $"{_o[x]}* ";
                }
                Print(exitsString);
            }

            Print("\nVAD SKALL JAG GÖRA? ", null, false);
            string fullInput = ReadAndLogLine();
            Print(""); // Newline after input

            _s = 0;
            _f = 0;
            _b = string.Empty;

            int firstSpace = fullInput.IndexOf(' ');
            if (firstSpace != -1 && fullInput.Length > firstSpace + 2)
            {
                _b = fullInput.Substring(firstSpace + 1, 2);
            }
            _a = fullInput.Length > 1 ? fullInput[..2] : fullInput;

            for (int i = 0; i < _w.Length; i += 2) { if (_w.Substring(i, 2) == _a) { _f = (i / 2) + 1; break; } }
            for (int i = 0; i < _oCommandString.Length; i += 2) { if (_oCommandString.Substring(i, 2) == _b) { _s = (i / 2) + 1; break; } }

            _t1++;
            if (_t1 == 60) { _t1 = 0; _t2++; }
            if (_t2 == 24) { _t2 = 0; }
            if (_t2 == 8 && _playerL != 18) { Print("VAMPYREN HAR RYMT - DIN TID ÄR UTE !"); break; }

            if (_a == "IN")
            {
                Print("JAG BÄR FÖLJANDE SAKER");
                int carriedItems = 0;
                for (int x = 1; x <= 22; x++) { if (_l[x] == 0) { Print(_o[x + 6]); carriedItems++; } }
                if (carriedItems == 0) Print("INGENTING");
                continue;
            }

            if (_f < 1) { Print("JAG FÖRSTÅR INTE !"); continue; }

            switch (_f)
            {
                case 1: // GÅ
                    if (_s >= 1 && _s <= 6) { if (_p[_playerL, _s] > 0) _playerL = _p[_playerL, _s]; else Print("JAG KAN INTE GÅ DIT"); } else { Print("VART SKA JAG GÅ?"); }
                    break;
                case 2: // TA
                    if (_s < 7) { Print("JAG FÖRSTÅR INTE!"); break; }
                    if (_c >= 6) { Print("JAG BÄR FÖR MYCKET"); break; }
                    if (_l[_s - 6] == _playerL) { _l[_s - 6] = 0; _c++; Print("OK"); } else { Print("JAG SER DEN INTE"); }
                    break;
                case 3: // SE
                    switch (_s) {
                        case 8: if (_l[2] == 0) Print($"{_t2:00}:{_t1:00}"); else Print("DEN HAR JAG INTE"); break;
                        case 10: if (_l[4] == 0) Print("ALLA UTGÅNGAR ÄR INTE SYNLIGA"); else Print("DEN HAR JAG INTE"); break;
                        case 26: if (_playerL == 1) Print("VAMPYREN VAKNAR VID MIDNATT"); else Print("JAG SER DEN INTE"); break;
                        default: Print("JAG SER INGET SPECIELLT MED DEN."); break;
                    }
                    break;
                case 4: // LÄGGA
                    if (_s == 14 && _l[8] == 0 && _playerL == 2) { _o[24] = "ASKA"; _fi = 1; _l[8] = 99; _c--; Print("OK"); break; }
                    if (_s < 7) { Print("VA ??"); break; }
                    if (_l[_s - 6] == 0) { _l[_s - 6] = _playerL; _c--; Print("OK"); } else { Print("DEN HAR JAG INTE"); }
                    break;
                case 5: // SLÅ
                    bool canSlåLåda = (_s == 16 && _l[10] == _playerL && _l[5] == 0);
                    bool canSlåEldstad = (_s == 28 && _l[1] == 0 && _playerL == 8);
                    if (!canSlåLåda && !canSlåEldstad) { Print("INGENTING HÄNDE"); break; }
                    Print("MED VAD? ", null, false);
                    string tool = ReadAndLogLine();
                    if (tool.Length > 1) tool = tool[..2];
                    if (canSlåLåda && tool == "YX") { _o[16] = "TRÄPÅLAR"; Print("DU SLOG SÖNDER LÅDAN TILL NÅGRA TRÄPÅLAR"); }
                    else if (canSlåEldstad && tool == "SL") { _o[28] = "EN SÖNDERSLAGEN ELDSTAD"; _p[8, 1] = 10; _d[8] = _o[28]; Print("OK"); }
                    else { Print("INGENTING HÄNDE"); }
                    break;
                case 6: // ÖPPNA
                    if (_s == 23 && _playerL == 18 && _l[7] == 0) { _o[23] = "VAMPYR I KISTA"; Print("OK"); }
                    else if (_playerL == 17 && _s == 22 && _oi == 1 && _l[7] == 0) { _o[22] = "ÖPPEN DÖRR"; _p[17, 1] = 18; Print("OK"); }
                    else { Print("INGENTING HÄNDE"); }
                    break;
                case 7: // ANVÄNDA
                    if (_s == 15 && _l[9] == 0 && _playerL == 17) { Print("OK"); _oi = 1; _c--; _l[9] = 99; break; }
                    if (_s == 16 && _playerL == 18 && _l[10] == 0 && _o[23] == "VAMPYR I KISTA") { Print("DU HAR PREJAT VAMPYREN - DU HAR VUNNIT!"); return; }
                    if (_s == 11 && _l[5] == 0 && _playerL == _v) { _v = 20; Print("OK"); break; }
                    if (_s == 12 && _l[6] == 0 && _playerL == _v) { _v = 20; Print("OK"); break; }
                    Print("INGENTING HÄNDE");
                    break;
                case 8: // HJÄLP
                    Print("JAG FÖRSTÅR FÖLJANDE VERB");
                    string help = "";
                    for (int i = 7; i <= 15; i++) help += _o[i] + " ";
                    Print(help);
                    break;
                default:
                    Print("JAG FÖRSTÅR INTE!");
                    break;
            }

            // Vampire logic: active between midnight (0) and 7am.
            if (_t2 < 7)
            {
                MoveVampire();
                if (_v == _playerL)
                {
                    Print("VAMPYREN ÄR HÄR", Color.Red);
                    if (_l[5] == 0) { Print("VAMPYREN RYGGAR TILLBAKA FÖR VITLÖKEN"); }
                    else if (_l[6] == 0) { Print("VAMPYREN RYGGAR TILLBAKA FÖR KORSET"); }
                    else
                    {
                        Print("VAMPYREN BITER DIG I HALSEN OCH DU SVIMMAR AV");
                        _playerL = _random.Next(1, 19); // Thrown into a random room (1-18)
                        _bi++;
                        if (_bi >= 4)
                        {
                            Print("DU ÄR NU EN VAMPYR-TJÄNARE...");
                            break; // Game Over
                        }
                    }
                }
            }
        }
    }

    private void MoveVampire()
    {
        if (_v == 20) return; // Fled
        int nextRoom;
        do { nextRoom = _p[_v, _random.Next(1, 7)]; } while (nextRoom == 0);
        _v = nextRoom;
    }

    private void InitializeData()
    {
        _d[1] = "HALLEN"; _d[2] = "LÄSRUMMET"; _d[3] = "VAPENKAMMAREN"; _d[4] = "SKATTKAMMAREN";
        _d[5] = "BRUNNEN"; _d[6] = "KÄLLAREN"; _d[7] = "TUNNELN"; _d[8] = "KAPELLET";
        _d[9] = "TORTYRKAMMAREN"; _d[10] = "LÖNNGÅNGEN"; _d[11] = "GROTTAN"; _d[12] = "UNDERJORDISK SJÖ";
        _d[13] = "BÅTEN"; _d[14] = "STRANDEN"; _d[15] = "KÖKET"; _d[16] = "FÖRRÅDET";
        _d[17] = "SIDORUMMET"; _d[18] = "GRAVKAMMAREN";

        _o[1] = "N"; _o[2] = "S"; _o[3] = "V"; _o[4] = "Ö"; _o[5] = "U"; _o[6] = "N";
        _o[7] = "GÅ"; _o[8] = "TA"; _o[9] = "SE"; _o[10] = "LÄGGA"; _o[11] = "SLÅ"; _o[12] = "ÖPPNA";
        _o[13] = "ANVÄNDA"; _o[14] = "HJÄLP"; _o[15] = "INVENTERA";
        _o[16] = "SLÄGGA"; _o[17] = "KLOCKA"; _o[18] = "FACKLA"; _o[19] = "PERGAMENT RULLE";
        _o[20] = "YXA"; _o[21] = "KORS"; _o[22] = "NYCKEL"; _o[23] = "HELIGT VATTEN";
        _o[24] = "OLJA"; _o[25] = "LÅDA"; _o[26] = "BÅT"; _o[27] = "SPADE";
        _o[28] = "KISTA";

        _l[1] = 3; _l[2] = 1; _l[3] = 2; _l[4] = 4; _l[5] = 9; _l[6] = 8;
        _l[7] = 4; _l[8] = 5; _l[9] = 6; _l[10] = 7; _l[11] = 12; _l[12] = 11;
        _l[13] = 14; _l[14] = 15; _l[15] = 16; _l[16] = 17; _l[17] = 18; _l[18] = 10;
        _l[19] = 1; _l[20] = 2; _l[21] = 8; _l[22] = 17;

        _o[23] = "KISTA"; _o[24] = "ELD I ELDSTADEN"; _o[25] = "SPINDELVÄV";
        _o[26] = "SKYLT"; _o[27] = "VÄGG"; _o[28] = "ELDSTAD";

        for (int i = 1; i <= 28; i++) { if (_o[i].Length >= 2) _oCommandString += _o[i][..2]; }

        int[] mapData = { 2,5,0,0,0,0, 1,4,3,0,0,0, 2,0,0,0,0,0, 2,7,0,5,0,0, 1,6,4,0,0,0, 5,0,0,0,0,0, 4,9,8,0,0,0, 7,0,0,0,0,0, 7,0,0,0,0,0, 11,0,0,0,0,0, 12,10,0,0,0,0, 13,0,11,0,0,0, 14,0,12,0,0,0, 0,15,13,0,0,0, 14,16,0,0,0,0, 15,17,0,0,0,0, 0,0,16,0,0,0, 0,0,0,0,0,0 };
        int mapIndex = 0;
        for (int i = 1; i <= 18; i++) { for (int j = 1; j <= 6; j++) { _p[i, j] = mapData[mapIndex++]; } }
    }
}
