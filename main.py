import customtkinter as ctk

WINDOW_WIDTH = 360
WINDOW_HEIGHT = 400
BUTTON_WIDTH = 5
LABEL_FONT_SIZE = 40

root = ctk.CTk()
root.title("Calculator")

# Set the window's position in the middle of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (WINDOW_WIDTH / 2))
y = int((screen_height / 2) - (WINDOW_HEIGHT / 2))
root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")


def resize_label_font_size(event=None) -> None:
    length = len(math_label.cget("text"))
    if length == 0:
        return
    width = root.winfo_width()
    height = root.winfo_height()
    new_label_size = min(int(width / length * 1.5), int(height))
    if new_label_size < 12:  # fold text to new line if text size is too small
        math_label.configure(wraplength=width)
    elif new_label_size < LABEL_FONT_SIZE:  # only set new size if its smaller than the original size
        math_label.configure(font=("Arial", new_label_size, "bold"))


def button_command(character: str) -> None:
    # First unpack error label if its packed
    error_label.place_forget()
    if character == "C":
        math_label.configure(text="")
    elif character == "=":
        execute_math_in_label()
    else:
        math_label.configure(text=math_label.cget("text") + character)
        # Scale label text size to window size
        resize_label_font_size()


def handle_keyboard_press(event=None) -> None:
    char = event.char
    if char in ("\r", "="):  # Enter or equals sign
        execute_math_in_label()
        return
    if char == "\x08":  # Backspace
        math_label.configure(text=math_label.cget("text")[:-1])
        return
    if char in ["c", "C"]:  # Clear
        math_label.configure(text="")
        return
    if "¨" in char:
        char.replace("¨", "")
    # Handle "^", its tricky since it only sends if you type another character after
    elif "^" in char:
        if char[-1] != " " and (any(char[-1] in string for string in button_characters)):
            button_command(char)
    # The rest
    elif char != " " and (any(char in string for string in button_characters)):
        button_command(char)


def execute_math_in_label(event=None) -> None:
    input = math_label.cget("text")
    if "^" in input:
        input = input.replace("^", "**")
    try:
        output = str(eval(input))
    except SyntaxError:
        output = None
        error_msg = "Syntax error"
    except ZeroDivisionError:
        output = None
        error_msg = "Can't divide by zero"
    if output is None:  # place error text in the top of the math label box
        error_label.configure(text=error_msg)
        error_label.place(in_=math_label, anchor="n", relx=0.5, y=2)
    else:
        if output.split(".")[-1] == 0:
            output = int(output)
        elif len(output.split(".")[-1]) > 5:  # round to 5 decimals
            output = f"{float(output):.5f}"
        math_label.configure(text=output)


# Styling
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Labels
math_label = ctk.CTkLabel(root, text="", font=("Arial", LABEL_FONT_SIZE, "bold"), anchor="center")
math_label.pack(fill="both", expand=True, pady=10, padx=10)
error_label = ctk.CTkLabel(root, text="", text_color="red", anchor="center")

# Frame containing all the buttons
button_frame = ctk.CTkFrame(root)
button_frame.pack(fill="both", expand=True)
button_frame.columnconfigure(tuple(range(4)), weight=1)
button_frame.rowconfigure(tuple(range(5)), weight=1)

# Make buttons for each row and column. Each string in the list is a row in descending order.
button_characters = ["^ ( ) /", "7 8 9 *", "4 5 6 -", "1 2 3 +", "0 . C ="]
for i, string in enumerate(button_characters):
    for j, char in enumerate(string.split(" ")):
        button = ctk.CTkButton(button_frame, text=char, corner_radius=0, font=("Arial", 20),
                               command=lambda btn_char=char: button_command(btn_char))
        button.grid(column=j, row=i, sticky="news")

# Bind window resizing
root.bind("<Configure>", resize_label_font_size)

# Bind keyboard press
root.bind("<Key>", handle_keyboard_press)


def dark_mode_switch_event():
    match switch_var.get():
        case "dark":
            ctk.set_appearance_mode("dark")
        case "light":
            ctk.set_appearance_mode("light")


switch_var = ctk.StringVar(value="dark")
switch = ctk.CTkSwitch(root, text="Dark", command=dark_mode_switch_event,
                       variable=switch_var, onvalue="dark", offvalue="light")
switch.place(in_=math_label, relx=0, rely=0)

##### TODO:
# - historikk
# - sette ANS når man begynner å skrive igjen (kanskje fjerne avrunding da?)

if __name__ == "__main__":
    root.mainloop()
