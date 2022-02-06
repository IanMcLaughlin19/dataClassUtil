import tkinter as tk
from code_generator_backend import DataclassGenerator
import json
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator


def main_app():

    def handle_button():
        text = enter_text.get("1.0", tk.END)
        result_text.delete("1.0", tk.END)
        if entry_class.get() != "":
            class_name = entry_class.get()
        else:
            class_name = "UnnamedClass"

        data_class = DataclassGenerator(json.loads(text), class_name=class_name, parent_class=True,
                                        add_defaults=checkbox_checked_defaults.get())
        if checkbox_chcked_subclass:
            class_code = data_class.generate_parent_class_str()
        else:
            class_code = data_class.generate_dataclass_str()
        result_text.insert("1.0", class_code)

    root = tk.Tk()
    root.title("Python Class Generator")
    text_entry_frame = tk.Frame(master=root)
    text_entry_frame.grid(row=0, column=1)
    result_text_frame = tk.Frame(master=root)
    result_text_frame.grid(row=0, column=2)

    code_label = tk.Label(master=result_text_frame, text="Python Code")
    code_label.pack()

    btn_convert = tk.Button(master=text_entry_frame, text="Convert data structure to Python", command=handle_button)
    btn_convert.pack()
    entry_label = tk.Label(master=text_entry_frame, text="Enter a valid data structure")
    entry_label.pack()
    enter_text = tk.Text(master=text_entry_frame)
    enter_text.pack()
    result_text = tk.Text(master=result_text_frame)
    result_text.pack()
    Percolator(result_text).insertfilter(ColorDelegator())


    sidebar = tk.Frame(root,bg="white", relief="sunken", borderwidth=2)
    sidebar.grid(row=0, column=0)

    class_label = tk.StringVar()
    class_label.set("Class Name:")
    label_class = tk.Label(master=sidebar, textvariable=class_label)
    label_class.grid(row=0, column=0)
    entry_class = tk.StringVar()
    entry_class_name = tk.Entry(master=sidebar, textvariable=entry_class)
    entry_class_name.grid(row=0, column=1)

    checkbox_val_subclass = tk.StringVar()
    checkbox_val_subclass.set("Enable subclasses?")
    checkbox_subclass_label = tk.Label(master=sidebar, textvariable=checkbox_val_subclass)
    checkbox_subclass_label.grid(row=1, column=0)
    checkbox_chcked_subclass = tk.BooleanVar()
    check_box_1 = tk.Checkbutton(master=sidebar, variable=checkbox_chcked_subclass)
    check_box_1.grid(row=1, column=1)

    checkbox_val_defaults = tk.StringVar()
    checkbox_val_defaults.set("Add default args?")
    checkbox_defaults_label = tk.Label(master=sidebar, textvariable=checkbox_val_defaults)
    checkbox_defaults_label.grid(row=2, column=0)
    checkbox_checked_defaults = tk.BooleanVar()
    check_box_2 = tk.Checkbutton(master=sidebar, variable=checkbox_checked_defaults)
    check_box_2.grid(row=2, column=1)

    root.mainloop()

if __name__ == '__main__':
    main_app()