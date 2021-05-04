//----------------------------------------------------------------------------------------------
// <copyright file="C64Colors.cs" company="MarcusMedinaPro">
// By Marcus Medina, 2021 - http://MarcusMedina.Pro 
// This file is subject to the terms and conditions defined in file "license.txt"- MIT, 
// which is part of this project. </copyright>
// ----------------------------------------------------------------------------------------------

namespace MarcusMedinaPro.Converter.C64
{
    using System.Drawing;

    /// <summary>
    /// Defines the C64Colors.
    /// </summary>
    public enum C64Colors
    {
        /// <summary>
        /// Defines the Black.
        /// </summary>
        Black = 0,

        /// <summary>
        /// Defines the White.
        /// </summary>
        White = 1,

        /// <summary>
        /// Defines the Red.
        /// </summary>
        Red = 2,

        /// <summary>
        /// Defines the Cyan.
        /// </summary>
        Cyan = 3,

        /// <summary>
        /// Defines the Violet.
        /// </summary>
        Violet = 4,

        /// <summary>
        /// Defines the Green.
        /// </summary>
        Green = 5,

        /// <summary>
        /// Defines the Blue.
        /// </summary>
        Blue = 6,

        /// <summary>
        /// Defines the Yellow.
        /// </summary>
        Yellow = 7,

        /// <summary>
        /// Defines the Orange.
        /// </summary>
        Orange = 8,

        /// <summary>
        /// Defines the Brown.
        /// </summary>
        Brown = 9,

        /// <summary>
        /// Defines the LightRed.
        /// </summary>
        LightRed = 10,

        /// <summary>
        /// Defines the DarkGrey.
        /// </summary>
        DarkGrey = 11,

        /// <summary>
        /// Defines the Grey2.
        /// </summary>
        Grey2 = 12,

        /// <summary>
        /// Defines the LightGreen.
        /// </summary>
        LightGreen = 13,

        /// <summary>
        /// Defines the LightBlue.
        /// </summary>
        LightBlue = 14,

        /// <summary>
        /// Defines the LightGrey.
        /// </summary>
        LightGrey = 15
    }

    /// <summary>
    /// Defines the <see cref="C64ColorsExtension" />.
    /// </summary>
    public static class C64ColorsExtension
    {
        /// <summary>
        /// To ColorfulColor converter.
        /// </summary>
        /// <param name="color">The color<see cref="C64Colors"/>.</param>
        /// <returns>The <see cref="Color"/>.</returns>
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
