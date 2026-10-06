namespace DrakulasSlottC64Port;

/// <summary>
/// Kör en snabb demo av C64Screen-layouten utan att starta spelet.
/// Anrop: dotnet run -- demo
/// </summary>
public static class C64ScreenDemo
{
    public static void Run(string? imagePath = null)
    {
        var screen = new C64Screen(imagePath);
        screen.Initialize();

        var lines = new[]
        {
            "Du befinner dig i ett mörkt slott.",
            "Det luktar fukt och gammalt blod.",
            "En fladdermus flyger förbi ditt huvud.",
            "",
            "Utgångar: NORR, SÖDER",
            "",
        };

        foreach (var line in lines)
        {
            if (line == "")
                screen.PrintBlank();
            else
                screen.Print(line);

            Thread.Sleep(200);
        }

        screen.WaitForInput();
        screen.ReadInput();
    }
}
