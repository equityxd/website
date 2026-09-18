@echo off
rem Regenerates "1 WIP\SONG Ernest - CV v1.pdf" on every save of the .typ source.
rem Keep this terminal open while editing. Ctrl+C to stop.
cd /d "%~dp0"
typst watch "1 WIP\SONG Ernest - CV v1.typ"
