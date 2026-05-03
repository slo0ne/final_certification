
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "books_data.json"

# Глобальный список книг
books = []

# ==================== РАБОТА С ФАЙЛАМИ ====================

def load_data():
    """Загружает данные из JSON-файла"""
    global books
    if not os.path.exists(DATA_FILE):
        books = []
        return
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            books = json.load(f)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные:\n{e}")
        books = []

def save_data():
    """Сохраняет данные в JSON-файл"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Успех", "Данные сохранены в файл!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные:\n{e}")

# ==================== ФУНКЦИИ ПРИЛОЖЕНИЯ ====================

def refresh_table():
    """Обновляет таблицу с книгами"""
    for row in tree.get_children():
        tree.delete(row)
    
    for book in books:
        tree.insert("", tk.END, values=(
            book.get("title", ""),
            book.get("author", ""),
            book.get("year", ""),
            book.get("genre", ""),
            book.get("status", "В наличии")
        ))

def add_book():
    """Добавляет новую книгу"""
    def save_new_book():
        title = entry_title.get().strip()
        author = entry_author.get().strip()
        year = entry_year.get().strip()
        genre = entry_genre.get().strip()
        status = status_var.get()
        
        if not title or not author:
            messagebox.showwarning("Предупреждение", "Название и автор обязательны для заполнения")
            return
        
        new_book = {
            "id": len(books) + 1,
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "status": status,
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        books.append(new_book)
        refresh_table()
        save_data()
        messagebox.showinfo("Успех", f"Книга \"{title}\" добавлена!")
        add_window.destroy()
    
    # Создаём окно добавления
    add_window = tk.Toplevel(root)
    add_window.title("Добавить книгу")
    add_window.geometry("400x350")
    add_window.resizable(False, False)
    
    # Поля ввода
    tk.Label(add_window, text="Название книги *:", font=("Arial", 10)).pack(pady=(10, 0))
    entry_title = tk.Entry(add_window, width=40, font=("Arial", 10))
    entry_title.pack(pady=5)
    
    tk.Label(add_window, text="Автор *:", font=("Arial", 10)).pack(pady=(10, 0))
    entry_author = tk.Entry(add_window, width=40, font=("Arial", 10))
    entry_author.pack(pady=5)
    
    tk.Label(add_window, text="Год издания:", font=("Arial", 10)).pack(pady=(10, 0))
    entry_year = tk.Entry(add_window, width=40, font=("Arial", 10))
    entry_year.pack(pady=5)
    
    tk.Label(add_window, text="Жанр:", font=("Arial", 10)).pack(pady=(10, 0))
    entry_genre = tk.Entry(add_window, width=40, font=("Arial", 10))
    entry_genre.pack(pady=5)
    
    tk.Label(add_window, text="Статус:", font=("Arial", 10)).pack(pady=(10, 0))
    status_var = tk.StringVar(value="В наличии")
    status_frame = tk.Frame(add_window)
    status_frame.pack(pady=5)
    tk.Radiobutton(status_frame, text="В наличии", variable=status_var, value="В наличии").pack(side=tk.LEFT, padx=10)
    tk.Radiobutton(status_frame, text="Выдана", variable=status_var, value="Выдана").pack(side=tk.LEFT, padx=10)
    
    # Кнопки
    btn_frame = tk.Frame(add_window)
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="Сохранить", command=save_new_book, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Отмена", command=add_window.destroy, bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=10)

def delete_book():
    """Удаляет выбранную книгу"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Предупреждение", "Выберите книгу для удаления")
        return
    
    selected_item = selected[0]
    values = tree.item(selected_item, "values")
    
    # Ищем книгу по названию и автору
    for i, book in enumerate(books):
        if book["title"] == values[0] and book["author"] == values[1]:
            confirm = messagebox.askyesno("Подтверждение", f"Удалить книгу \"{book['title']}\"?")
            if confirm:
                books.pop(i)
                refresh_table()
                save_data()
                messagebox.showinfo("Успех", "Книга удалена!")
            break

