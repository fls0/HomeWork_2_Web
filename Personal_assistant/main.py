from AdressBook.AB import main as ab_main
from NoteBook.NB import main as nb_main
from Map.Map import main as map_main
from sort.sort import main as sort_main
import os

def cls():
    os.system(['clear','cls'][os.name == 'nt'])

def menu():
    cls()
    while True:
        cls()
        print('MENU')
        choice = input(
            'Вітаю, я ваш персональний помічник.\nОберіть функцію:\n1.Записна книжка\n2.Нотатник\n3.Карта\n4.Сортування папки\n0.Вихід\n>>>')
        if choice == '1':
            cls()
            ab_main()
        elif choice == '2':
            cls()
            nb_main()
        elif choice == '3':
            cls()
            map_main()
        elif choice == '4':
            cls()
            sort_main()
        # elif choice == '5':
        #     cls()
        #     game_main()
        elif choice == '0':
            break

if __name__ == '__main__':
    menu()
