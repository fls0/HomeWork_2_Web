import json
import os
from datetime import datetime
from NoteBook.promp_ut import Completer, RainbowLexer, Sort_Completer
from prompt_toolkit import prompt
from colorama import init, Fore, Style
from abc import ABC, abstractmethod

def input_error(inner):
    def wrap(*args):        
        try:            
            result = inner(*args)
            if result is None:
                return 'Unknown command'
            return result
        except KeyError:
            return "KeyError"
        except ValueError:
            return "ValueError"
        except IndexError:
            return "IndexError"         
    return wrap

class Note:
    """Клас Note. 
        Основна сутність нашого NoteBook 
        Вирішив що буде мати такі поля (подивився як в телефоні):
            - title - заголовок
            - content - текст замітки
            - tags - теги замітки відповідно до тз
            - created_at - дата створення
     """
    def __init__(self, title, content, tags=None, created_at=None):
        self.title = title
        self.content = content
        self.tags = tags or []
        self.created_at = created_at
        
class Manager:
    """Клас Manager.
    Тут написані методи що використовуються для виконня завдання:    
        - def upload_notes - завантажує нотатки з диску. (Виконується при запуску)
        - def save_notes - зберігає нотатки на диск. (виконується 1- коли створюємо, 2- коли редактуємо, 3- коли видаляємо)
        - def add_notes - додає нотатки.
        - def edit_note - редактує нотатки
        - def delete_note - видаляє нотатки
        - def search_notes_by_tag - шукає нотатки по тегу(ам)
        - def search_notes_by_content - шукає нотатки по тексту нотатки.
        """
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.notes = []

    # Завантаження з диску
    def upload_notes(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as file:
                data = json.load(file)
                self.notes = [Note(**note_data) for note_data in data]

    # Завантаження на диск
    def save_notes(self):
        with open(self.storage_path, 'w') as file:
            data = [note.__dict__ for note in self.notes]
            json.dump(data, file, indent=4)

    def add_note(self, title, content, tags=None,):
        note = Note(title, content, tags, created_at=datetime.now().strftime('%Y-%m-%d %H:%M'))
        self.notes.append(note)

    def edit_note(self, note_index, title, content, tags=None):
        # if 0 <= note_index < len(self.notes):
            note = self.notes[note_index]
            note.title = title
            note.content = content
            note.tags = tags or []
            note.created_at = datetime.now().strftime('%Y-%m-%d %H:%M')  # Он  # Оновлюємо дату створення

    def delete_note(self, note_index):
        # if 0 <= note_index < len(self.notes):
            del self.notes[note_index]

    def search_notes_by_tag(self, tag):
        return [note for note in self.notes if tag.lower() in [t.lower() for t in note.tags]]

    def search_notes_by_content(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.content.lower()]
    
    def display_note(self, index, note):
        print(f"Note {index + 1}:")
        print(f"Title: {note.title.upper()}")
        print(f"Content: {note.content}")
        print(f"Tags: {', '.join(note.tags)}")
        print(f"Created At: {note.created_at}")
    
    def display_notes(self):
        for i, note in enumerate(self.notes):
            print(f"Note {i + 1}:")
            print(f"Title: {note.title.upper()}")
            print(f"Content: {note.content}")
            print(f"Tags: {', '.join(note.tags)}")
            print(f"Created At: {note.created_at}")
            print("-" * 30)
    #Сортування 
    def sort_notes(self, by_name=False, by_tags=False, by_created_date=False):
            if by_name:
                sorted_notest = sorted(self.notes, key=lambda x: x.title)
            elif by_tags:
                sorted_notest = sorted(self.notes, key=lambda x: x.tags)
            elif by_created_date:
                sorted_notest = sorted(self.notes, key=lambda x: x.created_at)
            else:
                return None
            return sorted_notest

    
@input_error # Повертає помилку при некорректному вводі
def input_index(note_manager):
    input_str = prompt("Input note index (or press 'Enter' to return): ", lexer=RainbowLexer())
    if input_str == '':
        return ''     
    elif input_str.isdigit():
        index = int(input_str) - 1
        index_note = note_manager.notes[index] # Провокуємо помилку, якщо нотатки з таким індексом немає       
        return index     
      
def main():
    storage_path = 'notes.json'
    note_manager = Manager(storage_path)
    note_manager.upload_notes()
    print("Доступні команди:'Add a Note','Edit a Note','Delete a Note', 'Search by Tag', 'Search by Content', 'Display Notes','Sort','Exit'")

    while True:
       
        choice = prompt('Enter your command: ', completer = Completer, lexer = RainbowLexer())
       
        if choice == 'Add a Note':            
            title =         prompt("Type new note title: (or press 'Enter' to return)", lexer = RainbowLexer())
            if title:
                content =   prompt("Enter note content: ", lexer = RainbowLexer())
                input_tags =      prompt("Enter tags (comma-separated): ", lexer = RainbowLexer())
                tags = [tag.strip() for tag in input_tags.split(',') if tag.strip()]
                note_manager.add_note(title, content, tags)
                note_manager.save_notes()
                print(Fore.GREEN + "Note added!")

        elif choice == 'Edit a Note':
            while True:
                index = input_index(note_manager)  
                if index == '':
                    break       
                elif isinstance(index, str):  # Перевірка, чи результат - рядок
                    print(index, ", Please enter a valid number")  # Виводимо повідомлення про помилку
                    continue
                print("Old title: ", note_manager.notes[index].title.upper())                
                title   =     prompt("Enter new title: (or press 'Enter' to skip)", lexer = RainbowLexer())
                if not title:
                    title = note_manager.notes[index].title
                print("Old content: ", note_manager.notes[index].content)
                content =     prompt("Enter new content: (or press 'Enter' to skip)", lexer = RainbowLexer())
                if not content:
                    content = note_manager.notes[index].content
                print("Old tags: ", note_manager.notes[index].tags)
                input_tags    =     prompt("Enter new tags (comma-separated) (or press 'Enter' to skip): ", lexer = RainbowLexer())
                if input_tags == '':
                    tags = note_manager.notes[index].tags
                else:
                    tags = [tag.strip() for tag in input_tags.split(',') if tag.strip()]
                note_manager.edit_note(index, title, content, tags)
                note_manager.save_notes()
                print(Fore.GREEN + "Note edited!")
                break

        elif choice == 'Delete a Note':
            while True:                
                index = input_index(note_manager) 
                if index == '':
                    break             
                elif isinstance(index, str):  # Перевірка, чи результат - рядок
                    print(index, ", Please enter a valid number")  # Виводимо повідомлення про помилку
                    continue
                note = note_manager.notes[index]
                note_manager.display_note(index, note)
                to_delete = input("Delete? Press 'Y'+'Enter' -> Yes; Press 'Enter' -> No >>")
                if to_delete.lower() != 'y':
                    break
                note_manager.delete_note(index)
                note_manager.save_notes()
                print(Fore.GREEN + "Note deleted!")
                break

        elif choice == 'Search by Tag':
            tag = prompt("Enter tag to search for: ", lexer = RainbowLexer())
            matching_notes = note_manager.search_notes_by_tag(tag)
            if matching_notes:
                for note in matching_notes:
                    print(f"Title: {note.title.upper()}") 
                    print(f"Content: {note.content}")
                    print(f"Tags: {', '.join(note.tags)}")
                    print(f"Created At: {note.created_at}")
                    print("-" * 30)
            else:
                print(Fore.GREEN + "No notes found with this tag.")

        elif choice == 'Search by Content':
            keyword = prompt("Enter keyword to search for: ", lexer = RainbowLexer())
            matching_notes = note_manager.search_notes_by_content(keyword)
            if matching_notes:
                for note in matching_notes:
                    print(f"Title: {note.title.upper()}") 
                    print(f"Content: {note.content}")
                    print(f"Tags: {', '.join(note.tags)}")
                    print(f"Created At: {note.created_at}")
                    print("-" * 30)
            else:
                print(Fore.GREEN + "No notes found with this keyword.")

        elif choice == 'Display Notes':
            note_manager.display_notes()

        elif choice == "Sort":
            print('Доступні сортування: Sort by name, Sort by tags, Sort by date')            
            sort_choice = prompt(f'{" > "*10}Enter sort type: ', completer = Sort_Completer, lexer = RainbowLexer())
                       
            if sort_choice == "Sort by name":
                sorted_notes = note_manager.sort_notes(by_name=True)
            elif sort_choice == "Sort by tags":
                sorted_notes = note_manager.sort_notes(by_tags=True)
            elif sort_choice == "Sort by date":
                sorted_notes = note_manager.sort_notes(by_created_date=True)
            else:
                print("Невірний вибір сортування")
                continue
          
            if sorted_notes:
                for note in sorted_notes: 
                    print(f"Title: {note.title.upper()}") 
                    print(f"Content: {note.content}")
                    print(f"Tags: {', '.join(note.tags)}")
                    print(f"Created At: {note.created_at}")
                    print("-" * 30)        

        elif choice == 'Exit':
            print("Good bye!")
            break

if __name__ == "__main__":
    init(autoreset=True)
    main()

