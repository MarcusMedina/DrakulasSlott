using Spectre.Console;

namespace DrakulasSlottC64Port;

/// <summary>
/// Renderar en C64-inspirerad skärmlayout:
/// - Övre 2/3: bild renderad som ANSI-block
/// - Nedre 1/3: scrollande text med typewriter-effekt
/// </summary>
public class C64Screen
{
    private readonly string? _imagePath;
    private int _textAreaTop;
    private int _currentTextRow;
    private const int TextAreaRows = 8;
    private const int TypewriterDelayMs = 18;

    public C64Screen(string? imagePath = null)
    {
        _imagePath = imagePath;
    }

    public void Initialize()
    {
        AnsiConsole.Clear();
        Console.CursorVisible = false;

        RenderImage();

        // Spara var textområdet börjar (en tom rad som separator)
        AnsiConsole.WriteLine();
        _textAreaTop = Console.CursorTop;
        _currentTextRow = 0;

        // Reservera utrymme för textområdet
        for (int i = 0; i < TextAreaRows; i++)
            AnsiConsole.WriteLine();
    }

    public void Print(string text, bool typewriter = true)
    {
        if (_currentTextRow >= TextAreaRows)
            ScrollTextArea();

        int targetRow = _textAreaTop + _currentTextRow;
        Console.SetCursorPosition(0, targetRow);
        ClearLine();

        if (typewriter)
            TypewriterPrint(text);
        else
            AnsiConsole.Markup(text);

        _currentTextRow++;
    }

    public void PrintBlank()
    {
        Print("", typewriter: false);
    }

    public void WaitForInput(string prompt = "> ")
    {
        if (_currentTextRow >= TextAreaRows)
            ScrollTextArea();

        int targetRow = _textAreaTop + _currentTextRow;
        Console.SetCursorPosition(0, targetRow);
        ClearLine();
        AnsiConsole.Markup($"[yellow]{prompt}[/]");
        Console.CursorVisible = true;
    }

    public string? ReadInput()
    {
        Console.CursorVisible = true;
        var input = Console.ReadLine();
        Console.CursorVisible = false;
        _currentTextRow++;
        return input;
    }

    public void Clear()
    {
        for (int i = 0; i < TextAreaRows; i++)
        {
            Console.SetCursorPosition(0, _textAreaTop + i);
            ClearLine();
        }
        _currentTextRow = 0;
    }

    // ── Privat ──────────────────────────────────────────────────────────────

    private void RenderImage()
    {
        if (_imagePath == null || !File.Exists(_imagePath))
        {
            RenderPlaceholder();
            return;
        }

        var image = new CanvasImage(_imagePath);
        // Sätt max bredd till terminalbredden men max 80 kolumner
        image.MaxWidth(Math.Min(Console.WindowWidth, 80));
        AnsiConsole.Write(image);
    }

    private static void RenderPlaceholder()
    {
        // Fallback: ASCII-slott om ingen bildfil finns
        var lines = new[]
        {
            "          /\\          /\\          ",
            "         /  \\   /\\   /  \\         ",
            "        /    \\ /  \\ /    \\        ",
            "       |  []  |    |  []  |       ",
            "       |      |    |      |       ",
            "  /\\   |  /\\  |    |  /\\  |   /\\ ",
            " /  \\  | /  \\ |    | /  \\ |  /  \\",
            "/____\\_|/____\\|____|/____\\|_/____\\",
            "|                                |",
            "|      DRAKULAS SLOTT            |",
            "|                                |",
            "|   Ett äventyr i mörkret        |",
            "|________________________________|",
        };

        foreach (var line in lines)
            AnsiConsole.MarkupLine($"[bold blue]{line}[/]");
    }

    private static void TypewriterPrint(string text)
    {
        foreach (char c in text)
        {
            AnsiConsole.Write(c.ToString());
            if (c != ' ')
                Thread.Sleep(TypewriterDelayMs);
        }
    }

    private void ScrollTextArea()
    {
        // Flytta alla rader ett steg uppåt
        var lines = new string[TextAreaRows];
        for (int i = 0; i < TextAreaRows; i++)
        {
            Console.SetCursorPosition(0, _textAreaTop + i);
            // Vi kan inte läsa tillbaka från terminalen — shift ner logiskt
            lines[i] = "";
        }

        // Rensa och skriv om (enklast — terminalen hanterar scrollning)
        for (int i = 0; i < TextAreaRows; i++)
        {
            Console.SetCursorPosition(0, _textAreaTop + i);
            ClearLine();
        }

        _currentTextRow = TextAreaRows - 1;
    }

    private static void ClearLine()
    {
        int width = Console.WindowWidth;
        Console.Write(new string(' ', width));
        Console.SetCursorPosition(0, Console.CursorTop);
    }
}
