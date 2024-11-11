import tkinter as tk
import keyboard
from googletrans import Translator
from threading import Timer

translator = Translator()

last_input_text = ""
debounce_timer = None
shortcut = "ctrl+alt+t"
source_lang = "en"  

languages = ["en", "ja", "es", "fr", "de", "zh"]

settings_window = None

def translate_text():
    global last_input_text
    
    input_text = input_box.get("1.0", "end-1c").strip()
    
    if input_text != last_input_text and input_text:
        target_lang = target_lang_var.get()
        result = translator.translate(input_text, src=source_lang, dest=target_lang)
        
        popup_text.config(state=tk.NORMAL)
        popup_text.delete("1.0", tk.END)
        popup_text.insert("1.0", result.text)
        popup_text.config(state=tk.DISABLED)
        
        popup_window.deiconify()
        popup_window.geometry(f"+{root.winfo_x()}+{root.winfo_y() + int(0.12 * screen_height)}")
        
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

def update_shortcut(new_shortcut):
    global shortcut
    keyboard.remove_hotkey(shortcut) 
    shortcut = new_shortcut
    keyboard.add_hotkey(shortcut, toggle_main_window)  

def update_target_lang_options():
    target_lang_menu['menu'].delete(0, 'end')
    
    for lang in languages:
        if lang != source_lang:
            target_lang_menu['menu'].add_command(label=lang, command=lambda l=lang: target_lang_var.set(l))

    if target_lang_var.get() == source_lang:
        target_lang_var.set(languages[0] if languages[0] != source_lang else languages[1])

def toggle_settings():
    global settings_window, source_lang

    if settings_window and tk.Toplevel.winfo_exists(settings_window):
        settings_window.destroy()
        settings_window = None
    else:
        settings_window = tk.Toplevel(root)
        settings_window.title("Settings")
        settings_window.overrideredirect(True)

        settings_window_width = popup_window_width
        settings_window_height = int(0.15 * screen_height)
        settings_x_position = root.winfo_x()
        settings_y_position = screen_height - settings_window_height - int(0.32 * screen_height)
        settings_window.geometry(f"{settings_window_width}x{settings_window_height}+{settings_x_position}+{settings_y_position}")
        
        settings_window.configure(bg="white")
        
        shortcut_frame = tk.Frame(settings_window, bg="white")
        shortcut_frame.pack(pady=10, padx=10, anchor="w")
        
        settings_label = tk.Label(shortcut_frame, text="Open Shortcut:", bg="white")
        settings_label.pack(side="left", padx=(0, 10))  

        shortcut_entry = tk.Entry(shortcut_frame)
        shortcut_entry.insert(0, shortcut)  
        shortcut_entry.pack(side="left")

        def save_shortcut():
            new_shortcut = shortcut_entry.get().strip()
            if new_shortcut:
                update_shortcut(new_shortcut)
            settings_window.destroy()

        language_frame = tk.Frame(settings_window, bg="white")
        language_frame.pack(pady=10, padx=10, anchor="w")

        lang_label = tk.Label(language_frame, text="Source Language:", bg="white")
        lang_label.pack(side="left", padx=(0, 10))

        source_lang_var = tk.StringVar(settings_window)
        source_lang_var.set(source_lang)  
        source_lang_menu = tk.OptionMenu(language_frame, source_lang_var, *languages)
        source_lang_menu.configure(bg="white")
        source_lang_menu.pack(side="left")

        def save_settings():
            global source_lang
            source_lang = source_lang_var.get() 
            update_target_lang_options() 
            save_shortcut()

        save_button = tk.Button(settings_window, text="Save", command=save_settings)
        save_button.pack(pady=20, anchor="center", side="bottom")

root = tk.Tk()
root.title("Input Box")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(0.2 * screen_width)  
window_height = int(0.1 * screen_height)
x_position = int(0.02 * screen_width)
y_position = screen_height - window_height - int(0.2 * screen_height)

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.configure(bg="white")
root.overrideredirect(True)
root.withdraw()  

input_box = tk.Text(root, height=3, wrap="word", bd=0, highlightthickness=0, bg="white")
input_box.pack(padx=10, pady=10)
input_box.bind("<KeyRelease>", on_input_change)  

target_lang_var = tk.StringVar(root)
target_lang_var.set("ja")  
target_lang_menu = tk.OptionMenu(root, target_lang_var, *[lang for lang in languages if lang != source_lang])
target_lang_menu.configure(bg="white")

settings_button = tk.Button(root, text="Settings", command=toggle_settings, bd=0, bg="white", fg="black")

target_lang_menu.pack(side="left", padx=10)
settings_button.pack(side="left", padx=5)

popup_window = tk.Toplevel(root)
popup_window.title("Translation")

popup_window_width = window_width  
popup_window_height = int(0.1 * screen_height)
popup_window.geometry(f"{popup_window_width}x{popup_window_height}")
popup_window.configure(bg="white")
popup_window.overrideredirect(True)
popup_window.withdraw()

popup_text = tk.Text(popup_window, height=3, wrap="word", state=tk.DISABLED, bd=0, highlightthickness=0, bg="white")
popup_text.pack(padx=10, pady=10)

keyboard.add_hotkey(shortcut, toggle_main_window)
toggle_main_window()

root.mainloop()
