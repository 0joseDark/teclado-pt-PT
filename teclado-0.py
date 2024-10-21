import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv
import pyautogui
import keyboard

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

def key_press(key, button):
    # Registra a tecla pressionada na tabela de memória
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    key_history.append({"timestamp": timestamp, "key": key})
    
    # Simula a pressão da tecla no aplicativo ativo
    pyautogui.press(key)
    
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
    # Cria a janela principal
    root = tk.Tk()
    root.title("Teclado Virtual Português Europeu")
    root.attributes('-topmost', True)  # Mantém a janela sempre no topo

    # Cria um frame para conter o teclado
    keyboard_frame = ttk.Frame(root, padding="10")
    keyboard_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Dicionário para mapear teclas especiais
    special_keys = {
        'Backspace': 'backspace', 'Tab': 'tab', 'Caps Lock': 'capslock',
        'Enter': 'enter', 'Shift': 'shift', 'Ctrl': 'ctrl', 'Win': 'win',
        'Alt': 'alt', 'Space': 'space', 'AltGr': 'altgr',
        'Menu': 'menu', '←': 'left', '↑': 'up', '↓': 'down', '→': 'right',
        'Insert': 'insert', 'Delete': 'delete', 'Home': 'home', 'End': 'end',
        'Page Up': 'pageup', 'Page Down': 'pagedown'
    }

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
            key_to_send = special_keys.get(key, key.lower())
            button.config(command=lambda k=key_to_send, b=button: key_press(k, b))

    root.mainloop()

# Função para lidar com teclas físicas pressionadas
def on_key_press(event):
    key = event.name
    # Encontra o botão correspondente à tecla pressionada
    for child in keyboard_frame.winfo_children():
        if isinstance(child, tk.Button) and child.cget('text').lower() == key.lower():
            key_press(key, child)
            break

# Inicia o teclado virtual
if __name__ == "__main__":
    # Configura o listener para teclas físicas
    keyboard.on_press(on_key_press)
    create_keyboard()