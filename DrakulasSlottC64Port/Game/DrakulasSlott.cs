#pragma warning disable IDE0059 // 'Unnecessary assignment of a value' nagging

namespace DrakulasSlott.Game
{
    using System;
    using static MarcusMedinaPro.Converter.C64.FakeBasic;

    /// <summary>
    /// Defines the <see cref="DrakulasSlott" />.
    /// </summary>
    internal static class DrakulasSlott
    {
        /// <summary>
        /// The Run.
        /// </summary>
        /// <returns>The <see cref="int"/>.</returns>
        internal static int Run()
        {
            // Declare variables to default values to avoid confusion
            var A = 0;
            var C = 0;
            var F = 0;
            var FI = 0;
            var L = 0;
            var L2 = 0;
            var OI = 0;
            var S = 0;
            var T1 = 0;
            var T2 = 0;
            var TA = 0;
            var X = 0;
            var Y = 0;
            var As = "";
            var Bs = "";
            var Os = "";
            var TGPs = "";
            var Ws = "";
            Splash();

            // -------------Data moved to top-------------
            Data("HALLEN", "LÄSRUMMET", "BIBLOTEKET", "VAPEN KAMMAREN");
            Data("TORNET", "LÄGRE TORNET", "KAPELLET", "ELDSTADEN AV TEGEL", "DEN GÖMDA KORRIDOREN");
            Data("DEN HEMLIGA PASSAGEN", "EN UNDERJORDISK SJÖ", "EN BÅT", "ALKEMISTENS LABRATORIUM");
            Data("FÖRVARINGS RUMMET", "TAKSKÄGGET", "GALLERIET", "SIDO RUMMET", "WAMPYRERNAS GRAV");
            Data("NORR", "SÖDER", "ÖST", "VÄST", "UPP", "NER", "SLÄGGA", 5);
            Data("KLOCKA", 1, "REP", 9);
            Data("PERGAMENT RULLE", 3, "YXA", 4, "ÅROR", 6);
            Data("NYCKEL", 7, "HELIGT VATTEN", 7);
            Data("OLJE FLASKA", 13, "LÅDA", 14);
            Data("HINK", 14);
            Data("FACKLA", 8);
            Data("SPIKAR");
            Data(15);
            Data("GOBELÄNG", 16, "BÅT", 11, "ROSTIG DÖRR", 17, "STÄNGD KISTA", 18);
            Data("ELD I ELDSTADEN", 2, "BOKHYLLA", 3);
            Data("SKYLT", 1, "BALKONG", 5);
            Data("ELDSTAD AV TEGEL", 2);
            Data(0, 0, 3, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0, 5, 3, 0, 0, 0, 0, 0, 4, 0, 0, 0, 7, 0, 0, 5, 0, 6, 0, 0, 0, 4, 0);
            Data(0, 2, 0, 0, 0, 0, 13, 0, 0, 0, 3, 0, 11, 8, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 14, 9, 0, 0, 0, 0, 0, 13, 0, 0, 2, 0, 0);
            Data(0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0);

            // ------------------Data end-----------------
            // 10 POKE53280,6:POKE 53281,0:PRINT"Ÿ"
            Poke(53280, 6);
            Poke(53281, 0);
            Print("Ÿ");

            // 20 PRINT"“            DRAKULAS SLOTT"
            Print("“            DRAKULAS SLOTT");

            // 100 DIMD$(18),O$(28),L(22),P(18,6):L=1:L2=L
            var Dsa = new string[19];
            var Osa = new string[29];
            var La = new int[23];
            var Pa = new int[19, 7];
            L = 1;
            L2 = L;

            // 110 FORX=1TO18:READD$(X):NEXT:DATAHALLEN,LÄSRUMMET,BIBLOTEKET,VAPEN KAMMAREN
            for (X = 1; X <= 18; X++)
            {
                Dsa[X] = ReadString();
            }

            // 120 DATATORNET,LÄGRE TORNET,KAPELLET,ELDSTADEN AV TEGEL,DEN GÖMDA KORRIDOREN
            // 130 DATADEN HEMLIGA PASSAGEN,EN UNDERJORDISK SJÖ,EN BÅT,ALKEMISTENS LABRATORIUM
            // 140 DATAFÖRVARINGS RUMMET,TAKSKÄGGET,GALLERIET,SIDO RUMMET,WAMPYRERNAS GRAV
            // 150 FORX=1TO28:READO$(X)
            for (X = 1; X <= 28; X++)
            {
                Osa[X] = ReadString();

                // 151 O$=O$+LEFT$(O$(X),2)
                Os += Left(Osa[X], 2);

                // 152 IFX>6THENREADL(X-6)
                if (X > 6)
                {
                    La[X - 6] = ReadInt();
                }

                // 160 NEXT
            }

            // 162 DATANORR,SÖDER,ÖST,VÄST,UPP,NER,SLÄGGA,5
            // 170 DATAKLOCKA,1,REP,9
            // 171 DATAPERGAMENT RULLE,3,YXA,4,ÅROR,6
            // 172 DATANYCKEL,7,HELIGT VATTEN,7
            // 180 DATAOLJE FLASKA,13,LÅDA,14
            // 181 DATAHINK,14
            // 184 DATAFACKLA,8
            // 186 DATASPIKAR
            // 187 DATA15
            // 193 DATAGOBELÄNG,16,BÅT,11,ROSTIG DÖRR,17,STÄNGD KISTA,18
            // 195 DATAELD I ELDSTADEN,2,BOKHYLLA,3
            // 200 DATASKYLT,1,BALKONG,5
            // 201 DATAELDSTAD AV TEGEL,2
            // 203 FORY=1TO18:FORX=1TO6:READP(Y,X):NEXTX,Y
            for (Y = 1; Y <= 18; Y++)
            {
                for (X = 1; X <= 6; X++)
                {
                    Pa[Y, X] = ReadInt();
                }
            }

            // 210 DATA,,3,2,,,,,1,,,,,,4,1,,,,,5,3,,,,,,4,,,,7,,,5,,6,,,,4,
            // 220 DATA,2,,,,,13,,,,3,,11,8,,,,,,10,,,,,,11,,,,,14,9,,,,,,13,,,2,,
            // 230 DATA,,,,16,,,,,,,,16,,,,,,17,,,,,
            // 240 W$="GÅTASELÄSLÖPBIFLDÖOLRO"
            Ws = "GÅTASELÄSLÖPBIFLDÖOLRO";

            // 245 T2=20
            T2 = 20;

        // 250 PRINT"“            DRAKULAS SLOTT"
        Row250:
            Print("“            DRAKULAS SLOTT");

            // 251 PRINT" JAG ÄR I ";D$(L):Y=0:L2=L:PRINT
            Print(" JAG ÄR I " + Dsa[L]);
            Y = 0;
            L2 = L;
            Print();

            // 260 IFL(12)<>0AND(L=10ORL=11ORL=12ORL=18)THEN280
            if (La[12] != 0 && (L == 10 || L == 11 || L == 12 || L == 18))
            {
                goto Row280;
            }

            // 270 GOTO290
            goto Row290;

        // 280 PRINT"DET ÄR MÖRKT JAG KAN INTE SE":GOTO330
        Row280:
            Print("DET ÄR MÖRKT JAG KAN INTE SE");
            goto Row330;

        // 290 PRINT"JAG SER ";:FORX=1TO22:IF(L(X)=L2)THENPRINT" *"+O$(X+6);:Y=Y+1
        Row290:
            Print("JAG SER ", false);
            for (X = 1; X <= 22; X++)
            {
                if ((La[X] == L2))
                {
                    Print(" *" + Osa[X + 6], false);
                    Y++; ;
                }

                // 300 NEXT:IFY=0THENPRINT"INGENTING‘"
            }
            if (Y == 0)
            {
                Print("INGENTING‘");
            }

            // 305 PRINT:PRINT
            Print();
            Print();

            // 310 PRINT"SYNLIGA UTGÅNGAR - ";:FORX=1TO6:IFP(L,X)>0THENPRINTO$(X);"* ";
            Print("SYNLIGA UTGÅNGAR - ", false);
            for (X = 1; X <= 6; X++)
            {
                if (Pa[L, X] > 0)
                {
                    Print(Osa[X] + "* ", false);
                }

                // 320 NEXT:PRINT
            }
            Print();

        // 330 PRINT  :S=0:F=0:INPUT"VAD SKALL JAG GÖRA ";A$:PRINT:B$=""
        Row330:
            Print();
            S = 0;
            F = 0;
            As = Input("VAD SKALL JAG GÖRA "); //TODO: Chech that all parameters are there
            Print();
            Bs = "";

            // 335 FORX=1TOLEN(A$)
            for (X = 1; X <= Len(As); X++)
            {
                // 340 IFMID$(A$,X,1)=" "ANDLEN(A$)>X+1THENB$=MID$(A$,X+1,2)
                if (Mid(As, X, 1) == " " && Len(As) > X + 1)
                {
                    Bs = Mid(As, X + 1, 2);
                }

                // 350 NEXT:GOSUB360:GOTO380
            }
            Gosub360();
            goto Row380;

            // 360 IFLEN(A$)>1THENA$=LEFT$(A$,2)
            void Gosub360()
            {
                if (Len(As) > 1)
                {
                    As = Left(As, 2);
                }

                // 370 RETURN
                // Return from Gosub
            }

        // 380 L2=L
        Row380:
            L2 = L;

            // 385 T1=T1+1
            T1++; ;

            // 386 IFT1=60THENT1=0:T2=T2+1
            if (T1 == 60)
            {
                T1 = 0;
                T2++; ;
            }

            // 400 IFB$="DÖ"THENB$="RO"
            if (Bs == "DÖ")
            {
                Bs = "RO";
            }

            // 405 IFT2=24THENPRINT"VAMPYREN HAR RYMT - DIN TID ÄR UTE !":GOTO1200
            if (T2 == 24)
            {
                Print("VAMPYREN HAR RYMT-DIN TID ÄR UTE !");
                goto Row1200;
            }

            // 410 IFB$="FL"THENB$="OL"
            if (Bs == "FL")
            {
                Bs = "OL";
            }

            // 415 IFA$="DÖ"ANDB$="VA"ANDL=18THEN1060
            if (As == "DÖ" && Bs == "VA" && L == 18)
            {
                goto Row1060;
            }

            // 425 IFB$="KI"THENB$="ST"
            if (Bs == "KI")
            {
                Bs = "ST";
            }

            // 430 IFA$="SI"ANDL=11THENPRINT"DU DRUNKNADE I DET ISKALLA VATTNET":GOTO1200
            if (As == "SI" && L == 11)
            {
                Print("DU DRUNKNADE I DET ISKALLA VATTNET");
                goto Row1200;
            }

            // 432 IFA$="SI"THENPRINT"JAG SER INGET VATTEN":GOTO330
            if (As == "SI")
            {
                Print("JAG SER INGET VATTEN");
                goto Row330;
            }

            // 435 IFA$="GÅ"ANDB$="TA"ANDL=16THENL=15:GOTO250
            if (As == "GÅ" && Bs == "TA" && L == 16)
            {
                L = 15;
                goto Row250;
            }

            // 437 IFB$="VA"THENB$="HE"
            if (Bs == "VA")
            {
                Bs = "HE";
            }

            // 440 IFA$="HJ"THEN1150
            if (As == "HJ")
            {
                goto Row1150;
            }

            // 445 IF(B$="TR"ORB$="PÅ")ANDO$(16)="TRÄPÅLAR"THENB$="LÅ"
            if ((Bs == "TR" || Bs == "PÅ") && Osa[16] == "TRÄPÅLAR")
            {
                Bs = "LÅ";
            }

            // 450 FORX=1TOLEN(W$)STEP2:IFMID$(W$,X,2)=A$THENF=(X+1)/2
            for (X = 1; X <= Len(Ws); X += 2)
            {
                if (Mid(Ws, X, 2) == As)
                {
                    F = (X + 1) / 2;
                }

                // 460 NEXT:FORX=1TOLEN(O$)STEP2:IFMID$(O$,X,2)=B$THENS=(X+1)/2
            }
            for (X = 1; X <= Len(Os); X += 2)
            {
                if (Mid(Os, X, 2) == Bs)
                {
                    S = (X + 1) / 2;
                }

                // 470 NEXT:IFA$<>"IN"THEN500
            }
            if (As != "IN")
            {
                goto Row500;
            }

            // 480 PRINT"JAG BÄR FÖLJANDE SAKER":A=0:FORX=1TO22:IFL(X)=0THENPRINTO$(X+6):A=A+1
            Print("JAG BÄR FÖLJANDE SAKER");
            A = 0;
            for (X = 1; X <= 22; X++)
            {
                if (La[X] == 0)
                {
                    Print(Osa[X + 6]);
                }
                A++; ;

                // 490 NEXT:IFA>0THEN330
            }
            if (A > 0)
            {
                goto Row330;
            }

            // 495 PRINT"INGENTING":GOTO330
            Print("INGENTING");
            goto Row330;

        // 500 IFF<1THENPRINT"JAG FÖRSTÅR INTE !":GOTO330
        Row500:
            if (F < 1)
            {
                Print("JAG FÖRSTÅR INTE !");
                goto Row330;
            }

            // 510 ONF-1GOTO640,790,870,905,950,1000,1030,1050,1100,1120
            switch (F - 1)
            {
                case 1: goto Row640;
                case 2: goto Row790;
                case 3: goto Row870;
                case 4: goto Row905;
                case 5: goto Row950;
                case 6: goto Row1000;
                case 7: goto Row1030;
                case 8: goto Row1050;
                case 9: goto Row1100;
                case 10: goto Row1120;
                default: Print("Error in ON GOTO F-1 "); break;
            }

            // 512 IFA$<>"GÅ"THENF=-1:GOTO500
            if (As != "GÅ")
            {
                F = -1;
                goto Row500;
            }

            // 520 IFS<1ORS>6THEN540
            if (S < 1 || S > 6)
            {
                goto Row540;
            }

            // 530 IFP(L,S)>0THENL=P(L,S):GOTO250
            if (Pa[L, S] > 0)
            {
                L = Pa[L, S];
                goto Row250;
            }

        // 540 IFB$<>"EL"ORL<>2THEN570
        Row540:
            if (Bs != "EL" || L != 2)
            {
                goto Row570;
            }

            // 550 IFFI=0THENPRINT"DU BRÄNDES TILL DÖDS":GOTO1200
            if (FI == 0)
            {
                Print("DU BRÄNDES TILL DÖDS");
                goto Row1200;
            }

            // 560 L=8:GOTO250
            L = 8;
            goto Row250;

        // 570 IFL<>5ORB$<>"BA"THEN600
        Row570:
            if (L != 5 || Bs != "BA")
            {
                goto Row600;
            }

            // 580 IFTGP$="BA"THENL=6:GOTO250
            if (TGPs == "BA")
            {
                L = 6;
                goto Row250;
            }

            // 590 PRINT"DU FÖLL OCH DOG":GOTO1200
            Print("DU FÖLL OCH DOG");
            goto Row1200;

        // 600 IF(L(15)=L)AND(B$="BÅ")THENL=12:GOTO250
        Row600:
            if ((La[15] == L) && (Bs == "BÅ"))
            {
                L = 12;
                goto Row250;
            }

            // 610 IFL<>16ORB$<>"TA"THEN670
            if (L != 16 || Bs != "TA")
            {
                goto Row670;
            }

            // 620 IF(L(10)=L)AND(O$(16)="LÅDA")THENL=15:GOTO250
            if ((La[10] == L) && (Osa[16] == "LÅDA"))
            {
                L = 15;
                goto Row250;
            }

            // 630 PRINT"KAN INTE ÄNNU, DET ÄR FÖR HÖGT":GOTO330
            Print("KAN INTE ÄNNU, DET ÄR FÖR HÖGT");
            goto Row330;

        // 640 IFS<7THENF=0:GOTO500
        Row640:
            if (S < 7)
            {
                F = 0;
                goto Row500;
            }

            // 645 IFC>6THENPRINT"JAG BÄR FÖR MYCKET":GOTO330
            if (C > 6)
            {
                Print("JAG BÄR FÖR MYCKET");
                goto Row330;
            }

            // 650 IFS<>14THEN690
            if (S != 14)
            {
                goto Row690;
            }

            // 660 INPUT"I VAD ";A$:GOSUB360
            As = Input("I VAD "); //TODO: Chech that all parameters are there
            Gosub360();

            // 665 IF(A$="HI")AND(L(11)=0)AND(L(8)=L)THEN680
            if ((As == "HI") && (La[11] == 0) && (La[8] == L))
            {
                goto Row680;
            }

        // 670 PRINT"KAN INTE":GOTO 330
        Row670:
            Print("KAN INTE");
            goto Row330;

        // 680 L(8)=0:C=C+1:GOTO250
        Row680:
            La[8] = 0;
            C++; ;
            goto Row250;

        // 690 IFS<>20THEN720
        Row690:
            if (S != 20)
            {
                goto Row720;
            }

            // 695 IF(L(14)<>L)THEN765
            if ((La[14] != L))
            {
                goto Row765;
            }

            // 700 IFTA=1THENL(14)=0:PRINT"AHA!":P(16,1)=17:GOTO330
            if (TA == 1)
            {
                La[14] = 0;
                Print("AHA!");
                Pa[16, 1] = 17;
                goto Row330;
            }

            // 710 PRINT"DEN ÄR FASTSPIKAD VID TAKSKÄGGET":GOTO330
            Print("DEN ÄR FASTSPIKAD VID TAKSKÄGGET");
            goto Row330;

        // 720 IF S<>19 THEN 730
        Row720:
            if (S != 19)
            {
                goto Row730;
            }

            // 723 IF L(13)=L AND L(1)=0THEN TA=1:PRINT"GOBELÄNGEN FÖLL":GOTO 780
            if (La[13] == L && La[1] == 0)
            {
                TA = 1;
                Print("GOBELÄNGEN FÖLL");
                goto Row780;
            }

            // 725 IF L(1)<>0 THEN PRINT"INGEN SLÄGGA":GOTO 330
            if (La[1] != 0)
            {
                Print("INGEN SLÄGGA");
                goto Row330;
            }

        // 730 IF S=19 AND (L(13)<>L)THEN765
        Row730:
            if (S == 19 && (La[13] != L))
            {
                goto Row765;
            }

            // 740 IF B$=""ORS<7THEN250
            if (Bs.Length == 0 || S < 7)
            {
                goto Row250;
            }

            // 750 IF S>20 THEN 670
            if (S > 20)
            {
                goto Row670;
            }

        // 760 IF (L(S-6)=L)THEN780
        Row760:
            if ((La[S - 6] == L))
            {
                goto Row780;
            }

        // 765 PRINT"JAG SER DEN INTE":GOTO330
        Row765:
            Print("JAG SER DEN INTE");
            goto Row330;

        // 780 C=C+1:L(S-6)=0:GOTO250
        Row780:
            C++; ;
            La[S - 6] = 0;
            goto Row250;

        // 790 IF B$=""ORS<7THEN250
        Row790:
            if (Bs.Length == 0 || S < 7)
            {
                goto Row250;
            }

            // 800 IF S<>26 THEN 840
            if (S != 26)
            {
                goto Row840;
            }

            // 810 IF L<>1 THEN S=23:GOTO760
            if (L != 1)
            {
                S = 23;
                goto Row760;
            }

            // 820 PRINT"VAMPYREN VAKNAR VID MIDNATT"
            Print("VAMPYREN VAKNAR VID MIDNATT");

            // 830 GOTO 330
            goto Row330;

        // 840 IF S<10 THEN 865
        Row840:
            if (S < 10)
            {
                goto Row865;
            }

            // 850 IF L(4)=0THEN860
            if (La[4] == 0)
            {
                goto Row860;
            }

        // 855 PRINT"DEN HAR JAG INTE":GOTO 330
        Row855:
            Print("DEN HAR JAG INTE");
            goto Row330;

        // 860 PRINT"ALLA UTGÅNGAR ÄR INTE SYNLIGA":GOTO330
        Row860:
            Print("ALLA UTGÅNGAR ÄR INTE SYNLIGA");
            goto Row330;

        // 865 IF S<>8 THEN 330
        Row865:
            if (S != 8)
            {
                goto Row330;
            }

            // 867 IF L(2)<>0THEN855
            if (La[2] != 0)
            {
                goto Row855;
            }

            // 869 PRINT T2;":";T1:GOTO330
            Print(T2 + ":" + T1);
            goto Row330;

        // 870 IF S=14ANDL(8)=0ANDL=2THENO$(24)="ASKA":FI=1:L(8)=99:C=C-1:GOTO250
        Row870:
            if (S == 14 && La[8] == 0 && L == 2)
            {
                Osa[24] = "ASKA";
                FI = 1;
                La[8] = 99;
                C--; ;
                goto Row250;
            }

            // 880 IF B$=""ORS<7THENPRINT"VA ??":GOTO330
            if (Bs.Length == 0 || S < 7)
            {
                Print("VA ??");
                goto Row330;
            }

            // 890 IF L(S-6)<>0THEN855
            if (La[S - 6] != 0)
            {
                goto Row855;
            }

            // 900 L(S-6)=L:C=C-1:GOTO250
            La[S - 6] = L;
            C--; ;
            goto Row250;

        // 905 IF (S<>16ORL(10)<>LORL(5)<>0)AND (S<>28ORL(1)<>0ORL<>8)THEN930
        Row905:
            if ((S != 16 || La[10] != L || La[5] != 0) && (S != 28 || La[1] != 0 || L != 8))
            {
                goto Row930;
            }

            // 910 INPUT"MED VAD ";A$:GOSUB 360
            As = Input("MED VAD "); //TODO: Chech that all parameters are there
            Gosub360();

            // 920 IF A$="YX"ANDS=16THEN940
            if (As == "YX" && S == 16)
            {
                goto Row940;
            }

            // 925 IF(A$="SL")ANDS=28THEN935
            if ((As == "SL") && S == 28)
            {
                goto Row935;
            }

        // 930 PRINT" INGENTING HÄNDE":GOTO 330
        Row930:
            Print(" INGENTING HÄNDE");
            goto Row330;

        // 935 O$(28)="EN SÖNDERSLAGEN ELDSTAD":P(8,1)=10:D$(8)=O$(28):GOTO 250
        Row935:
            Osa[28] = "EN SÖNDERSLAGEN ELDSTAD";
            Pa[8, 1] = 10;
            Dsa[8] = Osa[28];
            goto Row250;

        // 940 O$(16)="TRÄPÅLAR":PRINT" DU SLOG SÖNDER LÅDAN TILL NÅGRA TRÄPÅLAR";:GOTO250
        Row940:
            Osa[16] = "TRÄPÅLAR";
            Print(" DU SLOG SÖNDER LÅDAN TILL NÅGRA TRÄPÅLAR", false);
            goto Row250;

        // 950 IF S=23 AND L=18 AND L(7)=0 THEN 980
        Row950:
            if (S == 23 && L == 18 && La[7] == 0)
            {
                goto Row980;
            }

            // 960 IF L=17 AND S=22 AND OI=1ANDL(7)=0THEN990
            if (L == 17 && S == 22 && OI == 1 && La[7] == 0)
            {
                goto Row990;
            }

            // 970 GOTO 930
            goto Row930;

        // 980 O$(23)="VAMPYR I KISTA":GOTO250
        Row980:
            Osa[23] = "VAMPYR I KISTA";
            goto Row250;

        // 990 O$(22)="ÖPPEN DÖRR":P(17,1)=18:GOTO250
        Row990:
            Osa[22] = "ÖPPEN DÖRR";
            Pa[17, 1] = 18;
            goto Row250;

        // 1000 IF L(3)<>0ORS<>9THEN 670
        Row1000:
            if (La[3] != 0 || S != 9)
            {
                goto Row670;
            }

            // 1010 INPUT"I VAD";A$:GOSUB 360
            As = Input("I VAD"); //TODO: Chech that all parameters are there
            Gosub360();

            // 1020 TGP$=A$:GOTO250
            TGPs = As;
            goto Row250;

        // 1030 IF B$="OL"ORB$="FL"THEN PRINT"MENAR DU ATT JAG BÖR OLJA DEN ?":GOTO 250
        Row1030:
            if (Bs == "OL" || Bs == "FL")
            {
                Print("MENAR DU ATT JAG BÖR OLJA DEN ?");
                goto Row250;
            }

            // 1035 IF S<>25ORL<>3THEN670
            if (S != 25 || L != 3)
            {
                goto Row670;
            }

            // 1040 PRINT"AHA!":P(L,6)=9:GOTO 250
            Print("AHA!");
            Pa[L, 6] = 9;
            goto Row250;

        // 1050 IF S<>23ORL<>18OR O$(23)<>"VAMPYR I KISTAN"THEN670
        Row1050:
            if (S != 23 || L != 18 || Osa[23] != "VAMPYR I KISTAN")
            {
                goto Row670;
            }

        // 1060 INPUT"MED VAD ";A$:GOSUB360
        Row1060:
            As = Input("MED VAD "); //TODO: Chech that all parameters are there
            Gosub360();

            // 1070 IF A$="TR"OR A$="PÅ"AND L(10)=0AND O$(16)="TRÄPÅLAR" THEN 1090
            if (As == "TR" || As == "PÅ" && La[10] == 0 && Osa[16] == "TRÄPÅLAR")
            {
                goto Row1090;
            }

            // 1080 PRINT" DU GJORDE FEL ! VAMPYREN VAKNADE OCH DÖDADE DIG":GOTO1200
            Print(" DU GJORDE FEL ! VAMPYREN VAKNADE OCH DÖDADE DIG");
            goto Row1200;

        // 1090 PRINT" GRATULERAR ! - DU HAR DÖDAT VAMPYREN":GOTO1200
        Row1090:
            Print(" GRATULERAR ! - DU HAR DÖDAT VAMPYREN");
            goto Row1200;

        // 1100 IF L(9)<>0ORL<>17OR(S<>22ANDS<>6)THEN 670
        Row1100:
            if (La[9] != 0 || L != 17 || (S != 22 && S != 6))
            {
                goto Row670;
            }

            // 1110 OI=1:O$(22)="ÖPPEN DÖRR":P(17,1)=18:GOTO 250
            OI = 1;
            Osa[22] = "ÖPPEN DÖRR";
            Pa[17, 1] = 18;
            goto Row250;

        // 1120 IF L<>12 OR L(6)<>0 THEN 670
        Row1120:
            if (L != 12 || La[6] != 0)
            {
                goto Row670;
            }

            // 1130 PRINT "DU HAR ROTT MED BÅTEN TILL ANDRA SIDAN":L=16
            Print("DU HAR ROTT MED BÅTEN TILL ANDRA SIDAN");
            L = 16;

            // 1132 FOR X=1 TO 22
            for (X = 1; X <= 22; X++)
            {
                // 1133 IF L(X)=12 THEN L(X)=16
                if (La[X] == 12)
                {
                    La[X] = 16;
                }

                // 1135 NEXT
            }

            // 1140 L(15)=L:GOTO250
            La[15] = L;
            goto Row250;

        // 1150 PRINT"“  VÄDERSTRÄCKEN ÄR:"
        Row1150:
            Print("“  VÄDERSTRÄCKEN ÄR:");

            // 1160 PRINT" NORR,SÖDER,ÖST,VÄST,NER,UPP"
            Print(" NORR,SÖDER,ÖST,VÄST,NER,UPP");

            // 1165 PRINT"  VERBEN ÄR:"
            Print("  VERBEN ÄR:");

            // 1168 PRINT" GÅ,TA,SE,LÄGGA,SLÄPPA,ÖPPNA,BINDA,FLYTTA"
            Print(" GÅ,TA,SE,LÄGGA,SLÄPPA,ÖPPNA,BINDA,FLYTTA");

            // 1170 PRINT" DÖDA,OLJA,RO,SIMMA"
            Print(" DÖDA,OLJA,RO,SIMMA");

            // 1180 PRINT" ":GOTO330
            Print(" ");
            goto Row330;

        // 1200 PRINT"  F1’ SPELA DRAKULAS SLOTT EN GÅNG TILL"
        Row1200:
            Print("  F1’ SPELA DRAKULAS SLOTT EN GÅNG TILL");

            // 1210 PRINT" F3’ LADDA NÄSTA PROGRAM"
            Print(" F3’ LADDA NÄSTA PROGRAM");

            // 1220 PRINT" TRYCK F1’ ELLER F3’ !"
            Print(" TRYCK F1’ ELLER F3’ !");

        // 1230 GETA$:IFA$=""THEN1230
        Row1230:
            As = Get();
            if (As.Length == 0)
            {
                goto Row1230;
            }

            // 1240 IFA$="…"THENRUN
            if (As == "…")
            {
                return 1; // Run game again
            }

            // 1250 IFA$="†"THENPRINT"“  TRYCK PLAY PA‘.  BANDSPELAREN !":LOAD
            if (As == "†")
            {
                Print("“  TRYCK PLAY PA‘.  BANDSPELAREN !");
                return 0; // Play something else
            }

            // 1260 GOTO 1230
            goto Row1230;
        }

        /// <summary>
        /// The Splash.
        /// </summary>
        private static void Splash()
        {
            ResetConsole();
            Console.WriteLine("╭─────────────────────────────────────────────────────────╮");
            Console.WriteLine("│                      Drakulas Slott                     │");
            Console.WriteLine("├─────────────────────────────────────────────────────────┤");
            Console.WriteLine("│ Published : 19xx                                        │");
            Console.WriteLine("│ Legal     : Public Domain                               │");
            Console.WriteLine("│ Language  : Swedish                                     │");
            Console.WriteLine("│ Genre     : Adventure - Text only                       │");
            Console.WriteLine("│ Source    : http://www.gamebase64.com/game.php?id=18629 │");
            Console.WriteLine("│                                                         │");
            Console.WriteLine("├─────────────────────────────────────────────────────────┤");
            Console.WriteLine("│               Press ENTER to start the game             │");
            Console.WriteLine("╰─────────────────────────────────────────────────────────╯");
            Console.WriteLine();
            Console.ReadLine();
            ClearScreen();
        }
    }
}
#pragma warning restore IDE0059 // 'Unnecessary assignment' of a value