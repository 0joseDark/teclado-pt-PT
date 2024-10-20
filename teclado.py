import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv

# Definição das teclas do teclado português europeu, incluindo teclas de navegação
keys = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "'", '«', 'Backspace'],
    ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '+', '´', 'Insert', 'Home', 'Page Up'],
    ['Caps Lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ç', 'º', '~', 'Enter', 'Delete', 'End', 'Page Down'],
    ['Shift', '<', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', 'Shift'],
    ['Ctrl', 'Win', 'Alt', 'Space', 'AltGr', 'Win', 'Menu', 'Ctrl', '←', '↑', '↓', '→']
]

# Tabela na memória para armazenar o histórico de teclas pressionadas
key_history = []

def key_press(key):
    # Registra a tecla pressionada na tabela de memória
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    key_history.append({"timestamp": timestamp, "key": key})
    
    # Imprime a tecla pressionada (para debug)
    print(f"Tecla pressionada: {key}")
    
    # Salva o histórico no arquivo de log
    save_log()

def save_log():
    # Salva o histórico de teclas em um arquivo CSV
    with open("keyboard_log.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "key"])
        writer.writeheader()
        for entry in key_history:
            writer.writerow(entry)

def create_keyboard():
    # Cria a janela principal
    root = tk.Tk()
    root.title("Teclado Virtual Português Europeu")

    # Cria um frame para conter o teclado
    keyboard_frame = ttk.Frame(root, padding="10")
    keyboard_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Cria os botões para cada tecla
    for row_index, row in enumerate(keys):
        for col_index, key in enumerate(row):
            # Determina o tamanho do botão
            width = 2
            if key in ['Backspace', 'Tab', 'Caps Lock', 'Enter', 'Shift', 'Ctrl', 'Alt', 'AltGr']:
                width = 5
            elif key == 'Space':
                width = 20
            elif key in ['Insert', 'Home', 'Page Up', 'Delete', 'End', 'Page Down']:
                width = 4
            elif key in ['←', '↑', '↓', '→']:
                width = 3

            # Cria o botão
            ttk.Button(keyboard_frame, text=key, width=width, 
                       command=lambda k=key: key_press(k)).grid(row=row_index, column=col_index, padx=2, pady=2)

    root.mainloop()

# Inicia o teclado virtual
if __name__ == "__main__":
    create_keyboard()