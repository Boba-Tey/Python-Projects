from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
import os, shutil, re

# Renaming Logic -------------------------------------------------------------------
def rename_logic(text_file, source, raw_destination):
    while True:
        try:
            image_dic = {}
            last_filename = None
            with open(text_file, encoding="utf-8") as file:
                for line in file:
                    stripped = line.strip()

                    match = re.search(r"(IMG-\d{8}-WA\d{4}\.jpg)", stripped)
                    if match:
                        last_filename = match.group(1)

                    elif stripped.isdigit() and last_filename:
                        image_dic[stripped] = last_filename
                        last_filename = None  

            last_part = os.path.basename(source)
            destination = os.path.join(raw_destination, last_part)

            if not image_dic:
                messagebox.showerror("Task Error", "Wrong text file, images could not be renamed")
                break

            if not os.path.exists(destination):
                shutil.copytree(source, destination)
            else:
                messagebox.showerror("Task Error", "Folder is already copied to the destination.")
                break

            for caption, image_name in image_dic.items():
                old_path = os.path.join(destination, image_name)
                new_path = os.path.join(destination, f"{caption}.jpg")

                if os.path.exists(new_path):
                    continue

                elif os.path.exists(old_path):
                    os.rename(old_path, new_path)

            messagebox.showinfo("Task Complete", "Renaming finished!")
            break

        except Exception as e:
            messagebox.showerror("Task Error", e)
            break

    submit_button.config(text = "Submit")
    submit_button["state"] = NORMAL

# GUI -------------------------------------------------------------------------------
window = Tk()
window.geometry("500x300")
window.title("Bulk Image Rename")

main_frame = Frame(window)
main_frame.pack(expand = True)

main_title = Label(main_frame, text = "Bulk Image Renaming With WhatsApp Logs!", font = (25))
main_title.pack(pady = 20)

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

    entry_name = Entry(frame_name, width = 30, font = (15))
    entry_name.pack(side = LEFT, padx = 20)

    button_name = Button(frame_name, width = 15, text = your_text, command = your_command)
    button_name.pack(side = LEFT)

    return frame_name, entry_name, button_name, your_text, your_command

log_form = form_template("log_frame", "log_entry", "log_button", "WhatsApp Log File",
    lambda: open_explorer("file", log_form))

image_form = form_template("image_frame", "image_entry", "image_button", "Image Folder", 
    lambda: open_explorer("folder", image_form))

output_form = form_template("output_frame", "output_entry", "output_button", "Output Folder", 
    lambda: open_explorer("folder", output_form))

def submitting():
    log_path = log_form[1].get()
    image_path = image_form[1].get()
    output_path = output_form[1].get()

    if any(not i for i in [log_path, image_path, output_path]):
        messagebox.showerror("Missing Input", "Please fill in all the paths.")
    else:
        submit_button.config(text = "Processing...")
        submit_button["state"] = DISABLED
        Thread(target=rename_logic, args=(log_path, image_path, output_path)).start()

submit_button = Button(main_frame, width = 15, text = "Submit", command = submitting)
submit_button.pack(pady = 15)

window.mainloop()