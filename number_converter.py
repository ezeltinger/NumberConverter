import tkinter as tk

class Numeral:
    """Contains an object with a name, numeral base, and tkinter Label and Entry objects
    """
    def __init__(self, name:str, window:tk.Tk, base:int) -> None:
        self.name = name
        self.base = base
        self.label = tk.Label(master=window, text=self.name)
        self.entry = tk.Entry(master=window)


def handle_conversion():
    entry_count = 0
    for numeral in numerals:
        if numeral.entry.get():
            entry_count = entry_count + 1
            converting_base = numeral.base
            number = int(numeral.entry.get(), converting_base)
    if entry_count > 1:
        message["text"] = "More than one entry filled!"
    else:
        # hex_entry.insert(0, hex(decimal))
        # binary_entry.insert(0, bin(decimal))
        for numeral in numerals:
            if numeral.base != converting_base:
                if numeral.base == 2:
                    numeral.entry.insert(0, f'{number:b}')
                elif numeral.base == 16:
                    numeral.entry.insert(0, f'{number:x}')
                elif numeral.base == 10:
                    numeral.entry.insert(0, f'{number}')
                elif numeral.base == 8:
                    numeral.entry.insert(0, f'{number:o}')

def clear_entries():
    for numeral in numerals:
        numeral.entry.delete(0, 'end')

def handle_keypress(event):
    entry_count = sum(1 for numeral in numerals if numeral.entry.get())
    if entry_count > 1:
        clear_entries()
    elif entry_count == 1:
        handle_conversion()



numeral_tuples = [
    ("Decimal", 10),
    ("Hexadecimal", 16),
    ("Binary", 2),
    ("Octal", 8)
]
numerals = []

window = tk.Tk()
window.title("Number Converter")

window.columnconfigure(list(range(2)), weight=1, minsize=150)
window.rowconfigure(list(range(len(numeral_tuples)+2)), weight=1, minsize=50)

# Create Numeral object for each numeral in numeral_tuples list and put it in numerals list
for name, base in numeral_tuples:
    numerals.append(Numeral(name=name, window=window, base=base))

# Place the label and entry widgets for each Numeral object
for numeral in numerals:
    numeral.label.grid(row=numerals.index(numeral), column=0, padx=5, pady=5)
    numeral.entry.grid(row=numerals.index(numeral), column=1, padx=5, pady=5)

# Create and place a message widget below the numerals
message = tk.Label(master=window)
message.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Add a button for converting numbers
convert_button = tk.Button(
    master=window, 
    text="Convert",
    width=8,
    height=1,
    command=handle_conversion
)
convert_button.grid(row=5, 
                    column=0, 
                    sticky="ew")

# Add a button for clearing the entries
clear_button = tk.Button(
    master=window,
    text="Clear",
    width=8,
    height=1,
    command=clear_entries
)
clear_button.grid(row=5, 
                    column=1, 
                    sticky="ew")

# Use the enter key to convert or clear entries
window.bind("<Return>", handle_keypress)

window.mainloop()
