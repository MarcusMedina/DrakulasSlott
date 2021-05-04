//----------------------------------------------------------------------------------------------
// <copyright file="FakeBasic.cs" company="MarcusMedinaPro">
// By Marcus Medina, 2021 - http://MarcusMedina.Pro
// This file is subject to the terms and conditions defined in file "license.txt"- MIT,
// which is part of this project. </copyright>
// ----------------------------------------------------------------------------------------------

namespace MarcusMedinaPro.Converter.C64
{
    using System;
    using System.Collections;
    using System.Diagnostics;
    using Console = Colorful.Console;

    /// <summary>
    /// Defines the <see cref="FakeBasic" />.
    /// </summary>
    public static class FakeBasic
    {
        /// <summary>
        /// Defines the PetschiiA.
        /// </summary>
        private const string PetschiiA = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[£]↑←─♠│──▔─││╮╰╯└╲╱┌┐●▁♥▏╭╳○♣▕♦┼▌│π◥";

        /// <summary>
        /// Defines the PetschiiB.
        /// </summary>
        private const string PetschiiB = " ▌▄▔▁▏▒▕▄◤▄├▗└┐▂┌┴┬┤▎▍▐▔▀▃▟▖▝┘▘π";

        /// <summary>
        /// Defines the Datacollection.
        /// </summary>
        private static readonly Queue Datacollection = new Queue();

        /// <summary>
        /// Defines the PosX.
        /// </summary>
        private static int PosX;

        /// <summary>
        /// Defines the PosY.
        /// </summary>
        private static int PosY;

        /// <summary>
        /// Gets a value indicating whether Reverse.
        /// </summary>
        public static bool Reverse { get; private set; }

        /// <summary>
        /// The BackColor.
        /// </summary>
        /// <param name="color">The color<see cref="C64Colors"/>.</param>
        public static void BackColor(C64Colors color) => Console.BackgroundColor = color.ToColorfulColor();

        /// <summary>
        /// The BorderColor.
        /// </summary>
        /// <param name="color">The color<see cref="C64Colors"/>.</param>
        public static void BorderColor(C64Colors color)
        {
            // Method intentionally left empty. Will be implemented later
        }

        /// <summary>
        /// The Chr.
        /// </summary>
        /// <param name="chr">The chr<see cref="int"/>.</param>
        /// <returns>The <see cref="string"/>.</returns>
        public static string Chr(int chr)
        {
            if (chr >= 32 && chr <= 127)
            {
                return PetschiiA.Substring(chr - 32, 1);
            }
            else if (chr >= 160 && chr <= 191)
            {
                return PetschiiB.Substring(chr - 160, 1);
            }
            else if (chr == 147)
            {
                ClearScreen();
            }
            return ((char)chr).ToString();
        }

        /// <summary>
        /// The ClearScreen.
        /// </summary>
        public static void ClearScreen()
        {
            Console.Clear(); PosX = 0; PosY = 0;
        }

        /// <summary>
        /// The Data.
        /// </summary>
        /// <param name="data">The data<see cref="object[]"/>.</param>
        public static void Data(params object[] data)
        {
            foreach (var item in data)
            {
                Datacollection.Enqueue(item);
            }
        }

        /// <summary>
        /// The FontColor.
        /// </summary>
        /// <param name="color">The color<see cref="C64Colors"/>.</param>
        public static void FontColor(C64Colors color) => Console.ForegroundColor = color.ToColorfulColor();

        /// <summary>
        /// The Get.
        /// </summary>
        /// <param name="output">The output<see cref="string"/>.</param>
        /// <returns>The <see cref="string"/>.</returns>
        public static string Get(string output = "")
        {
            if (output.Length != 0) Print(output);
            return Console.ReadKey().ToString().ToUpper();
        }

        /// <summary>
        /// The Input.
        /// </summary>
        /// <param name="output">The output<see cref="string"/>.</param>
        /// <returns>The <see cref="string"/>.</returns>
        public static string Input(string output = "")
        {
            output += "? ";
            Print(output);
            return Console.ReadLine().ToUpper();
        }

        /// <summary>
        /// The Left.
        /// </summary>
        /// <param name="value">The value<see cref="string"/>.</param>
        /// <param name="length">The length<see cref="int"/>.</param>
        /// <returns>The <see cref="string"/>.</returns>
        public static string Left(string value, int length) => value.Substring(0, length);

        /// <summary>
        /// The Len.
        /// </summary>
        /// <param name="str">The str<see cref="string"/>.</param>
        /// <returns>The <see cref="int"/>.</returns>
        public static int Len(string str) => str.Length;

        /// <summary>
        /// The Mid.
        /// </summary>
        /// <param name="input">The input<see cref="string"/>.</param>
        /// <param name="startPos">The startPos<see cref="int"/>.</param>
        /// <param name="length">The length<see cref="int"/>.</param>
        /// <returns>The <see cref="string"/>.</returns>
        public static string Mid(string input, int startPos, int length) => input.Substring(startPos - 1, length);

