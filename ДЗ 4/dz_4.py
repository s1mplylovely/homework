from pydantic import BaseModel, model_validator
from typing import List


class Book(BaseModel):
    title: str
    author: str
    year: int
    available: bool = True
    categories: List[str]

    def is_book_borrow(self) -> None:  # true, если недоступна
        try:
            test_book(self)
            print(f"Книга '{self.title} - {self.author}' в наличии")
        except BookNotAvailable as e:
            print(e)


class User(BaseModel):
    name: str
    email: str
    membership_id: str = ''
    books: List[Book] = []

    @model_validator(mode="after")
    def validate_email(self):
        if ('@' in self.email and '.' in self.email
            and 0 < self.email.find('@') < self.email.find('.')-1 < len(self.email)-2
                and self.email.count('@') == self.email.count('.') == 1):
            return self
        else:
            raise ValueError("email error")

    def books_list(self):
        print(f"Список книг пользователя {self.name}:")
        if len(self.books) == 0:
            print("-")
        else:
            for book in self.books:
                print(f"'{book.title}' - {book.author}")

    def log_operation(func):
        def wrapper(self, book: Book):
            f1 = f"Пользователь {self.name}, id = {self.membership_id} "
            f2 = f" книгу '{book.title}' - {book.author}"
            if func.__name__ == 'add_book':
                if book.available:
                    func(self, book)
                    print(f1+"взял"+f2)
            elif func.__name__ == 'return_book':
                if book in self.books:
                    func(self, book)
                    print(f1+"вернул"+f2)
            else:
                func(self, book)
                pass
        return wrapper

    @log_operation
    def add_book(self, book: Book) -> None:
        if book.available:
            self.books.append(book)
            book.available = False
        else:
            print(f"Книги '{book.title} - {book.author}' нет в наличии")

    @log_operation
    def return_book(self, book: Book) -> None:
        if book in self.books:
            del self.books[self.books.index(book)]
            book.available = True
        else:
            print("Ошибка")


class Library(BaseModel):
    books: List[Book] = []
    users: List[User] = []
    id: int = 1

    def books_list(self):
        print("Список книг:")
        for book in self.books:
            print(
                f"'{book.title}' - {book.author}, {book.year} год, доступ: {book.available}, жанры: {book.categories}")

    def users_list(self):
        print("Список пользователей:")
        for user in self.users:
            print(
                f"Имя: {user.name}, email: {user.email}, id: {user.membership_id}")

    def log_operation(func):
        def wrapper(self, x):
            if x in self.books or self.users:
                func(self, x)
                pass
            else:
                func(self, x)
                if func.__name__ == 'add_book':
                    print(f"Добавлена книга '{x.title}' - {x.author}")
                elif func.__name__ == 'add_user':
                    print(
                        f"Добавлен пользователь {x.name}, id = {x.membership_id}")
        return wrapper

    @log_operation
    def add_book(self, book: Book) -> None:
        if book in self.books:
            print("Эта книга уже добавлена")
        else:
            self.books.append(book)

    @log_operation
    def add_user(self, user: User) -> None:
        if user in self.users:
            print("Такой пользователь уже есть")
        else:
            self.users.append(user)
            user.membership_id = str(self.id).zfill(4)
            self.id += 1

    def find_book(self, title: str) -> None:
        books_titles = [x.title for x in self.books]
        if title in books_titles:
            print(f"Книга '{title}' есть в библиотеке")
        else:
            print(f"Книги '{title}' нет в библиотеке")

    def total_books(self) -> int:
        return len(self.books)


class BookNotAvailable(Exception):
    pass


def test_book(book: Book):
    if book.available:
        pass
    else:
        raise BookNotAvailable(
            f"Книга '{book.title}' - {book.author} недоступна")


user1 = User(name="Ivan", email="ivan@example.com")
# incorrect_user = User(name="Ivan", email="ivan", membership_id="100")
user2 = User(name="Petr", email="petr@example.com")

book1 = Book(title="Евгений Онегин", author="А.С. Пушкин",
             year=1831, categories=["роман в стихах", "классика"])
book2 = Book(title="Отцы и дети", author="И.С. Тургенев",
             year=1862, categories=["роман", "классика"])
library = Library()
library.add_book(book1)
library.add_book(book2)
print('Кол-во книг в библиотеке:')
print(library.total_books())
library.add_user(user1)
library.add_user(user2)
library.books_list()
library.users_list()
library.find_book("Евгений Онегин")
library.find_book("Война и мир")
user1.add_book(book1)
user1.books_list()
user2.add_book(book2)
library.books_list()
user1.return_book(book1)
user1.books_list()
library.books_list()
