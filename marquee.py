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

def clear_text(text_widget):
    text_widget.delete('1.0', tk.END)  # Borra todo el contenido del Text widget


def main():
    fifo_path = 'myfifo'  # Asegúrate de que este path sea correcto y que el FIFO exista

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

    # Leer datos del FIFO y mostrarlos en el Text widget
    reader_thread = threading.Thread(target=read_fifo, args=(fifo_path, text_widget))
    reader_thread.daemon = True
    reader_thread.start()

    # Iniciar el loop principal de Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()

