'''
Скрипт для сохранения структуры директории в файл.

Сама структура сохраняется в \diles\название_директории.json
Сжатая структура сохраняется в \files (сжатые данные)\название_директории.bin

'''

from json import dumps
from os import mkdir, walk
from os.path import abspath, exists
from zlib import compress


class Tree:
    def __init__(self, path=''):
        if not path:
            path = abspath(__file__).split('\\')[:-1]
            self.path = self.project_path = '\\'.join(path)
        elif not exists(path):  # Проверяем, существует ли указанный путь
            raise NotADirectoryError(f'Папка "{path}" не найдена!')
        # Получаем путь к папке проекта
        else:
            project_path = abspath(__file__).split('\\')[:-1]
            self.project_path = '\\'.join(project_path)

            self.path = path

    def get_files_tree(self):  # Получаем список файлов
        structure = {}
        # Если папка находится в папке проекта, записываем сокращённые пути
        if self.project_path in self.path:
            for path, dirs, files in walk(self.path):
                PATH = path.replace(self.path, '')
                structure[PATH] = []
                for file in files:
                    structure[PATH].append(file)
        # Иначе, записываем полные пути
        else:
            for path, dirs, files in walk(self.path):
                structure[path] = []
                for file in files:
                    structure[path].append(file)

        if self.path == self.project_path:  # Если искомая папка и папка проекта - одна и та же, удаляем папку dirs из списка
            try:
                structure.pop('\\files')
                structure.pop('\\files (сжатые данные)')
            except:
                pass

        return structure

    def __str__(self):  # Конвертация списка файлов в строку
        return dumps(self.get_files_tree(), ensure_ascii=False, indent=4)

    def __bytes__(self):  # Функция сжатия данных
        data = dumps(self.get_files_tree())
        return compress(data.encode(), level=9)

    def save(self):  # Сохранение данных в файл
        # Получаем путь для сохранения файлов и создаём его
        path = self.project_path + '\\files'
        if not exists(path):
            mkdir(path)

        # Получаем путь для сохранения сжатых данных и создаём его
        compress_path = self.project_path + '\\files (сжатые данные)'
        if not exists(compress_path):
            mkdir(compress_path)

        # Сохраняем данные в файл
        name = self.path.split('\\')[-1]
        with open(f'{path}\\{name}.json', 'w') as file:
            file.write(str(self))

            print(f'Создан файл {path}\\{name}.json')

        # Сжимаем данные и сохраняем в файл
        with open(f'{compress_path}\\{name}.bin', 'wb') as file:
            file.write(bytes(self))

            print(f'Создан файл {compress_path}\\{name}.json')

if __name__ == '__main__':
    # Сохраняем список файлов текущей директории
    tree = Tree()
    tree.save()

    # Запрашиваем у пользователя путь к папке
    path = input('Введите путь к папке:\n')
    while path:
        try:  # Пытаемся сохранить данные
            tree = Tree(path)
            tree.save()
        except NotADirectoryError as error:  # Если папка не найдена, уведомляем пользователя
            print(error)
        except Exception as error:  # В случае другой ошибки, уведомляем пользователя
            print('Произошла неизвестная ошибка!', error, sep='\n')
        finally:  # В конце, запрашиваем у пользователя путь к папке и выполняем алгоритм заново
            path = input('Введите новый путь к папке:\n')
