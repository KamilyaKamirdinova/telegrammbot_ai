from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from telegram import Update
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, filters
from telegram.ext.filters import Filters


# Путь к вашей модели Keras
MODEL_PATH = 'model.h5'

# Загрузка модели
model = load_model(MODEL_PATH)


# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне изображение для классификации.')


# Функция для обработки входящего изображения
def handle_image(update: Update, context: CallbackContext) -> None:
    # Сохранение изображения, полученного от пользователя
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('input_image.jpg')

    # Загрузка изображения и подготовка для классификации
    img_path = 'input_image.jpg'
    img = image.load_img(img_path, target_size=(30, 30))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x /= 255.0  # Нормализация

    # Предсказание класса
    predictions = model.predict(x)
    class_index = np.argmax(predictions)

    # Определение класса по индексу
    # classes = {
    #     0: 'Speed limit (20km/h)',
    #     1: 'Speed limit (30km/h)',
    #     2: 'Speed limit (50km/h)',
    #     3: 'Speed limit (60km/h)',
    #     4: 'Speed limit (70km/h)',
    #     5: 'Speed limit (80km/h)',
    #     6: 'End of speed limit (80km/h)',
    #     7: 'Speed limit (100km/h)',
    #     8: 'Speed limit (120km/h)',
    #     9: 'No passing',
    #     10: 'No passing veh over 3.5 tons',
    #     11: 'Right-of-way at intersection',
    #     12: 'Priority road',
    #     13: 'Yield',
    #     14: 'Stop',
    #     15: 'No vehicles',
    #     16: 'Veh > 3.5 tons prohibited',
    #     17: 'No entry',
    #     18: 'General caution',
    #     19: 'Dangerous curve left',
    #     20: 'Dangerous curve right',
    #     21: 'Double curve',
    #     22: 'Bumpy road',
    #     23: 'Slippery road',
    #     24: 'Road narrows on the right',
    #     25: 'Road work',
    #     26: 'Traffic signals',
    #     27: 'Pedestrians',
    #     28: 'Children crossing',
    #     29: 'Bicycles crossing',
    #     30: 'Beware of ice/snow',
    #     31: 'Wild animals crossing',
    #     32: 'End speed + passing limits',
    #     33: 'Turn right ahead',
    #     34: 'Turn left ahead',
    #     35: 'Ahead only',
    #     36: 'Go straight or right',
    #     37: 'Go straight or left',
    #     38: 'Keep right',
    #     39: 'Keep left',
    #     40: 'Roundabout mandatory',
    #     41: 'End of no passing',
    #     42: 'End no passing veh > 3.5 tons'
    # }
    classes = {
        0: 'Ограничение максимальной скорости (20km/h)',
        1: 'Ограничение максимальной скорости (30km/h)',
        2: 'Ограничение максимальной скорости (50km/h)',
        3: 'Ограничение максимальной скорости (60km/h)',
        4: 'Ограничение максимальной скорости (70km/h)',
        5: 'Ограничение максимальной скорости (80km/h)',
        6: 'Конец зоны ограничение максимальной скорости (80km/h)',
        7: 'Ограничение максимальной скорости (100km/h)',
        8: 'Ограничение максимальной скорости (120km/h)',
        9: 'Обгон запрещен',
        10: 'Обгон грузовым автомобилям запрещен',
        11: 'Пересечение со второстепенной дорогой',
        12: 'Круговое движение',
        13: 'Уступи дорогу',
        14: 'Движение без остановки запрещено',
        15: 'Движение запрещено',
        16: 'Движение грузовых автомобилей запрещено',
        17: 'Движение направо',
        18: 'Прочие опасности',
        19: 'Опасный поворот (левый)',
        20: 'Опасный поворот (правый)',
        21: 'Опасные повороты',
        22: 'Неровная дорога',
        23: 'Скользкая дорога',
        24: 'Сужение дороги',
        25: 'Дорожные работы',
        26: 'Светофорное регулирование',
        27: 'Пешеходный переход',
        28: 'Дети',
        29: 'Пересечение с велосипедной дорожкой',
        30: 'Гололедица',
        31: 'Дикие животные',
        32: 'Конец зоны всех ограничений',
        33: 'Въезд запрещен',
        34: 'Движение налево',
        35: 'Движение прямо',
        36: 'Движение прямо или направо',
        37: 'Движение прямо или налево',
        38: 'Объезд препятствия справа',
        39: 'Объезд препятствия слева',
        40: 'Главная дорога',
        41: 'Конец зоны запрещения обгона',
        42: 'Конец зоны запрещения обгона грузовым автомобилям'
    }
    predicted_class = classes.get(class_index, 'Неизвестный класс')

    # Вывод результата
    update.message.reply_text(f'Класс изображения: {predicted_class}')


# Функция для обработки команды /help
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Отправьте мне изображение для классификации.')


def main() -> None:
    updater = Updater("6867647010:AAHJ0rgES62Q4jbOJGrH7SxpL3Hztb_jvhU")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo & ~Filters.command, handle_image))
    dp.add_handler(CommandHandler("help", help_command))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
