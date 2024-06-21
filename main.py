import queue
import tkinter as tk
import threading
import time
from decoder import scan

morse_queue = queue.Queue()
command_queue = []

def run_decoder():
    scan_thread.start()

def toggle_decoder():
    command_queue.append('TOGGLE')


scan_thread = threading.Thread(target=scan, args=(morse_queue,command_queue))
scan_thread.daemon = True


def worker(morse_queue, text_widget):
    while True:
        item = morse_queue.get()

        if item:
            text_widget.insert(tk.END, item)
            text_widget.see(tk.END)
        morse_queue.task_done()


def clear_text(text_widget):
    text_widget.delete('1.0', tk.END)  # Borra todo el contenido del Text widget


def show():
    # Crear una ventana de Tkinter
    root = tk.Tk()
    root.title("No tengo wifi")
    root.geometry('800x600')  # Define el tamaño de la ventana (ancho x alto)
    # Crear un Text widget
    font_settings = ('Terminus', 36)
    text_widget = tk.Text(root, wrap='word', font=font_settings, bg='black', fg='green')
    text_widget.pack(expand=True, fill='both')
    # Crear un botón para limpiar el Text widget
    clear_button = tk.Button(root, text="Clear", command=lambda: clear_text(text_widget))
    clear_button.place(relx=1.0, rely=0.0, anchor='ne')  # Posicionar el botón en la esquina superior derecha
    run_read_button = tk.Button(root, text="Run", command=lambda: run_decoder())
    run_read_button.place(relx=1.0, rely=0.2, anchor='ne')  # Posicionar el botón en la esquina superior derecha
    run_read_button = tk.Button(root, text="=Toggle Read", command=lambda: toggle_decoder())
    run_read_button.place(relx=1.0, rely=0.3, anchor='ne')  # Posicionar el botón en la esquina superior derecha


    # Leer datos del queue y mostrarlos en el Text widget
    reader_thread = threading.Thread(target=worker, args=(morse_queue, text_widget))
    reader_thread.daemon = True
    reader_thread.start()

    # Iniciar el loop principal de Tkinter
    root.mainloop()
   
show()

morse_queue.join()
