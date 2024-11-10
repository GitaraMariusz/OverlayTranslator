import tkinter as tk
import keyboard
from googletrans import Translator
from threading import Timer

translator = Translator()

last_input_text = ""
debounce_timer = None

def translate_text():
    global last_input_text
    
    input_text = input_box.get("1.0", "end-1c").strip()
    
    if input_text != last_input_text and input_text:
        target_lang = target_lang_var.get()
        result = translator.translate(input_text, src="en", dest=target_lang)
        
        popup_text.config(state=tk.NORMAL)
        popup_text.delete("1.0", tk.END)
        popup_text.insert("1.0", result.text)
        popup_text.config(state=tk.DISABLED)
        
        popup_window.deiconify()
        popup_window.geometry(f"+{root.winfo_x()}+{root.winfo_y() + root.winfo_height() + 10}")
        
        last_input_text = input_text

    elif not input_text:
        popup_window.withdraw()
        last_input_text = ""

def on_input_change(event=None):
    global debounce_timer
    if debounce_timer:
        debounce_timer.cancel()
    debounce_timer = Timer(0.5, translate_text)
    debounce_timer.start()

def toggle_main_window():
    if root.state() == 'withdrawn':
        root.deiconify()
    else:
        root.withdraw()

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("200x100")
    settings_window.configure(bg="white")
    settings_label = tk.Label(settings_window, text="Settings window", bg="white")
    settings_label.pack(padx=20, pady=20)

root = tk.Tk()
root.title("Input Box")

window_width = 300
window_height = 100
root.configure(bg="white")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = 10
y_position = screen_height - window_height - 200

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.overrideredirect(True)
root.withdraw()  

input_box = tk.Text(root, height=3, wrap="word", bd=0, highlightthickness=0, bg="white")
input_box.pack(padx=10, pady=10)
input_box.bind("<KeyRelease>", on_input_change)  


target_lang_var = tk.StringVar(root)
target_lang_var.set("ja")  
target_lang_menu = tk.OptionMenu(root, target_lang_var, "es", "fr", "de", "ja", "zh")
target_lang_menu.configure(bg="white")

settings_button = tk.Button(root, text="Settings", command=open_settings, bd=0, bg="white", fg="black")

target_lang_menu.pack(side="left", padx=10)
settings_button.pack(side="left", padx=5)

popup_window = tk.Toplevel(root)
popup_window.title("Translation")
popup_window.geometry("300x100")
popup_window.configure(bg="white")
popup_window.overrideredirect(True)
popup_window.withdraw()

popup_text = tk.Text(popup_window, height=3, wrap="word", state=tk.DISABLED, bd=0, highlightthickness=0, bg="white")
popup_text.pack(padx=10, pady=10)

keyboard.add_hotkey("ctrl+alt+t", toggle_main_window)
toggle_main_window()

root.mainloop()
