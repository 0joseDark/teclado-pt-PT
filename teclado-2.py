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

# Variável global para a área de texto
text_area = None

def key_press(key, button):
    global text_area
    # Registra a tecla pressionada na tabela de memória
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    key_history.append({"timestamp": timestamp, "key": key})
    
    # Processa a tecla pressionada
    if key == 'Backspace':
        text_area.delete('end-2c', 'end-1c')
    elif key == 'Enter':
        text_area.insert('end', '\n')
    elif key == 'Space':
        text_area.insert('end', ' ')
    elif key == 'Tab':
        text_area.insert('end', '\t')
    elif len(key) == 1:  # Para caracteres simples
        text_area.insert('end', key)
    
    # Muda a cor do botão temporariamente
    original_color = button.cget("background")
    button.configure(background="yellow")
    button.after(100, lambda: button.configure(background=original_color))
    
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
    global text_area
    # Cria a janela principal
    root = tk.Tk()
    root.title("Teclado Virtual Português Europeu com Nota")

    # Cria a área de texto
    text_area = tk.Text(root, height=10, width=50)
    text_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Cria um frame para conter o teclado
    keyboard_frame = ttk.Frame(root, padding="10")
    keyboard_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

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
            button = tk.Button(keyboard_frame, text=key, width=width)
            button.grid(row=row_index, column=col_index, padx=2, pady=2)

            # Define a função de callback para o botão
            button.config(command=lambda k=key, b=button: key_press(k, b))

    # Botão para salvar o conteúdo da nota
    save_button = tk.Button(root, text="Salvar Nota", command=save_note)
    save_button.grid(row=2, column=0, pady=10)

    # Botão para limpar a nota
    clear_button = tk.Button(root, text="Limpar Nota", command=clear_note)
    clear_button.grid(row=2, column=1, pady=10)

    root.mainloop()

def save_note():
    with open("nota.txt", "w", encoding='utf-8') as file:
        file.write(text_area.get("1.0", "end-1c"))
    print("Nota salva com sucesso!")

def clear_note():
    text_area.delete("1.0", "end")
    print("Nota limpa!")

# Inicia o teclado virtual
if __name__ == "__main__":
    create_keyboard()