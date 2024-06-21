import os
import tkinter as tk
import threading
import time

def read_fifo(fifo_path, text_widget):
    with open(fifo_path, 'r') as fifo:
        while True:
            line = fifo.read()
            if line:
                text_widget.insert(tk.END, line)
                text_widget.see(tk.END)
            else:
                time.sleep(0.1)  # Evita un loop ocupado

def main():
    fifo_path = 'myfifo'  # Asegúrate de que este path sea correcto y que el FIFO exista

    # Crear una ventana de Tkinter
    root = tk.Tk()
    root.title("FIFO Reader")

    # Crear un Text widget
    text_widget = tk.Text(root, wrap='word')
    text_widget.pack(expand=True, fill='both')

    # Leer datos del FIFO y mostrarlos en el Text widget
    reader_thread = threading.Thread(target=read_fifo, args=(fifo_path, text_widget))
    reader_thread.daemon = True
    reader_thread.start()

    # Iniciar el loop principal de Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()

