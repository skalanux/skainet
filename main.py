import queue
import tkinter as tk
import threading
import time
from decoder import scan

morse_queue = queue.Queue()
command_queue = []


def toggle_decoder():
    if scan_thread.is_alive():
        command_queue.append('TOGGLE')
    else:
        scan_thread.start()


scan_thread = threading.Thread(target=scan, args=(morse_queue,command_queue))
scan_thread.daemon = True


def worker(morse_queue, text_widget):
    while True:
        item = morse_queue.get()

        if item:
            text_widget.insert(tk.END, item)
            #text_widget.see(tk.END)
        morse_queue.task_done()


def clear_text(text_widget):
    text_widget.delete('1.0', tk.END)  # Borra todo el contenido del Text widget
    text_widget.insert(tk.END, ' > ')


def show():
    root = tk.Tk()
    root.title("No tengo wifi")
    root.geometry('800x600')

    font_settings = ('Terminus', 36)
    text_widget = tk.Text(root, wrap='word', font=font_settings, bg='black', fg='green')
    text_widget.pack(expand=True, fill='both')
    text_widget.insert(tk.END, ' > ')
    run_read_button = tk.Button(root, text="Start/Stop", command=lambda: toggle_decoder())
    run_read_button.place(relx=0.4, rely=0.8, anchor='ne')  # Posicionar el botón en la esquina superior derecha

    clear_button = tk.Button(root, text="Clear", command=lambda: clear_text(text_widget))
    clear_button.place(relx=0.7, rely=0.8, anchor='ne')  # Posicionar el botón en la esquina superior derecha

    reader_thread = threading.Thread(target=worker, args=(morse_queue, text_widget))
    reader_thread.daemon = True
    reader_thread.start()

    root.mainloop()
   
show()

morse_queue.join()
