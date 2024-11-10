import tkinter as tk
import keyboard
from googletrans import Translator

def translate_text():
    input_text = input_box.get("1.0", "end-1c")
    target_lang = target_lang_var.get()
    
    translator = Translator()
    result = translator.translate(input_text, src="en", dest=target_lang)
    
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert("1.0", result.text)
    output_box.config(state=tk.DISABLED)

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
target_lang_var.set("es")
target_lang_menu = tk.OptionMenu(root, target_lang_var, "es", "fr", "de", "ja", "zh")
target_lang_menu.pack()

translate_button = tk.Button(root, text="Translate", command=translate_text)
translate_button.pack(pady=5)

output_box = tk.Text(root, height=5, wrap="word", state=tk.DISABLED)
output_box.pack(pady=5)

root.bind("<Escape>", hide_overlay)
keyboard.add_hotkey("ctrl+alt+t", show_overlay)

root.mainloop()
