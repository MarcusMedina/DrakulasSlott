//----------------------------------------------------------------------------------------------
// <copyright file="program.cs" company="Codic Education">
// By Marcus Medina, 2021 - http://MarcusMedina.Pro
// This file is subject to the terms and conditions defined in file "license.txt"- GNU3,
// which is part of this project. </copyright>
// ----------------------------------------------------------------------------------------------

namespace DrakulasSlott
{
    using DrakulasSlott.Game;

    /// <summary>
    /// Defines the <see cref="Program" />.
    /// </summary>
    internal static class Program
    {
        /// <summary>
        /// The Main.
        /// </summary>
        internal static void Main()
        {
            while (DrakulasSlott.Run() == 1) ;
        }
    }
}