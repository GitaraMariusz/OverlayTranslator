import tkinter as tk
import keyboard
from googletrans import Translator

translator = Translator()

last_input_text = ""

def translate_text():
    global last_input_text
    
    input_text = input_box.get("1.0", "end-1c")
    
    if input_text != last_input_text and input_text.strip():
        target_lang = target_lang_var.get()
        result = translator.translate(input_text, src="en", dest=target_lang)
        
        output_box.config(state=tk.NORMAL)
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", result.text)
        output_box.config(state=tk.DISABLED)
        
        last_input_text = input_text

    root.after(500, translate_text)

def show_overlay():
    root.deiconify()

def hide_overlay(event=None):
    root.withdraw()

root = tk.Tk()
window_width = 300
window_height = 200

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = 10
y_position = screen_height - window_height - 40

root.title("Overlay Translator")
root.overrideredirect(True)
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.withdraw()

input_box = tk.Text(root, height=5, wrap="word")
input_box.place(x=10, rely=0.7, anchor="sw")

target_lang_var = tk.StringVar(root)
target_lang_var.set("ja")  
target_lang_menu = tk.OptionMenu(root, target_lang_var, "es", "fr", "de", "ja", "zh")
target_lang_menu.place(x=10, y=10)

output_box = tk.Text(root, height=5, wrap="word", state=tk.DISABLED)
output_box.place(x=10, rely=1.0, anchor="sw")

root.bind("<Escape>", hide_overlay)
keyboard.add_hotkey("ctrl+t", show_overlay)

show_overlay()

translate_text()

root.mainloop()
