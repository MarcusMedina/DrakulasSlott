using System.Drawing;

namespace MarcusMedinaPro.Converter.C64
{

    public enum C64Colors
    {
        Black = 0,
        White = 1,
        Red = 2,
        Cyan = 3,
        Violet = 4,
        Green = 5,
        Blue = 6,
        Yellow = 7,
        Orange = 8,
        Brown = 9,
        LightRed = 10,
        DarkGrey = 11,
        Grey2 = 12,
        LightGreen = 13,
        LightBlue = 14,
        LightGrey = 15
    }

    public static class C64ColorsExtension
    {
        public static Color ToColorfulColor(this C64Colors color)
        {
            color = (C64Colors)((int)color % 15);
            return color switch
            {
                C64Colors.Black => Color.Black,
                C64Colors.White => Color.White,
                C64Colors.Red => Color.Red,
                C64Colors.Cyan => Color.Cyan,
                C64Colors.Violet => Color.Violet,
                C64Colors.Green => Color.Green,
                C64Colors.Blue => Color.Blue,
                C64Colors.Yellow => Color.Yellow,
                C64Colors.Orange => Color.Orange,
                C64Colors.Brown => Color.Brown,
                C64Colors.LightRed => Color.IndianRed,
                C64Colors.DarkGrey => Color.DarkRed,
                C64Colors.LightGreen => Color.GreenYellow,
                C64Colors.Grey2 => Color.DarkSlateGray,
                C64Colors.LightBlue => Color.LightBlue,
                C64Colors.LightGrey => Color.LightGray,
                _ => Color.Black,
            };
        }
    }

}