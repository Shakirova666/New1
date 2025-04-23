class Deq:
    """
    Реализация дека на базе вектора
    для языка Python она тривиальна)
    """
    # Конструктор

    def __init__(self):
        self.array = []

    # Количество элементов в деке
    def size(self):
        return len(self.array)

    # Добавить элемент в конец дека
    def push_last(self, c):
        self.array.append(c)

    # Добавить элемент в начало дека
    def push_first(self, c):
        self.array.insert(0, c)

    # Удалить элемент из конца дека
    def pop_last(self):
        return self.array.pop()

    # Удалить элемент из начала дека
    def pop_first(self):
        return self.array.pop(0)

    # Последний элемент дека
    def last(self):
        return self.array[len(self.array) - 1]

    # Первый элемент дека
    def first(self):
        return self.array[0]
