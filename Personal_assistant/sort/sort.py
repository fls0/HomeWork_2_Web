import os
import shutil

class FileSorter:
    def __init__(self, path):
        self.path = path
        self.extensions = {
            'images': ('.jpg', '.png', '.jpeg', '.svg'),
            'videos': ('.avi', '.mp4', '.mov', '.mkv'),
            'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
            'music': ('.mp3', '.ogg', '.wav', '.amr'),
            'archives': ('.zip', '.gz', '.tar'),
            'python' : ('.py')
        }

        self.unknown_extensions = set()

        self.for_print = {
            'images': [],
            'videos': [],
            'documents': [],
            'music': [],
            'archives': [],
            'python' : []
        }

    def normalize(self, name):
        return ''.join(c for c in name if c.isalnum() or c in [' ', '.', '_']).rstrip()
    #нормалізує ім;я

    def add_and_print_extensions(self, folder, extension):
        if folder in self.for_print:
            if extension not in self.for_print[folder]:
                self.for_print[folder].append(extension)
        else:
            self.unknown_extensions.add(extension)
    #якщо розширення не в фор_прінт, розширення перекидається до фор_прінт

    def sort_files(self):
        for root, dirs, files in os.walk(self.path):
            for folder in dirs:
                if folder.lower() in self.extensions.keys():
                    dirs.remove(folder)

            for file in files:
                filename, extension = os.path.splitext(file)
                found = False
                for folder, exts in self.extensions.items():
                    if extension.lower() in exts:
                        new_path = os.path.join(root, folder, self.normalize(file))
                        os.makedirs(os.path.dirname(new_path), exist_ok=True)
                        shutil.move(os.path.join(root, file), new_path)
                        found = True
                        self.add_and_print_extensions(folder, extension.lower())
                        break
                if not found:
                    self.unknown_extensions.add(extension.lower())
    #основна частина коду, створюємо нову папку відповідно до розширення папки та перекидуєм її туди, потім викликаємо функцію адд_енд_прінт, ти визначаємо що далі робити з розширенням, або перекидаємо його до невідомих

        for folder in ['archives']:
            for root, dirs, files in os.walk(os.path.join(self.path, folder)):
                for file in files:
                    filename, extension = os.path.splitext(file)
    #розділяємо ім'я та розширення за допомгою функцій ос

                    if extension.lower() in self.extensions['archives']:
                        self.for_print['archives'].append(extension.lower())
    #додаємо в знайдені розширення, знайдений архів

                    if extension.lower() == '.zip':
                        new_folder = os.path.join(root, self.normalize(filename))
                        os.makedirs(new_folder, exist_ok=True)
                        shutil.unpack_archive(os.path.join(root, file), new_folder)
                        os.remove(os.path.join(root, file))
    #розпаковуємо архів за допомогою функцій шутіл та ос

    def print_results(self):
        print('Знайдені розширення:')
        for folder, extensions in self.for_print.items():
            if extensions:
                print(f'{folder}: {", ".join(extensions)}')
        
        print('Невідомі розширення:')
        print(', '.join(self.unknown_extensions))
    
def main():
    while True:    
        print("Для відміни введіть пусту строку або 'cancel'. ")
        path = str(input("Шлях до папки ==> (C:|Users|Oleg|Documents|some_rubbish): "))
        if path == '' or path == 'cancel':
            break
        sorter = FileSorter(path)
        sorter.sort_files()
        sorter.print_results()

if __name__ == "__main__":
    main()