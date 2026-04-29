"""
FokusMask v0.3 - Приложение для воспроизведения шумов
Версия с ttkbootstrap, стилизованным ползунком громкости и полным функционалом
"""

# Импорт необходимых библиотек
import tkinter as tk
from tkinter import messagebox
import pygame  # Для воспроизведения звука
from PIL import Image, ImageTk  # Для работы с изображениями
import os  # Для работы с путями к файлам
import ttkbootstrap as tb  # Стилизованные виджеты
from ttkbootstrap.constants import *  # Константы для стилей

# Инициализация pygame mixer для работы со звуком
pygame.mixer.init()

# Глобальные переменные
current_sound = None  # Текущий воспроизводимый звук
volume_scale = None   # Ползунок громкости
volume_percent_label = None  # Метка с процентом громкости

def get_asset_path(subfolder, filename):
    """
    Функция для получения полного пути к файлу ассетов
    subfolder: 'audio' или 'design'
    filename: имя файла
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, 'assets', subfolder, filename)

def load_button_image(image_path, width=130, height=70):
    """
    Загрузка и масштабирование изображения для кнопки
    image_path: путь к изображению
    width, height: размеры кнопки (по умолчанию 130x70)
    """
    try:
        img = Image.open(image_path)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except FileNotFoundError:
        print(f"Ошибка: Не найден файл {image_path}")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

def play_noise(noise_type):
    """
    Функция для воспроизведения шума
    noise_type: тип шума ('white', 'brown', 'rain')
    """
    global current_sound
    
    # Определяем имя файла в зависимости от типа шума
    if noise_type == 'white':
        filename = 'white_noise.wav'
        noise_name = "Белый шум"
    elif noise_type == 'brown':
        filename = 'brown_noise.wav'
        noise_name = "Коричневый шум"
    elif noise_type == 'rain':
        filename = 'rain_noise.wav'
        noise_name = "Шум дождя"
    else:
        print(f"Неизвестный тип шума: {noise_type}")
        return
    
    sound_path = get_asset_path('audio', filename)
    
    if not os.path.exists(sound_path):
        print(f"Ошибка: Файл {sound_path} не найден!")
        messagebox.showerror("Ошибка", f"Аудиофайл {filename} не найден!")
        return
    
    try:
        # Останавливаем текущий звук, если он воспроизводится
        if current_sound is not None:
            pygame.mixer.Sound.stop(current_sound)
        
        # Загружаем и воспроизводим новый звук
        current_sound = pygame.mixer.Sound(sound_path)
        current_sound.play(loops=-1)
        
        # Устанавливаем текущую громкость
        if volume_scale is not None:
            volume_value = volume_scale.get()
            change_volume(volume_value)
        
        print(f"[v0.3] Воспроизводится: {noise_name}")
        
    except Exception as e:
        print(f"Ошибка воспроизведения: {e}")
        messagebox.showerror("Ошибка", f"Не удалось воспроизвести файл {filename}")

def stop_all_noises():
    """
    Функция для остановки всех звуков
    """
    global current_sound
    
    try:
        pygame.mixer.stop()
        current_sound = None
        print("[v0.3] Воспроизведение остановлено")
    except Exception as e:
        print(f"Ошибка остановки: {e}")

def change_volume(value):
    """
    Изменение громкости текущего звука
    value: значение от 0 до 100
    """
    global current_sound, volume_percent_label
    
    volume_level = float(value) / 100.0
    
    if current_sound is not None:
        current_sound.set_volume(volume_level)
    
    # Обновляем метку с процентом
    if volume_percent_label is not None:
        volume_percent_label.config(text=f"{int(float(value))}%")
    
    print(f"[v0.3] Громкость: {int(float(value))}%")

def create_button(parent, image_path, command, width=130, height=70):
    """
    Создание кнопки с изображением
    """
    img = load_button_image(image_path, width, height)
    
    if img:
        button = tb.Button(parent, image=img, command=command, bootstyle="secondary")
        button.image = img
        return button
    else:
        text = os.path.basename(image_path).replace('_button.png', '').replace('_', ' ').title()
        button = tb.Button(parent, text=text, command=command, bootstyle="secondary", width=15)
        return button

def set_volume_to(percent):
    """
    Установка громкости на определенный процент
    """
    if volume_scale is not None:
        volume_scale.set(percent)
        change_volume(percent)

def set_mute():
    """
    Выключение звука (Mute)
    """
    if volume_scale is not None:
        current_value = volume_scale.get()
        if current_value > 0:
            # Сохраняем предыдущее значение и ставим 0
            setattr(set_mute, 'last_volume', current_value)
            volume_scale.set(0)
            change_volume(0)
        else:
            # Восстанавливаем предыдущее значение
            last = getattr(set_mute, 'last_volume', 50)
            volume_scale.set(last)
            change_volume(last)

def main():
    """
    Главная функция для создания пользовательского интерфейса
    """
    global volume_scale, volume_percent_label
    
    # Создание главного окна с ttkbootstrap
    root = tb.Window(themename="darkly")
    root.title("FokusMask v0.3")
    root.geometry("500x480")  # Увеличил высоту для комфортного отображения
    root.resizable(False, False)
    
    # Заголовок приложения с версией
    title_label = tb.Label(
        root, 
        text="FokusMask v0.3", 
        font=("Arial", 24, "bold"),
        bootstyle="inverse-primary"
    )
    title_label.pack(pady=20)
    
    # Подзаголовок
    subtitle_label = tb.Label(
        root,
        text="Сосредоточься с фоновыми шумами",
        font=("Arial", 10),
        bootstyle="secondary"
    )
    subtitle_label.pack(pady=(0, 10))
    
    # Размеры кнопок
    BUTTON_WIDTH = 130
    BUTTON_HEIGHT = 70
    
    # Фрейм для кнопок пресетов
    presets_frame = tk.Frame(root)
    presets_frame.pack(pady=10)
    
    # Кнопка пресета 1 (Белый шум)
    preset1_btn = create_button(
        presets_frame,
        get_asset_path('design', 'preset1_button.png'),
        lambda: play_noise('white'),
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    preset1_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Кнопка пресета 2 (Коричневый шум)
    preset2_btn = create_button(
        presets_frame,
        get_asset_path('design', 'preset2_button.png'),
        lambda: play_noise('brown'),
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    preset2_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Кнопка пресета 3 (Шум дождя)
    preset3_btn = create_button(
        presets_frame,
        get_asset_path('design', 'preset3_button.png'),
        lambda: play_noise('rain'),
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    preset3_btn.pack(side=tk.LEFT, padx=10, pady=10)
    
    # Кнопка Стоп
    stop_btn = create_button(
        root,
        get_asset_path('design', 'stop_button.png'),
        stop_all_noises,
        200,
        60
    )
    stop_btn.pack(pady=20)
    
    # ========== ПОЛЗУНОК ГРОМКОСТИ ==========
    
    volume_container = tb.Frame(root)
    volume_container.pack(pady=15, padx=20, fill="x")
    
    # Верхняя часть
    volume_header = tb.Frame(volume_container)
    volume_header.pack(fill="x", pady=(0, 10))
    
    volume_title = tb.Label(
        volume_header,
        text="🎵 Громкость",
        font=("Arial", 11, "bold"),
        bootstyle="info"
    )
    volume_title.pack(side="left")
    
    volume_percent_label = tb.Label(
        volume_header,
        text="50%",
        font=("Arial", 11, "bold"),
        bootstyle="info"
    )
    volume_percent_label.pack(side="right")
    
    # Ползунок
    volume_scale = tb.Scale(
        volume_container,
        from_=0,
        to=100,
        orient="horizontal",
        bootstyle="info",
        command=change_volume
    )
    volume_scale.set(50)
    volume_scale.pack(fill="x", pady=(0, 10))
    
    # Кнопки быстрой настройки
    volume_buttons = tb.Frame(volume_container)
    volume_buttons.pack(fill="x", pady=(5, 0))
    
    mute_btn = tb.Button(
        volume_buttons,
        text="🔇 Mute",
        bootstyle="danger-outline",
        width=10,
        command=set_mute
    )
    mute_btn.pack(side="left", padx=5)
    
    low_btn = tb.Button(
        volume_buttons,
        text="25%",
        bootstyle="secondary-outline",
        width=8,
        command=lambda: set_volume_to(25)
    )
    low_btn.pack(side="left", padx=5)
    
    mid_btn = tb.Button(
        volume_buttons,
        text="50%",
        bootstyle="info-outline",
        width=8,
        command=lambda: set_volume_to(50)
    )
    mid_btn.pack(side="left", padx=5)
    
    high_btn = tb.Button(
        volume_buttons,
        text="75%",
        bootstyle="warning-outline",
        width=8,
        command=lambda: set_volume_to(75)
    )
    high_btn.pack(side="left", padx=5)
    
    max_btn = tb.Button(
        volume_buttons,
        text="100% 🔊",
        bootstyle="success-outline",
        width=8,
        command=lambda: set_volume_to(100)
    )
    max_btn.pack(side="left", padx=5)
    
    # Строка состояния внизу
    status_label = tb.Label(
        root,
        text="Готов к работе | FokusMask v0.3",
        font=("Arial", 8),
        bootstyle="secondary"
    )
    status_label.pack(side="bottom", pady=10)
    
    print("[v0.3] Приложение FokusMask успешно запущено")
    root.mainloop()

# Точка входа
if __name__ == "__main__":
    print("=== FokusMask v0.3 ===")
    print("Запуск приложения с поддержкой:")
    print("  - 3 типа фоновых шумов")
    print("  - Регулировка громкости")
    print("  - Стилизованный интерфейс ttkbootstrap")
    print("  - Бесконечное зацикливание аудио")
    print()
    
    main()