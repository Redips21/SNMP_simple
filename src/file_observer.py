class FileObserver:
    name_path: str

    def __init__(self, name_path: str):
        self.name_path = name_path

    def update(self, info: str):
        try:
            with open(self.name_path, 'a', encoding='UTF-8') as file:
                file.write(info + "\n")

        except FileNotFoundError:
            print(f"Файл {self.name_path} не найден")
            return {}
        except TypeError as e:
            print(str(e))
            return {}

    # дописать exception

    # подумать почему при записи лога в файл первая строчка остается пустой
    # сделать так чтобы добавление последнего лога было не в конец файла а в начало