        /// <summary>
        /// The Poke.
        /// </summary>
        /// <param name="address">The address<see cref="int"/>.</param>
        /// <param name="val">The val<see cref="int"/>.</param>
        public static void Poke(int address, int val)
        {
            switch (address)
            {
                case 53280:
                    BorderColor((C64Colors)val);
                    break;

                case 53281:
                    BackColor((C64Colors)val);
                    break;

                default:
                    Debug.WriteLine("Unknown address {0}", address);
                    break;
            }
        }

        /// <summary>
        /// The Poke53280.
        /// </summary>
        /// <param name="color">The color<see cref="int"/>.</param>
        public static void Poke53280(int color) => BorderColor((C64Colors)color);

        /// <summary>
        /// The Poke53281.
        /// </summary>
        /// <param name="color">The color<see cref="int"/>.</param>
        public static void Poke53281(int color) => BackColor((C64Colors)color);

        /// <summary>
        /// The Print.
        /// </summary>
        /// <param name="output">The output<see cref="int"/>.</param>
        /// <param name="Newline">The Newline<see cref="bool"/>.</param>
        public static void Print(int output, bool Newline = true) => Print(output.ToString(), Newline);

        /// <summary>
        /// The Print.
        /// </summary>
        /// <param name="output">The output<see cref="string"/>.</param>
        /// <param name="Newline">The Newline<see cref="bool"/>.</param>
        public static void Print(string output = "", bool Newline = true)
        {
            foreach (var ch in output)
            {
                var petscIICode = ch;

                // hint: https://www.c64-wiki.com/images/a/a2/Zeichensatz-c64-poke2.jpg
                petscIICode = GetpetscIICode(ch);
                ExecutePetscII(petscIICode);
            }
            if (Newline)
            {
                PosY++;
                PosX = 0;
            }
        }

        /// <summary>
        /// The ReadInt.
        /// </summary>
        /// <returns>The <see cref="int"/>.</returns>
        public static int ReadInt() => (int)Datacollection.Dequeue();

        /// <summary>
        /// The ReadString.
        /// </summary>
        /// <returns>The <see cref="string"/>.</returns>
        public static string ReadString() => (string)Datacollection.Dequeue();

        /// <summary>
        /// The ResetConsole.
        /// </summary>
        public static void ResetConsole()
        {
            Console.OutputEncoding = System.Text.Encoding.Unicode;
            Console.Clear();
        }

        /// <summary>
        /// The Test.
        /// </summary>
        public static void Test() => Print(PetschiiB);

        private static void ExecutePetscII(char petscIICode)
        {
            switch ((int)petscIICode)
            {
                case 003: { Stop(); break; }
                case 005: { FontColor(C64Colors.White); break; }
                case 013: { PosX = 0; PosY++; break; }
                case 017: { PosY++; break; }
                case 018: { Reverse = true; break; }
                case 019: { PosX = 0; PosY = 0; break; }
                case 028: { FontColor(C64Colors.Red); break; }
                case 029: { PosX++; break; }
                case 030: { FontColor(C64Colors.Green); break; }
                case 031: { FontColor(C64Colors.Blue); break; }
                case 129: { FontColor(C64Colors.Orange); break; }
                case 141: { PosY++; PosX = 0; break; }
                case 144: { FontColor(C64Colors.Black); break; }
                case 145: { PosY--; break; }
                case 146: { Reverse = false; break; }
                case 147: { ClearScreen(); PosX = 0; PosY = 0; break; }
                case 148: { Insert(); break; }
                case 149: { FontColor(C64Colors.Brown); break; }
                case 150: { FontColor(C64Colors.LightRed); break; }
                case 151: { FontColor(C64Colors.DarkGrey); break; }
                case 152: { FontColor(C64Colors.Grey2); break; }
                case 153: { FontColor(C64Colors.LightGreen); break; }
                case 154: { FontColor(C64Colors.LightBlue); break; }
                case 155: { FontColor(C64Colors.LightGrey); break; }
                case 156: { FontColor(C64Colors.Red); break; }
                case 157: { PosX++; break; }
                case 158: { FontColor(C64Colors.Yellow); break; }
                case 159: { FontColor(C64Colors.Cyan); break; }
                default: { Console.SetCursorPosition(PosX++, PosY); System.Console.Write(petscIICode); break; }
            }
        }

        private static char GetpetscIICode(char ch) => (int)ch switch
        {
            376 => (char)159,
            92 => (char)163,
            95 => (char)171,
            96 => (char)151,
            '‘' => (char)157,
            '' => (char)29,
            '' => (char)18,
            '’' => (char)146,
            '“' => (char)147,
            97 => '♠',
            20 => '\b',
            _ => ch
        };

        /// <summary>
        /// The Insert.
        /// </summary>
        private static void Insert() => Debug.WriteLine("CHR$(148) function not coded yet");

        /// <summary>
        /// The Stop.
        /// </summary>
        private static void Stop() => Environment.Exit(0);
    }
}