# README #

Voraussetzungen: 
Die hier geschriebenen Programme dienen dazu einen Tisch mit RGB-LED Matrix zu steuern.
- Die RGB-LEDs sind mit WS2801 Chips in Serie geschaltet und verlaufen im Form einer Schlange.
- Mein Tisch hat 10 Spalten und 20 Zeilen.
- Ich führe das Python-Skript auf einem Raspberry-Pi aus, dieser sendet dann die Befehle via SPI über die GPIO-Pins an die LED-Schlange.
