import tkinter as tk
from tkinter import ttk

def preset_action(preset_name):
    """Функция для обработки нажатий на кнопки пресетов"""
    print(f"Выбран пресет: {preset_name}")

def stop_action():
    """Функция для обработки нажатия на кнопку Стоп"""
    print("Стоп")

def volume_changed(value):
    """Функция для обработки изменения громкости"""
    print(f"Громкость изменена: {value}")

# Создание главного окна
root = tk.Tk()
root.title("FokusMask v0.1")
root.geometry("500x400")
root.resizable(False, False)

# Заголовок приложения
title_label = tk.Label(
    root, 
    text="FokusMask", 
    font=("Arial", 24, "bold")
)
title_label.pack(pady=20)

# Фрейм для кнопок пресетов
presets_frame = tk.Frame(root)
presets_frame.pack(pady=10)

# Кнопки пресетов
preset1_btn = tk.Button(
    presets_frame,
    text="Пресет 1",
    width=15,
    height=2,
    command=lambda: preset_action("Пресет 1")
)
preset1_btn.pack(side=tk.LEFT, padx=5)

preset2_btn = tk.Button(
    presets_frame,
    text="Пресет 2",
    width=15,
    height=2,
    command=lambda: preset_action("Пресет 2")
)
preset2_btn.pack(side=tk.LEFT, padx=5)

preset3_btn = tk.Button(
    presets_frame,
    text="Пресет 3",
    width=15,
    height=2,
    command=lambda: preset_action("Пресет 3")
)
preset3_btn.pack(side=tk.LEFT, padx=5)

# Кнопка Стоп
stop_btn = tk.Button(
    root,
    text="Стоп",
    width=20,
    height=2,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    command=stop_action
)
stop_btn.pack(pady=20)

# Фрейм для ползунка громкости
volume_frame = tk.Frame(root)
volume_frame.pack(pady=10)

# Подпись для ползунка
volume_label = tk.Label(
    volume_frame,
    text="Громкость:",
    font=("Arial", 10)
)
volume_label.pack()

# Ползунок громкости
volume_scale = tk.Scale(
    volume_frame,
    from_=0,
    to=100,
    orient=tk.HORIZONTAL,
    length=300,
    command=volume_changed
)
volume_scale.set(50)  # Устанавливаем начальное значение 50
volume_scale.pack()

# Запуск главного цикла
if __name__ == "__main__":
    root.mainloop()