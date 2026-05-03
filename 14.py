import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")

        # Поля ввода
        self.date_var = tk.StringVar()
        self.temperature_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.precipitation_var = tk.StringVar()

        tk.Label(root, text="Дата (YYYY-MM-DD)").pack()
        tk.Entry(root, textvariable=self.date_var).pack()

        tk.Label(root, text="Температура (°C)").pack()
        tk.Entry(root, textvariable=self.temperature_var).pack()

        tk.Label(root, text="Описание погоды").pack()
        tk.Entry(root, textvariable=self.description_var).pack()

        tk.Label(root, text="Осадки (да/нет)").pack()
        tk.Entry(root, textvariable=self.precipitation_var).pack()

        # Кнопка добавления записи
        self.add_button = tk.Button(root, text="Добавить запись", command=self.add_record)
        self.add_button.pack()

        # Таблица записей
        self.records_list = ttk.Treeview(root, columns=("date", "temperature", "description", "precipitation"),
                                         show="headings")
        self.records_list.heading("date", text="Дата")
        self.records_list.heading("temperature", text="Температура (°C)")
        self.records_list.heading("description", text="Описание")
        self.records_list.heading("precipitation", text="Осадки")
        self.records_list.pack()

        # Фильтрация
        tk.Label(root, text="Фильтр по дате").pack()
        self.date_filter_var = tk.StringVar()
        tk.Entry(root, textvariable=self.date_filter_var).pack()

        tk.Label(root, text="Фильтр по температуре (> °C)").pack()
        self.temp_filter_var = tk.StringVar()
        tk.Entry(root, textvariable=self.temp_filter_var).pack()

        filter_button = tk.Button(root, text="Применить фильтр", command=self.filter_records)
        filter_button.pack()

        self.data = []
        self.load_data()

    def add_record(self):
        date = self.date_var.get()
        temperature = self.temperature_var.get()
        description = self.description_var.get()
        precipitation = self.precipitation_var.get().lower()

        # Проверка корректности ввода
        if not self.validate_input(date, temperature, description, precipitation):
            return

        self.data.append({
            "date": date,
            "temperature": float(temperature),
            "description": description,
            "precipitation": precipitation
        })
        self.records_list.insert("", "end", values=(date, temperature, description, precipitation))
        self.save_data()

    def validate_input(self, date, temperature, description, precipitation):
        # Проверка даты
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD.")
            return False

        # Проверка температуры
        try:
            float(temperature)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return False

        # Проверка описания
        if not description:
            messagebox.showerror("Ошибка", "Описание не должно быть пустым.")
            return False

        # Проверка осадков
        if precipitation not in ['да', 'нет']:
            messagebox.showerror("Ошибка", "Осадки должны быть 'да' или 'нет'.")
            return False

        return True

    def filter_records(self):
        date_filter = self.date_filter_var.get()
        temp_filter = self.temp_filter_var.get()

        for item in self.records_list.get_children():
            self.records_list.delete(item)

        for record in self.data:
            if (date_filter in record['date'] or not date_filter) and (
            float(record['temperature']) > float(temp_filter) if temp_filter else True):
                self.records_list.insert("", "end", values=(
                record["date"], record["temperature"], record["description"], record["precipitation"]))

    def save_data(self):
        with open("weather_records.json", "w") as f:
            json.dump(self.data, f)

    def load_data(self):
        if os.path.exists("weather_records.json"):
            with open("weather_records.json", "r") as f:
                self.data = json.load(f)
                for record in self.data:
                    self.records_list.insert("", "end", values=(
                    record["date"], record["temperature"], record["description"], record["precipitation"]))


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()