def edit_book():
    """Редактирует выбранную книгу"""
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Предупреждение", "Выберите книгу для редактирования")
        return
    
    selected_item = selected[0]
    values = tree.item(selected_item, "values")
    
    # Находим книгу
    for book in books:
        if book["title"] == values[0] and book["author"] == values[1]:
            edit_window = tk.Toplevel(root)
            edit_window.title("Редактировать книгу")
            edit_window.geometry("400x350")
            edit_window.resizable(False, False)
            
            # Поля с текущими значениями
            tk.Label(edit_window, text="Название книги:", font=("Arial", 10)).pack(pady=(10, 0))
            entry_title = tk.Entry(edit_window, width=40, font=("Arial", 10))
            entry_title.insert(0, book["title"])
            entry_title.pack(pady=5)
            
            tk.Label(edit_window, text="Автор:", font=("Arial", 10)).pack(pady=(10, 0))
            entry_author = tk.Entry(edit_window, width=40, font=("Arial", 10))
            entry_author.insert(0, book["author"])
            entry_author.pack(pady=5)
            
            tk.Label(edit_window, text="Год издания:", font=("Arial", 10)).pack(pady=(10, 0))
            entry_year = tk.Entry(edit_window, width=40, font=("Arial", 10))
            entry_year.insert(0, book.get("year", ""))
            entry_year.pack(pady=5)
            
            tk.Label(edit_window, text="Жанр:", font=("Arial", 10)).pack(pady=(10, 0))
            entry_genre = tk.Entry(edit_window, width=40, font=("Arial", 10))
            entry_genre.insert(0, book.get("genre", ""))
            entry_genre.pack(pady=5)
            
            tk.Label(edit_window, text="Статус:", font=("Arial", 10)).pack(pady=(10, 0))
            status_var = tk.StringVar(value=book.get("status", "В наличии"))
            status_frame = tk.Frame(edit_window)
            status_frame.pack(pady=5)
            tk.Radiobutton(status_frame, text="В наличии", variable=status_var, value="В наличии").pack(side=tk.LEFT, padx=10)
            tk.Radiobutton(status_frame, text="Выдана", variable=status_var, value="Выдана").pack(side=tk.LEFT, padx=10)
            
            def save_edit():
                book["title"] = entry_title.get().strip()
                book["author"] = entry_author.get().strip()
                book["year"] = entry_year.get().strip()
                book["genre"] = entry_genre.get().strip()
                book["status"] = status_var.get()
                refresh_table()
                save_data()
                messagebox.showinfo("Успех", "Книга обновлена!")
                edit_window.destroy()
            
            btn_frame = tk.Frame(edit_window)
            btn_frame.pack(pady=20)
            tk.Button(btn_frame, text="Сохранить", command=save_edit, bg="#4CAF50", fg="white", width=12).pack(side=tk.LEFT, padx=10)
            tk.Button(btn_frame, text="Отмена", command=edit_window.destroy, bg="#f44336", fg="white", width=12).pack(side=tk.LEFT, padx=10)
            break

def search_books():
    """Поиск книг"""
    search_term = search_entry.get().strip().lower()
    if not search_term:
        refresh_table()
        return
    
    for row in tree.get_children():
        tree.delete(row)
    
    for book in books:
        if (search_term in book["title"].lower() or 
            search_term in book["author"].lower() or
            search_term in book.get("genre", "").lower()):
            tree.insert("", tk.END, values=(
                book["title"],
                book["author"],
                book.get("year", ""),
                book.get("genre", ""),
                book.get("status", "В наличии")
            ))

def show_statistics():
    """Показывает статистику"""
    total = len(books)
    available = sum(1 for b in books if b.get("status") == "В наличии")
    borrowed = sum(1 for b in books if b.get("status") == "Выдана")
    
    stats_text = f"""
📊 СТАТИСТИКА БИБЛИОТЕКИ

Всего книг: {total}
В наличии: {available}
Выдано: {borrowed}
Загруженность: {int(borrowed/total*100) if total > 0 else 0}%
    """
    messagebox.showinfo("Статистика", stats_text)

# ==================== СОЗДАНИЕ ГЛАВНОГО ОКНА ====================

root = tk.Tk()
root.title("Библиотека / Каталог книг")
root.geometry("900x500")
root.resizable(True, True)

# ==================== ВЕРХНЯЯ ПАНЕЛЬ ПОИСКА ====================

top_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
top_frame.pack(fill=tk.X)

tk.Label(top_frame, text="🔍 Поиск:", font=("Arial", 11), bg="#f0f0f0").pack(side=tk.LEFT, padx=(10, 5))
search_entry = tk.Entry(top_frame, width=40, font=("Arial", 10))
search_entry.pack(side=tk.LEFT, padx=5)
search_entry.bind("<KeyRelease>", lambda event: search_books())
tk.Button(top_frame, text="Сброс", command=refresh_table, bg="#9E9E9E", fg="white").pack(side=tk.LEFT, padx=5)

# ==================== ТАБЛИЦА С КНИГАМИ ====================

columns = ("Название", "Автор", "Год", "Жанр", "Статус")
tree = ttk.Treeview(root, columns=columns, show="headings", height=18)

# Настройка колонок
tree.heading("Название", text="Название книги")
tree.heading("Автор", text="Автор")
tree.heading("Год", text="Год")
tree.heading("Жанр", text="Жанр")
tree.heading("Статус", text="Статус")

tree.column("Название", width=250)
tree.column("Автор", width=180)
tree.column("Год", width=80, anchor=tk.CENTER)
tree.column("Жанр", width=120)
tree.column("Статус", width=100, anchor=tk.CENTER)

# Добавляем полосу прокрутки
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
scrollbar.pack(side=tk.LEFT, fill=tk.Y, pady=10)

# ==================== ПАНЕЛЬ КНОПОК ====================

button_frame = tk.Frame(root, pady=10)
button_frame.pack(fill=tk.X, side=tk.BOTTOM)

btn_style = {"width": 14, "height": 1, "font": ("Arial", 10)}

tk.Button(button_frame, text="📚 Добавить книгу", command=add_book, bg="#4CAF50", fg="white", **btn_style).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="✏️ Редактировать", command=edit_book, bg="#2196F3", fg="white", **btn_style).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="🗑️ Удалить", command=delete_book, bg="#f44336", fg="white", **btn_style).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="📊 Статистика", command=show_statistics, bg="#FF9800", fg="white", **btn_style).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(button_frame, text="💾 Сохранить", command=save_data, bg="#9C27B0", fg="white", **btn_style).pack(side=tk.LEFT, padx=5, pady=5)

# ==================== ЗАПУСК ====================

if __name__ == "__main__":
    load_data()
    refresh_table()
    root.mainloop()