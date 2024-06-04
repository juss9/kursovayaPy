import sqlite3
import tkinter as tk
from tkinter import messagebox

# Подключение к базе данных
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Создание таблицы студентов, если её нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    major TEXT
)
''')
conn.commit()

# Создание таблицы результатов экзаменов, если её нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS exam_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT NOT NULL,
    score INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
''')
conn.commit()

# Функция для добавления студента в базу данных
def add_student(name, age, major):
    cursor.execute('INSERT INTO students (name, age, major) VALUES (?, ?, ?)', (name, age, major))
    conn.commit()
    messagebox.showinfo("Успех", f'Студент {name} успешно добавлен.')

# Функция для просмотра всех студентов
def view_students():
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()

    if not students:
        messagebox.showinfo("Студенты не найдены", "Студентов не найдено.")
    else:
        student_list = "\n".join([f'ID: {student[0]}, ФИО: {student[1]}, Возраст: {student[2]}, Специальность:{student[3]}' for student in students])
        messagebox.showinfo("Список студентов", f"Список студентов:\n{student_list}")

# Функция для обновления информации о студенте
def update_student(student_id, name, age, major):
    cursor.execute('UPDATE students SET name=?, age=?, major=? WHERE id=?', (name, age, major, student_id))
    conn.commit()
    messagebox.showinfo("Успех", f'Информация о студенте с ID {student_id} успешно обновлена.')

# Функция для удаления студента
def delete_student(student_id):
    cursor.execute('DELETE FROM students WHERE id=?', (student_id,))
    conn.commit()
    messagebox.showinfo("Успех", f'Студент с ID {student_id} успешно удален.')

# Функция для добавления результата экзамена для студента
def add_exam_result(student_id, subject, score):
    cursor.execute('INSERT INTO exam_results (student_id, subject, score) VALUES (?, ?, ?)', (student_id, subject, score))
    conn.commit()
    messagebox.showinfo("Успех", f'Результат экзамена успешно добавлен для студента с ID {student_id}.')

# Функция для просмотра результатов экзаменов для студента
def view_exam_results(student_id):
    cursor.execute('SELECT * FROM exam_results WHERE student_id=?', (student_id,))
    exam_results = cursor.fetchall()

    if not exam_results:
        messagebox.showinfo("Результаты не найдены", f'Результаты экзаменов для студента с ID {student_id} не найдены.')
    else:
        result_list = "\n".join([f'Предмет: {result[2]}, Балл: {result[3]}' for result in exam_results])
        messagebox.showinfo("Результаты экзаменов", f'Результаты экзаменов для студента с ID {student_id}:\n{result_list}')

# Функция для отображения главного окна меню
def show_menu_window():
    menu_window = tk.Tk()
    menu_window.title("Система Управления Базой Данных Студентов")
    menu_window.configure(bg='#FFEBEB')  # Установка цвета фона в нежно-розовый

    label_student_id = tk.Label(menu_window, text="ID студента:", bg='#FFEBEB')
    entry_student_id = tk.Entry(menu_window)

    label_name = tk.Label(menu_window, text="ФИО:", bg='#FFEBEB')
    entry_name = tk.Entry(menu_window)

    label_age = tk.Label(menu_window, text="Возраст:", bg='#FFEBEB')
    entry_age = tk.Entry(menu_window)

    label_major = tk.Label(menu_window, text="Специальность:", bg='#FFEBEB')
    entry_major = tk.Entry(menu_window)

    label_subject = tk.Label(menu_window, text="Предмет:", bg='#FFEBEB')
    entry_subject = tk.Entry(menu_window)

    label_score = tk.Label(menu_window, text="Балл:", bg='#FFEBEB')
    entry_score = tk.Entry(menu_window)

    label_student_id.pack()
    entry_student_id.pack()

    label_name.pack()
    entry_name.pack()

    label_age.pack()
    entry_age.pack()

    label_major.pack()
    entry_major.pack()

    label_subject.pack()
    entry_subject.pack()

    label_score.pack()
    entry_score.pack()

    def on_submit():
        choice = menu_window_choice.get()
        handle_menu_choice(choice)

    menu_window_choice = tk.StringVar()
    menu_window_choice.set("1")

    # Функция для обработки выбора в меню
    def handle_menu_choice(choice):
        if choice == '1':
            name = entry_name.get()
            age = entry_age.get()
            major = entry_major.get()
            add_student(name, age, major)
        elif choice == '2':
            view_students()
        elif choice == '3':
            student_id = entry_student_id.get()
            name = entry_name.get()
            age = entry_age.get()
            major = entry_major.get()
            update_student(student_id, name, age, major)
        elif choice == '4':
            student_id = entry_student_id.get()
            delete_student(student_id)
        elif choice == '5':
            student_id = entry_student_id.get()
            subject = entry_subject.get()
            score = entry_score.get()
            add_exam_result(student_id, subject, score)
        elif choice == '6':
            student_id = entry_student_id.get()
            view_exam_results(student_id)
        else:
            messagebox.showinfo("Неверный выбор", "Пожалуйста, введите число от 1 до 6.")

    # Добавление переключателей для выбора в меню
    menu_choices = [
        ("Добавить студента", "1"),
        ("Просмотреть студентов", "2"),
        ("Обновить информацию о студенте", "3"),
        ("Удалить студента", "4"),
        ("Добавить результат экзамена", "5"),
        ("Просмотреть результаты экзаменов", "6"),
    ]

    for text, choice in menu_choices:
        tk.Radiobutton(menu_window, text=text, variable=menu_window_choice, value=choice, bg='#FFEBEB').pack()

    submit_button = tk.Button(menu_window, text="Выполнить", command=on_submit, bg='#FFD9D9')  # Кнопка с нежно-красным цветом
    submit_button.pack()

    menu_window.mainloop()

# Вызов функции для отображения главного окна меню
show_menu_window()

# Закрытие соединения с базой данных
conn.close()
