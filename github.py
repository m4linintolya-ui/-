import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("700x500")
        self.filename = "books.json"
        self.books = self.load_data()

        # --- Форма ввода ---
        frame_form = tk.Frame(root, pady=10)
        frame_form.pack()

        tk.Label(frame_form, text="Название:").grid(row=0, column=0)
        self.ent_title = tk.Entry(frame_form)
        self.ent_title.grid(row=0, column=1, padx=5)

        tk.Label(frame_form, text="Автор:").grid(row=0, column=2)
        self.ent_author = tk.Entry(frame_form)
        self.ent_author.grid(row=0, column=3, padx=5)

        tk.Label(frame_form, text="Жанр:").grid(row=1, column=0, pady=5)
        self.ent_genre = tk.Entry(frame_form)
        self.ent_genre.grid(row=1, column=1, padx=5)

        tk.Label(frame_form, text="Страниц:").grid(row=1, column=2)
        self.ent_pages = tk.Entry(frame_form)
        self.ent_pages.grid(row=1, column=3, padx=5)

        btn_add = tk.Button(frame_form, text="Добавить книгу", command=self.add_book, bg="#e1e1e1")
        btn_add.grid(row=2, column=0, columnspan=4, sticky="we", pady=10)

        # --- Фильтрация ---
        frame_filter = tk.Frame(root)
        frame_filter.pack(fill="x", padx=10)
        
        tk.Label(frame_filter, text="Фильтр по жанру:").pack(side="left")
        self.ent_filter_genre = tk.Entry(frame_filter, width=15)
        self.ent_filter_genre.pack(side="left", padx=5)
        
        tk.Button(frame_filter, text="Применить", command=self.update_table).pack(side="left")
        tk.Button(frame_filter, text="Сброс", command=self.reset_filter).pack(side="left", padx=5)
        
        self.check_pages_var = tk.BooleanVar()
        tk.Checkbutton(frame_filter, text="Более 200 стр.", variable=self.check_pages_var, command=self.update_table).pack(side="left")

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страниц")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_table()

    def add_book(self):
        title = self.ent_title.get().strip()
        author = self.ent_author.get().strip()
        genre = self.ent_genre.get().strip()
        pages = self.ent_pages.get().strip()

        # Валидация
        if not all([title, author, genre, pages]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        
        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {"title": title, "author": author, "genre": genre, "pages": int(pages)}
        self.books.append(new_book)
        self.save_data()
        self.update_table()
        
        # Очистка полей
        for entry in [self.ent_title, self.ent_author, self.ent_genre, self.ent_pages]:
            entry.delete(0, tk.END)

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        genre_filter = self.ent_filter_genre.get().lower()
        only_big_books = self.check_pages_var.get()

        for book in self.books:
            if genre_filter and genre_filter not in book['genre'].lower():
                continue
            if only_big_books and book['pages'] <= 200:
                continue
            
            self.tree.insert("", "end", values=(book['title'], book['author'], book['genre'], book['pages']))

    def reset_filter(self):
        self.ent_filter_genre.delete(0, tk.END)
        self.check_pages_var.set(False)
        self.update_table()

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
