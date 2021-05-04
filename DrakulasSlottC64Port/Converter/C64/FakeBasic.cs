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
        private static Queue Datacollection = new Queue();

        /// <summary>
        /// Defines the PosX.
        /// </summary>
        private static int PosX = 0;

        /// <summary>
        /// Defines the PosY.
        /// </summary>
        private static int PosY = 0;

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
                var petsciiCode = ch;

                // hint: https://www.c64-wiki.com/images/a/a2/Zeichensatz-c64-poke2.jpg

                if (ch == 376)
                {
                    petsciiCode = (char)159;
                }
                else if (ch == 92)
                {
                    petsciiCode = (char)163;
                }
                else if (ch == 95)
                {
                    petsciiCode = (char)171;
                }
                else if (ch == 96)
                {
                    petsciiCode = (char)151;
                }
                else if (ch == '‘')
                {
                    petsciiCode = (char)157;
                }
                else if (ch == '')
                {
                    petsciiCode = (char)29;
                }
                else if (ch == '') { petsciiCode = (char)18; }
                else if (ch == '’') { petsciiCode = (char)146; }
                else if (ch == '‘') { petsciiCode = (char)145; }
                else if (ch == '“') { petsciiCode = (char)147; }
                else if (ch == 97)
                {
                    petsciiCode = '♠';
                }
                else if (ch == 20)
                {
                    petsciiCode = '\b';
                }

                if (petsciiCode == 147)
                {
                    ClearScreen();
                    PosX = 0;
                    PosY = 0;
                }
                else if (petsciiCode == 3)
                {
                    Stop();
                }
                else if (petsciiCode == 5)
                {
                    FontColor(C64Colors.White);
                }
                else if (petsciiCode == 17)
                {
                    PosY++;
                }
                else if (petsciiCode == 18)
                {
                    Reverse = true;
                }
                else if (petsciiCode == 19) { PosX = 0; PosY = 0; }
                else if (petsciiCode == 28)
                {
                    FontColor(C64Colors.Red);
                }
                else if (petsciiCode == 29)
                {
                    PosX++;
                }
                else if (petsciiCode == 30)
                {
                    FontColor(C64Colors.Green);
                }
                else if (petsciiCode == 31)
                {
                    FontColor(C64Colors.Blue);
                }
                else if (petsciiCode == 129)
                {
                    FontColor(C64Colors.Orange);
                }
                else if (petsciiCode == 141) { PosY++; PosX = 0; } // Shift return
                else if (petsciiCode == 144)
                {
                    FontColor(C64Colors.Black);
                }
                else if (petsciiCode == 145)
                {
                    PosY--;
                }
                else if (petsciiCode == 146)
                {
                    Reverse = false;
                }
                else if (petsciiCode == 147)
                {
                    ClearScreen();
                }
                else if (petsciiCode == 148)
                {
                    Insert();
                }
                else if (petsciiCode == 149)
                {
                    FontColor(C64Colors.Brown);
                }
                else if (petsciiCode == 150)
                {
                    FontColor(C64Colors.LightRed); //pink
                }
                else if (petsciiCode == 151)
                {
                    FontColor(C64Colors.DarkGrey);
                }
                else if (petsciiCode == 152)
                {
                    FontColor(C64Colors.Grey2);
                }
                else if (petsciiCode == 153)
                {
                    FontColor(C64Colors.LightGreen);
                }
                else if (petsciiCode == 154)
                {
                    FontColor(C64Colors.LightBlue);
                }
                else if (petsciiCode == 155)
                {
                    FontColor(C64Colors.LightGrey);
                }
                else if (petsciiCode == 156)
                {
                    FontColor(C64Colors.Red); //purple
                }
                else if (petsciiCode == 157)
                {
                    PosX++;
                }
                else if (petsciiCode == 158)
                {
                    FontColor(C64Colors.Yellow);
                }
                else if (petsciiCode == 159)
                {
                    FontColor(C64Colors.Cyan);
                }
                else if (petsciiCode == 13) { PosX = 0; PosY++; }
                else
                {
                    Console.SetCursorPosition(PosX++, PosY);
                    System.Console.Write(petsciiCode);
                }
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
