from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
import os, shutil, re

# Renaming Logic -------------------------------------------------------------------
def rename_logic(text_file, source, raw_destination, custom_regex):
    try:
        lines = [line.strip() for line in open(text_file, encoding="utf-8") if line.strip()]
        image_dic = {}

        for i in range(len(lines)):
            line = lines[i]
            
            if custom_regex:
                pattern = re.compile(rf"{custom_regex}.*\.(?:jpg|jpeg|png|gif|bmp|webp)")
            else:
                pattern = re.compile(r"IMG.*\.(?:jpg|jpeg|png|gif|bmp|webp)")
            
            match = pattern.search(line)
            if match:
                orignal_filename = match.group(0)
                
                if i + 1 < len(lines):
                    caption_line = lines[i + 1]
                    
                    if not pattern.search(caption_line):
                        image_dic[orignal_filename] = caption_line
                    else:
                        continue

        if not image_dic:
            messagebox.showerror("Task Error", "No valid image names found in text file or folder.")
            return
        
        last_part = os.path.basename(source)
        destination = os.path.join(raw_destination, last_part)

        if not os.path.exists(source):
            messagebox.showerror("Task Error", "The source folder does not exist.")
            return
        
        if not os.path.exists(raw_destination):
            messagebox.showerror("Task Error", "The destination folder does not exist.")
            return

        if not os.path.exists(destination):
            shutil.copytree(source, destination)
        else:
            messagebox.showerror("Task Error", "Folder already exists in destination.")
            return

        for image_name, caption in image_dic.items():
            old_file = os.path.join(destination, image_name)
            extension = os.path.splitext(image_name)[1]
            new_file_name_base = f"{caption}{extension}"
            new_file = os.path.join(destination, new_file_name_base)
            
            if os.path.exists(new_file):
                continue

            if os.path.exists(old_file):
                os.rename(old_file, new_file)
        
        messagebox.showinfo("Task Complete", "Renaming finished!")

    except Exception as e:
        messagebox.showerror("Task Error", str(e))
    finally:
        submit_button.config(text = "Submit", state = NORMAL)

# GUI -------------------------------------------------------------------------------
window = Tk()
window.geometry("500x300")
window.title("Bulk Image Rename")

main_frame = Frame(window)
main_frame.pack(expand = True)

main_title = Label(main_frame, text = "Bulk Image Renaming With WhatsApp OR Text Logs!", font = ("Arial", 12))
main_title.pack(pady = 20)

optional_frame = Frame(main_frame)
optional_frame.pack()

def toggle_regex():
    if regex_var.get() == 1:
        regex_entry.config(state = NORMAL)
        regex_entry.delete(0, END)
    else:
        regex_entry.delete(0, END)
        regex_entry.insert(0, "Using Default Regex (IMG)")
        regex_entry.config(state = DISABLED)

regex_var = IntVar()

regex_entry = Entry(optional_frame, width = 30, font = ("Arial", 12))
regex_entry.pack(side = LEFT, padx = 20)
toggle_regex()

regex_checkbox = Checkbutton(optional_frame, text = "Custom Regex", font = ("Arial", 12), 
    variable = regex_var, command = toggle_regex)
regex_checkbox.pack(side = LEFT)

def open_explorer(type, form):
    path_text = form[1]

    if type == "file":
        file_name = filedialog.askopenfilename(
            title = "Open a file",
            initialdir = "/",
            filetypes = [("text files", "*.txt")]
            )
        path_text.delete(0, END)
        path_text.insert(END, file_name)

    elif type == "folder":
        folder_name = filedialog.askdirectory()
        path_text.delete(0, END)
        path_text.insert(END, folder_name)

def form_template(frame_name, entry_name, button_name, your_text, your_command):
    frame_name = Frame(main_frame)
    frame_name.pack(pady = 5)

    entry_name = Entry(frame_name, width = 30, font = ("Arial", 12))
    entry_name.pack(side = LEFT, padx = 20)

    button_name = Button(frame_name, width = 15, text = your_text, font = ("Arial", 10), command = your_command)
    button_name.pack(side = LEFT)

    return frame_name, entry_name, button_name, your_text, your_command

log_form = form_template("log_frame", "log_entry", "log_button", "Log File",
    lambda: open_explorer("file", log_form))

image_form = form_template("image_frame", "image_entry", "image_button", "Image Folder", 
    lambda: open_explorer("folder", image_form))

output_form = form_template("output_frame", "output_entry", "output_button", "Output Folder", 
    lambda: open_explorer("folder", output_form))

def submitting():
    form_values = {
        "log_path": log_form[1].get(),
        "image_path": image_form[1].get(),
        "output_path": output_form[1].get()
    }

    if regex_var.get() == 1:
        form_values["custom_regex"] = regex_entry.get()
    else:
        form_values["custom_regex"] = None 

    required = ["log_path", "image_path", "output_path"]
    if any(not form_values[field] for field in required):
        messagebox.showerror("Missing Input", "Please fill in all the paths.")
        return
    
    if regex_var.get() == 1 and not form_values["custom_regex"]:
        messagebox.showerror("Missing Input", "Custom regex not provided!")
        return

    submit_button.config(text = "Processing...", state = DISABLED)
    Thread(target = rename_logic, 
        args = (form_values["log_path"], form_values["image_path"], form_values["output_path"], form_values["custom_regex"])).start()

info_frame = Frame(main_frame)
info_frame.pack(pady = 15)

description = """Use Custom Regex (Regular Expression) to specify a common pattern that appears at the beginning of your original image filenames.
\nExample: 'IMG' is the common pattern in filenames like 'IMG-01.jpg' and 'IMG-02.jpg'.
\nSimilarly, 'image' is the common pattern in filenames like 'image summer.png' and 'image beach.png'.
\nThis feature helps the script scan for the original image names and correctly map them to the new names you want from the text file."""

help_button = Button(info_frame, width = 10, text = "Help", font = ("Arial", 10), 
    command = lambda: messagebox.showinfo("Tutorial", description))
help_button.pack(side = LEFT, padx = 10)

submit_button = Button(info_frame, width = 10, text = "Submit", font = ("Arial", 10), command = submitting)
submit_button.pack(side = LEFT)

window.mainloop()
