namespace DrakulasSlottC64Port;

public class Program
{
    public static void Main(string[] args)
    {
        if (args.Length > 0 && args[0] == "demo")
        {
            // dotnet run -- demo [valfri bildsökväg]
            string? imagePath = args.Length > 1 ? args[1] : null;
            C64ScreenDemo.Run(imagePath);
            return;
        }

        var game = new DrakulasSlottGame();
        game.Run();
    }
}