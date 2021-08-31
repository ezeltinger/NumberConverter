import tkinter as tk
from tkinter import ttk, Checkbutton, IntVar
from typing import List, Tuple
from functools import partial
import struct

class Numeral:
    """Contains an object with a name, numeral base, and tkinter Label and Entry objects
    """
    def __init__(self, name:str, window:tk.Tk, base:int) -> None:
        self.name = name
        self.base = base
        self.label = tk.Label(master=window, text=self.name)
        self.entry = tk.Entry(master=window)


def convert_integer():
    entry_count = 0
    for numeral in int_numerals:
        if numeral.entry.get():
            entry_count = entry_count + 1
            converting_base = numeral.base
            number = int(numeral.entry.get(), converting_base)
            if little_endian.get() and converting_base == 10:
                number = int(endian_swap(pad_zeros(f'{number:x}', float=False)), 16)
    if entry_count > 1:
        message["text"] = "More than one entry filled!"
    else:
        for numeral in int_numerals:
            if numeral.base != converting_base:
                if numeral.base == 2:
                    numeral.entry.insert(0, f'{number:b}')
                elif numeral.base == 16:
                    numeral.entry.insert(0, f'{number:x}')
                elif numeral.base == 10:
                    if little_endian.get():
                        # swap from little to big endian to properly display the decimal number
                        swapped_decimal = int(endian_swap(pad_zeros(f'{number:x}', float=False)), 16)
                        numeral.entry.insert(0, f'{swapped_decimal}')
                    else:
                        numeral.entry.insert(0, f'{number}')
                elif numeral.base == 8:
                    numeral.entry.insert(0, f'{number:o}')


def convert_float():
    entry_count = 0
    for numeral in float_numerals:
        if numeral.entry.get():
            entry_count = entry_count + 1
            converting_base = numeral.base
            if converting_base == 16:
                hex_string = numeral.entry.get()
                # Need to pad hex with 0s
                hex_string = pad_zeros(hex_string)
                message["text"] = ""
                if len(hex_string)>8:
                    message["text"] = "Only two bytes or less allowed for hex float!"
            elif converting_base == 10:
                number = float(numeral.entry.get())
    if entry_count > 1:
        message["text"] = "More than one entry filled!"
    else:
        for numeral in float_numerals:
            if numeral.base != converting_base:
                if numeral.base == 16:
                    hex_string = hex(struct.unpack('<I', struct.pack('<f', number))[0])[2:]
                    if little_endian.get():
                        hex_string = endian_swap(hex_string)
                    numeral.entry.insert(0, hex_string)
                if numeral.base == 10:
                    if little_endian.get():
                        hex_string = endian_swap(hex_string)
                    number = struct.unpack('!f', bytes.fromhex(hex_string))[0]
                    numeral.entry.insert(0, f'{number}')

def endian_swap(big):
    little_hex = bytearray.fromhex(big)
    little_hex.reverse()
    str_little = ''.join(format(x, '02x') for x in little_hex)
    return str_little

def pad_zeros(hex_string, float=True):
    if float:
        if len(hex_string)<8:
            zeros = 8 - len(hex_string)
            for zero in range(zeros):
                hex_string = "0" + hex_string
    else:
        zeros = len(hex_string)%2
        for zero in range(zeros):
                hex_string = "0" + hex_string
    return hex_string

def clear_entries(numerals):
    for numeral in numerals:
        numeral.entry.delete(0, 'end')

def handle_keypress(event):
    int_entry_count = sum(1 for numeral in int_numerals if numeral.entry.get())
    if int_entry_count > 1:
        clear_entries(int_numerals)
    elif int_entry_count == 1:
        convert_integer()
    float_entry_count = sum(1 for numeral in float_numerals if numeral.entry.get())
    if float_entry_count > 1:
        clear_entries(float_numerals)
    elif float_entry_count == 1:
        convert_float()


def converter_layout(row_number, numeral_tuples) -> Tuple[List[Numeral], int]:
    numerals = []

    # Create Numeral object for each numeral in numeral_tuples list and put it in numerals list
    for name, base in numeral_tuples:
        numerals.append(Numeral(name=name, window=window, base=base))

    # Place the label and entry widgets for each Numeral object
    for numeral in numerals:
        numeral.label.grid(row=row_number, column=0, padx=5, pady=5)
        numeral.entry.grid(row=row_number, column=1, padx=5, pady=5)
        row_number = row_number + 1
    
    return numerals, row_number


int_tuples = [
    ("Decimal", 10),
    ("Hexadecimal", 16),
    ("Binary", 2),
    ("Octal", 8)
]

float_tuples = [
    ("Decimal Float", 10),
    ("Hex Float", 16)
]

total_rows = len(int_tuples) + len(float_tuples) + 5

window = tk.Tk()
window.title("Number Converter")

window.columnconfigure(list(range(2)), weight=1, minsize=100)
window.rowconfigure(list(range(total_rows)), weight=1, minsize=25)

little_endian = IntVar()
int_numerals, current_row = converter_layout(row_number=0, numeral_tuples=int_tuples)

# Add a button for converting numbers
convert_button = tk.Button(
    master=window, 
    text="Convert",
    width=8,
    height=1,
    command=convert_integer
)
convert_button.grid(row=current_row, 
                    column=0,
                    padx=5,
                    sticky="ew")

# Add a button for clearing the entries
clear_button = tk.Button(
    master=window,
    text="Clear",
    width=8,
    height=1,
    command=partial(clear_entries,int_numerals)
)
clear_button.grid(row=current_row, 
                    column=1,
                    padx=5,
                    sticky="ew")
current_row += 1

int_separator = ttk.Separator(window, orient='horizontal')
int_separator.grid(row=current_row, columnspan=2, sticky='ew')

current_row += 1

# ttk.Label(window, text='Float Converter').grid(row=current_row, columnspan=2)
# current_row += 1

float_numerals, current_row = converter_layout(row_number=current_row, numeral_tuples=float_tuples)
all_numerals = int_numerals + float_numerals

# Add a button for converting floats
convert_float_button = tk.Button(
    master=window, 
    text="Convert Float",
    width=8,
    height=1,
    command=convert_float
)
convert_float_button.grid(row=current_row, 
                    column=0,
                    padx=5,
                    sticky="ew")

# Add a button for clearing the float entries
clear_float_button = tk.Button(
    master=window,
    text="Clear",
    width=8,
    height=1,
    command=partial(clear_entries,float_numerals)
)
clear_float_button.grid(row=current_row, 
                    column=1,
                    padx=5,
                    sticky="ew")
current_row += 1

float_separator = ttk.Separator(window, orient='horizontal')
float_separator.grid(row=current_row, columnspan=2, sticky='ew')

current_row += 1

endian_check = Checkbutton(master=window, 
                            text="Little Endian",
                            variable=little_endian, 
                            onvalue=1, 
                            offvalue=0, 
                            height=1, 
                            width=10
                            )
endian_check.grid(row=current_row, 
                    column=0, 
                    columnspan=2, 
                    padx=5, 
                    pady=5)
current_row += 1

# Create and place a message widget below the numerals
message = ttk.Label(master=window)
message.grid(row=current_row, column=0, columnspan=2, padx=5, pady=5)

# Use the enter key to convert or clear entries
window.bind("<Return>", handle_keypress)

window.mainloop()
