# NumberConverter

Converts numbers between decimal, hex, binary, and octal.

## Building Executable

1. In the scripts directory run `create_venv.bat` to build the python venv.
2. Then run the command `pyinstaller number_converter.py --onefile --noconsole`
3. Use the executable in dist/ to start the Number Converter program.

## User Guide

The executable can be found at <https://github.com/ezeltinger/NumberConverter/releases> or in the dist/ folder of the repo after pyinstaller is run.

Once you have Number Converter open, you can add a number to any of the entries and then click 'Convert' or hit enter to convert to other numeral systems.

To clear all entries, click 'Clear' or hit enter when two or more entries are filled.

Little-Endian is now supported for both float and int conversions.
