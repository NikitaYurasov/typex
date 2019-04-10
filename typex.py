from tkinter import *
import numpy as np


root = Tk()
root.title('TYPEX')


E_D_Label = Label(root, text='Select Mode:', bg='white', fg='red', width=100)
E_D_Label.pack()

E_But = Button(root, text='Encrypt')
D_But = Button(root, text='Decrypt')
Norm_But = Button(root, text='Back')

mode = ''


def E_Button(event):
    global mode
    mode = 'E'
    E_But.config(state=ACTIVE, fg='green')
    D_But.config(state=DISABLED)


def D_Button(event):
    global mode
    mode = 'D'
    D_But.config(state=ACTIVE, fg='green')
    E_But.config(state=DISABLED)


def But_Back(event):
    E_But.config(state=ACTIVE)
    D_But.config(state=ACTIVE)


E_But.bind('<Button-1>', E_Button)
D_But.bind('<Button-1>', D_Button)
Norm_But.bind('<Button-1>', But_Back)

E_But.pack(padx=5, pady=5)
D_But.pack(padx=5, pady=5)
Norm_But.pack()

E_D_Text_I_Label = Label(root, text='Write the message:', bg='white', fg='red', width=100)
E_D_Text_I_Label.pack()
E_D_Text_Input = Entry(root, width=100, show='*')
E_D_Text_Input.pack()


b = Button(root, text="Crypt")
E_D_Text_O_Label = Label(root, text='Final message:', bg='white', fg='red', width=100)
E_D_Text_Output = Label(root, bg='black', fg='white', width=100)


def Crypt(event):
    # Роторы
    rotors = (
        (10, 24, 14, 12, 23, 2, 7, 15, 24, 2, 7, 5, 22, 6, 2, 1, 22, 12, 6, 9, 7, 2, 11, 23, 14, 2),
        (1, 7, 11, 26, 12, 5, 11, 20, 11, 7, 18, 6, 17, 18, 19, 1, 13, 5, 2, 9, 11, 13, 6, 17, 26, 24),
        (9, 1, 21, 6, 4, 19, 25, 6, 17, 10, 26, 1, 23, 6, 1, 17, 19, 17, 25, 21, 3, 21, 17, 1, 18, 20)
    )

    # Коммутатор
    switch = {
        'H': 'Z', 'S': 'N', 'L': 'M',
        'P': 'Q', 'R': 'W', 'X': 'Y'
    }
    # Первая стадия - роторное шифрование
    def stageOne(mode, message):
        X, Y, Z = 2, 0, 1  # Позиция роторов
        x, y, z = 7, 1, 8  # Ключевая настройка
        finalMessage = ""
        for symbol in message:
            rotor = rotors[X][x] + rotors[Y][y] + rotors[Z][z]
            if mode == 'E':
                if symbol in [chr(x) for x in range(65, 91)]:
                    finalMessage += chr((ord(symbol) - 13 + rotor) % 26 + ord('A'))
                else:
                    continue
            else:
                finalMessage += chr((ord(symbol) - 13 - rotor) % 26 + ord('A'))
            if x != 25:
                x += 1
            else:
                x = 0
                if y != 25:
                    y += 1
                else:
                    y = 0
                    if z != 25:
                        z += 1
                    else:
                        z = 0
        return finalMessage

    # Вторая стадия - шифр пар
    def stageTwo(message):
        finalMessage = list(message)
        for symbol in range(len(finalMessage)):
            for key in switch:
                if finalMessage[symbol] == key:
                    finalMessage[symbol] = switch[key]
                elif finalMessage[symbol] == switch[key]:
                    finalMessage[symbol] = key
                else:
                    pass
        return "".join(finalMessage)

    # Переключение режимов шифрования/расшифрования
    def encryptDecrypt(mode):
        message = E_D_Text_Input.get().upper()
        if mode == 'E':
            message = stageOne(mode, message)
            message = stageTwo(message)
        if mode == 'D':
            message = stageTwo(message)
            message = stageOne(mode, message)
        if mode not in ['E', 'D']:
            E_D_Text_Output['text'] = "Error: mode is not Found!"
            raise SystemExit
        return message

    E_D_Text_Output['text'] = encryptDecrypt(mode)


b.bind('<Button-1>', Crypt)
b.pack()
E_D_Text_Output.pack()

check_label = Label(root, text='Check Mode:', bg='white', fg='red', width=100)
check_entry = Entry(root, bg='black', fg='white', width=100)
check_bot = Button(root, text='Check')

check_label.pack()

check_bot.bind('<Button-1>', Crypt)
check_bot.pack()
check_entry.pack()

root.mainloop()
