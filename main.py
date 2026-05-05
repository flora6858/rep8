import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = self.load_data()

        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar()
        categories = ["Еда", "Транспорт", "Развлечения", "Жильё", "Прочее"]
        self.category_combo = ttk.Combobox(self.root, textvariable=self.category_var, values=categories)
        self.category_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Сумма", "Категория", "Дата"), show="headings")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Фильтрация
        tk.Label(self.root, text="Фильтр по категории:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_var = tk.StringVar()
        filter_combo = ttk.Combobox(self.root, textvariable=self.filter_var, values=["Все"] + categories)
        filter_combo.set("Все")
        filter_combo.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Период с (ГГГГ-ММ-ДД):").grid(row=6, column=0, padx=5, pady=5)
        self.start_date_entry = tk.Entry(self.root)
        self.start_date_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.root, text="по (ГГГГ-ММ-ДД):").grid(row=7, column=0, padx=5, pady=5)
        self.end_date_entry = tk.Entry(self.root)
        self.end_date_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтры", command=self.apply_filters).grid(row=8, column=0, columnspan=2, pady=10)

        # Подсчёт суммы
        self.total_label = tk.Label(self.root, text="Общая сумма: 0")
        self.total_label.grid(row=9, column=0, columnspan=2, pady=5)

    def validate_input(self, amount, date_str):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректная сумма")
            return False

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты (используйте ГГГГ-ММ-ДД)")
            return False
        return True

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_var.get()
        date_str = self.date_entry.get()

        if not self.validate_input(amount, date_str):
            return

        expense = {
            "amount": float(amount),
            "category": category,
            "date": date_str
        }
        self.expenses.append(expense)
        self.save_data()
        self.update_table()
        # Очистка полей
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)

    def update_table(self, filtered_expenses=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        display_expenses = filtered_expenses if filtered_expenses else self.expenses
        for expense in display_expenses:
            self.tree.insert("", "end", values=(expense["amount"], expense["category"], expense["date"]))

        total = sum(exp["amount"] for exp in display_expenses)
        self.total_label.config(text=f"Общая сумма: {total}")

    def apply_filters(self):
        category_filter = self.filter_var.get()
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()

        filtered = self.expenses

        if category_filter != "Все":
            filtered = [exp for exp in filtered if exp["category"] == category_filter

        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                filtered = [exp for exp in filtered if datetime.strptime(exp["date"], "%Y-%m-%d") >= start_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат начальной даты")
                return

        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
                filtered = [exp for exp in filtered if datetime.strptime(exp["date"], "%Y-%m-%d") <= end_date]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат конечной даты")
                return

        self.update_table(filtered)

    def save_data(self):
        with open("expenses.json", "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("expenses.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
