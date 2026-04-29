"""
FokusMask v0.2 - Приложение для воспроизведения шумов
Автор: FocusMask Team
Версия: 0.2"""

# Импорт необходимых библиотек
import tkinter as tk
from tkinter import messagebox
import pygame  # Для воспроизведения звука
from PIL import Image, ImageTk  # Для работы с изображениями
import os  # Для работы с путями к файлам

# Инициализация pygame mixer для работы со звуком
pygame.mixer.init()

# Глобальная переменная для отслеживания текущего воспроизводимого шума
current_sound = None

def get_asset_path(subfolder, filename):
    """
    Функция для получения полного пути к файлу ассетов
    subfolder: 'audio' или 'design'
    filename: имя файла
    """
    # Получаем путь к директории, где находится main.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Формируем полный путь к файлу
    return os.path.join(base_dir, 'assets', subfolder, filename)

def load_button_image(image_path, width=130, height=70):
    """
    Загрузка и масштабирование изображения для кнопки
    image_path: путь к изображению
    width, height: размеры кнопки (по умолчанию 130x70)
    """
    try:
        # Открываем изображение
        img = Image.open(image_path)
        # Изменяем размер изображения
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        # Конвертируем в формат для tkinter
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
    elif noise_type == 'brown':
        filename = 'brown_noise.wav'
    elif noise_type == 'rain':
        filename = 'rain_noise.wav'
    else:
        print(f"Неизвестный тип шума: {noise_type}")
        return
    
    # Получаем полный путь к файлу
    sound_path = get_asset_path('audio', filename)
    
    # Проверяем существование файла
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
        current_sound.play(loops=-1)  # loops=-1 означает бесконечное воспроизведение
        print(f"Воспроизводится: {noise_type} шум")
        
    except Exception as e:
        print(f"Ошибка воспроизведения: {e}")
        messagebox.showerror("Ошибка", f"Не удалось воспроизвести файл {filename}")

def stop_all_noises():
    """
    Функция для остановки всех звуков
    """
    global current_sound
    
    try:
        # Останавливаем воспроизведение
        pygame.mixer.stop()
        current_sound = None
        print("Воспроизведение остановлено")
    except Exception as e:
        print(f"Ошибка остановки: {e}")

def create_button(parent, image_path, command, width=130, height=70):
    """
    Создание кнопки с изображением
    parent: родительский виджет
    image_path: путь к изображению
    command: функция для вызова при нажатии
    width, height: размеры кнопки
    """
    # Загружаем изображение
    img = load_button_image(image_path, width, height)
    
    if img:
        # Если изображение загружено успешно, создаем кнопку с картинкой
        button = tk.Button(parent, image=img, command=command, bd=0)
        button.image = img  # Сохраняем ссылку на изображение
        return button
    else:
        # Если изображение не загружено, создаем текстовую кнопку как запасной вариант
        print("Создана текстовая кнопка как запасной вариант")
        text = os.path.basename(image_path).replace('_button.png', '').replace('_', ' ').title()
        button = tk.Button(parent, text=text, command=command, width=15, height=2)
        return button

def main():
    """
    Главная функция для создания пользовательского интерфейса
    """
    # Создание главного окна
    root = tk.Tk()
    root.title("FokusMask v0.2")
    root.geometry("500x400")
    root.resizable(False, False)
    
    # Заголовок приложения
    title_label = tk.Label(
        root, 
        text="FokusMask", 
        font=("Arial", 24, "bold")
    )
    title_label.pack(pady=20)
    
    # Размеры кнопок (можно изменить при необходимости)
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
        200,  # stop кнопка может быть шире
        60
    )
    stop_btn.pack(pady=20)
    
    # Фрейм для ползунка громкости (пока не трогаем, но оставляем заготовку)
    volume_frame = tk.Frame(root)
    volume_frame.pack(pady=10)
    
    # Подпись для ползунка
    volume_label = tk.Label(
        volume_frame,
        text="Громкость (будет реализовано позже)",
        font=("Arial", 10),
        fg="gray"
    )
    volume_label.pack()
    
    # Запуск главного цикла
    root.mainloop()

# Точка входа в программу
if __name__ == "__main__":
    # Проверка наличия необходимых директорий
    required_dirs = [
        'assets/audio',
        'assets/design'
    ]
    
    print("=== FokusMask v0.1 ===")
    print("Проверка наличия необходимых папок:")
    
    for dir_path in required_dirs:
        full_path = os.path.join(os.path.dirname(__file__), dir_path)
        if not os.path.exists(full_path):
            print(f"  ВНИМАНИЕ: Папка {dir_path} не найдена!")
            print(f"  Будет создана автоматически: {full_path}")
            os.makedirs(full_path, exist_ok=True)
        else:
            print(f"  OK: Папка {dir_path} найдена")
    
    print("\nНеобходимые аудиофайлы (положите их в assets/audio/):")
    print("  - white_noise.wav (белый шум)")
    print("  - brown_noise.wav (коричневый шум)")
    print("  - rain_noise.wav (шум дождя)")
    
    print("\nНеобходимые изображения (положите их в assets/design/):")
    print("  - preset1_button.png (кнопка для белого шума)")
    print("  - preset2_button.png (кнопка для коричневого шума)")
    print("  - preset3_button.png (кнопка для шума дождя)")
    print("  - stop_button.png (кнопка 'Стоп')")
    
    print("\nРекомендуемый размер изображений: 130x70 пикселей")
    print("Для stop_button.png: 200x60 пикселей")
    
    print("\nЗапуск программы...\n")
    
    # Запускаем главную функцию
    main()