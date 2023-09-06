import telebotimport osfrom dotenv import load_dotenvfrom telebot import typesfrom datetime import datetimeload_dotenv()TOKEN = os.getenv('TOKEN')bot = telebot.TeleBot(TOKEN)# Словарь для хранения информации о заказе каждого пользователяuser_data = {}# Создайте словарь с путями к фотографиям для каждой пиццыpizza_photos = {    "bbq_pizza": "Barbeku.jpg",    "italian_pizza": "Italiano.jpg",    "fajita_pizza": "Fahita.jpg",    "four_cheese_pizza": "Pizza4cheese.jpg",    "pepperoni_pizza": "Peperoni.jpg",    "cheese_lovers_pizza": "CheeseLovers.jpg",    "hot_chili_pizza": "HotChili.jpg",    "pollo_veggi_pizza": "PoloVezhi.jpg",    "mac_chicken_alfredo_pizza": "Alfredo.jpg",    "hawaiian_pizza": "Gavaiskaia.jpg",    "meat_lovers_pizza": "MeatLovers.jpg"}# Функция для сохранения информации о заказах в текстовом файлеdef save_order_data(chat_id):    filename = "orders.txt"    order_data = {        "номер": user_data[chat_id]['phone'],        "пицца": user_data[chat_id]['pizza'],        "размер": user_data[chat_id]['size'],        "адрес": user_data[chat_id]['address'],        "время": user_data[chat_id]['time'].strftime('%Y-%m-%d %H:%M:%S')    }    with open(filename, 'a', encoding='utf-8') as file:        file.write(f"Заказ от чата ID: {chat_id}\n")        for key, value in order_data.items():            file.write(f"{key}: {value}\n")        file.write("\n")# Функция для сохранения информации о заказах в истории пользователяdef save_order_to_history(chat_id):    if 'orders' not in user_data[chat_id]:        user_data[chat_id]['orders'] = []    order_data = {        "номер": user_data[chat_id]['phone'],        "пицца": user_data[chat_id]['pizza'],        "размер": user_data[chat_id]['size'],        "адрес": user_data[chat_id]['address'],        "время": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Добавляем текущее время    }    user_data[chat_id]['orders'].append(order_data)# Функция для отправки сообщения с кнопкой "Заказать пиццу"def send_order_confirmation(chat_id):    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)    item = types.KeyboardButton("🍕Заказать пиццу")    item_history = types.KeyboardButton("⏳История")    markup.add(item, item_history)  # Добавляем кнопку "История"    bot.send_message(chat_id, "Спасибо за ваш заказ, вам перезвонят для уточнения ваших данных!", reply_markup=markup)# Функция для отправки сообщения с кнопкой "Назад"def send_back_button(chat_id):    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)    item = types.KeyboardButton("↩️Назад")    markup.add(item)    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)# Обработчик команды /start иначе пользователь начинает заказ заново@bot.message_handler(commands=['start'])def start(message):    chat_id = message.chat.id    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)    item = types.KeyboardButton("🍕Заказать пиццу")    item_history = types.KeyboardButton("⏳История заказов")    markup.add(item, item_history)  # Добавляем кнопку "История"    bot.send_message(chat_id, "Добро пожаловать! Нажмите кнопку 'Заказать пиццу' для начала или 'История' для просмотра истории заказов.", reply_markup=markup)# Функция для чтения данных из файла orders.txt и парсинга заказовdef read_orders_from_file():    orders = []    try:        with open("orders.txt", "r", encoding="utf-8") as file:            lines = file.read().split("\n")            current_order = None            for line in lines:                if line.strip():  # Пропускаем пустые строки                    key, value = line.split(": ")                    if key == "Заказ от чата ID":                        if current_order:                            orders.append(current_order)                        current_order = {"Чат ID": value.strip()}                    else:                        current_order[key] = value.strip()            if current_order:                orders.append(current_order)    except FileNotFoundError:        pass    return orders# Обработчик команды "История" для просмотра истории заказов@bot.message_handler(func=lambda message: message.text == "⏳История")def show_order_history(message):    chat_id = message.chat.id    # Чтение заказов из файла    orders = read_orders_from_file()    if orders:        markup = types.InlineKeyboardMarkup(row_width=1)        for i, order in enumerate(orders, start=1):            chat_id_order = order.get('Чат ID', '')            button_text = f"Заказ #{i}"            callback_data = f"view_order_{i}"            button = types.InlineKeyboardButton(button_text, callback_data=callback_data)            markup.add(button)        bot.send_message(chat_id, "Выберите заказ для просмотра:", reply_markup=markup)    else:        bot.send_message(chat_id, "У вас пока нет истории заказов.")# Обработчик для просмотра конкретного заказа@bot.callback_query_handler(func=lambda call: call.data.startswith("view_order_"))def view_order(call):    chat_id = call.message.chat.id    order_number = int(call.data.split("_")[2])    # Чтение заказов из файла    orders = read_orders_from_file()    if 0 < order_number <= len(orders):        order = orders[order_number - 1]        order_info = "\n".join([f"{key}: {value}" for key, value in order.items()])        bot.send_message(chat_id, f"Информация о заказе #{order_number}:\n{order_info}")    else:        bot.send_message(chat_id, "Заказ с таким номером не найден.")@bot.message_handler(func=lambda message: message.text == "🍕Заказать пиццу")def order_pizza(message):    chat_id = message.chat.id    bot.send_message(chat_id, "Пожалуйста, введите ваш номер телефона:")    bot.register_next_step_handler(message, get_phone)# Функция для получения номера телефонаdef get_phone(message):    chat_id = message.chat.id    phone = message.text    # Проверяем, что номер телефона состоит из 12 цифр и начинается с 996    if len(phone) == 12 and phone.startswith("996") and phone[3:].isdigit():        user_data[chat_id] = {'phone': phone}        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)        item = types.KeyboardButton("✅ Правильно")        markup.add(item)        item = types.KeyboardButton("❌ Изменить")        markup.add(item)        bot.send_message(chat_id, f"Ваш номер телефона: {phone}. Правильно?", reply_markup=markup)        bot.register_next_step_handler(message, confirm_phone)    else:        bot.send_message(chat_id, "Пожалуйста, введите корректный номер телефона, начиная с 996 и содержащий 12 цифр (без +).")        bot.register_next_step_handler(message, get_phone)# Функция для подтверждения номера телефонаdef confirm_phone(message):    chat_id = message.chat.id    text = message.text    if text == "✅ Правильно":        markup = types.ReplyKeyboardRemove(selective=False)        bot.send_message(chat_id, "Отлично! Теперь вы можете заказать пиццу.", reply_markup=markup)        show_pizza_menu(chat_id)    elif text == "❌ Изменить":        bot.send_message(chat_id, "Введите новый номер телефона:")        bot.register_next_step_handler(message, get_phone)    else:        bot.send_message(chat_id, "Пожалуйста, используйте кнопки \"✅ Правильно\" или \"❌ Изменить\".")        bot.register_next_step_handler(message, confirm_phone)# Функция для отображения меню пиццыdef show_pizza_menu(chat_id):    markup = types.InlineKeyboardMarkup(row_width=1)    pizza_menu = [        ("🍕Барбекю Пицца с курицей", "bbq_pizza"),        ("🍕Итальяно Пицца с курицей", "italian_pizza"),        ("🍕Фахита", "fajita_pizza"),        ("🍕Пицца 4 сыра", "four_cheese_pizza"),        ("🍕Пеперони Пицца", "pepperoni_pizza"),        ("🍕Чиз Ловерс", "cheese_lovers_pizza"),        ("🍕Хот Чили Пицца", "hot_chili_pizza"),        ("🍕Поло Вежжи Пицца", "pollo_veggi_pizza"),        ("🍕Мак Курица Альфредо Пицца", "mac_chicken_alfredo_pizza"),        ("🍕Гавайская Пицца", "hawaiian_pizza"),        ("🍕Meat Lover's Pizza", "meat_lovers_pizza")    ]    for pizza_name, pizza_id in pizza_menu:        button = types.InlineKeyboardButton(pizza_name, callback_data=pizza_id)        markup.add(button)    bot.send_message(chat_id, "Выберите пиццу из меню:", reply_markup=markup)# Обработчик нажатия кнопок с пиццей@bot.callback_query_handler(    func=lambda call: call.data in pizza_photos.keys())def pizza_selection(call):    chat_id = call.message.chat.id    pizza_id = call.data    user_data[chat_id]['pizza'] = pizza_id    # Отправляем фотографию пиццы    photo_path = pizza_photos[pizza_id]    bot.send_photo(chat_id, open(photo_path, 'rb'))    # Отправляем клавиатуру с размерами    markup = types.InlineKeyboardMarkup(row_width=2)    sizes = ["13см - 185сом", "18см - 350сом", "30см - 495сом", "40см - 745сом"]    for size in sizes:        button = types.InlineKeyboardButton(size, callback_data=size)        markup.add(button)    # Добавляем кнопку "Назад"    back_button = types.InlineKeyboardButton("↩️Назад", callback_data="back_to_pizza_selection")    markup.add(back_button)    bot.send_message(chat_id, "Выберите размер пиццы или нажмите \"Назад\" для выбора пиццы заново:", reply_markup=markup)# Обработчик нажатия кнопок "Назад" или пиццы после выбора размера@bot.callback_query_handler(func=lambda call: call.data in pizza_photos.keys() or call.data == "back_to_pizza_selection")def pizza_or_back_selection(call):    chat_id = call.message.chat.id    if call.data == "back_to_pizza_selection":        # Если нажата кнопка "Назад", вернемся к выбору пиццы        show_pizza_menu(chat_id)    else:        # Если нажата кнопка с пиццей, сохраним выбор пиццы и отправим фото        pizza_id = call.data        user_data[chat_id]['pizza'] = pizza_id        # Отправляем фотографию пиццы        photo_path = pizza_photos[pizza_id]        bot.send_photo(chat_id, open(photo_path, 'rb'))        # Отправляем клавиатуру с размерами        markup = types.InlineKeyboardMarkup(row_width=2)        sizes = ["13см - 185сом", "18см - 350сом", "30см - 495сом", "40см - 745сом"]        for size in sizes:            button = types.InlineKeyboardButton(size, callback_data=size)            markup.add(button)        # Добавляем кнопку "Назад"        back_button = types.InlineKeyboardButton("↩️Назад", callback_data="back_to_pizza_selection")        markup.add(back_button)        bot.send_message(chat_id, "Выберите размер пиццы или нажмите \"Назад\" для выбора пиццы заново:", reply_markup=markup)# Обработчик нажатия кнопок с размерами пиццы@bot.callback_query_handler(func=lambda call: call.data in ["13см - 185сом", "18см - 350сом", "30см - 495сом", "40см - 745сом"])def size_selection(call):    chat_id = call.message.chat.id    user_data[chat_id]['size'] = call.data    bot.send_message(chat_id, "Пожалуйста, введите точный адрес для доставки:")    bot.register_next_step_handler(call.message, get_address)# Обработчик нажатия кнопок "Назад"@bot.message_handler(func=lambda message: message.text == "↩️Назад")def go_back(message):    chat_id = message.chat.id    send_back_button(chat_id)# Функция для получения адресаdef get_address(message):    chat_id = message.chat.id    address = message.text    user_data[chat_id]['address'] = address    # Сохраняем текущее время    user_data[chat_id]['time'] = datetime.now()    # Отправляем данные заказа в группу    order_info = f"Номер: {user_data[chat_id]['phone']}\nПицца: {user_data[chat_id]['pizza']}\nРазмер: {user_data[chat_id]['size']}\nАдрес: {address}\nВремя заказа: {user_data[chat_id]['time'].strftime('%Y-%m-%d %H:%M:%S')}"    bot.send_message(-1001876571035, order_info)  # Замените GROUP_CHAT_ID на ID вашей группы    # Сохраняем данные о заказе в текстовом файле    save_order_data(chat_id)    # Сохраняем данные о заказе в истории пользователя    save_order_to_history(chat_id)    # Отправляем сообщение пользователю и кнопку для повторного заказа    send_order_confirmation(chat_id)# Обработчик команды "История" для просмотра истории заказов@bot.message_handler(func=lambda message: message.text == "⏳История")def show_order_history(message):    chat_id = message.chat.id    # Проверяем, есть ли у пользователя история заказов    if chat_id in user_data:        orders = user_data[chat_id].get('orders', [])        if orders:            markup = types.InlineKeyboardMarkup(row_width=1)            for i, order in enumerate(orders, start=1):                pizza_name = order['pizza']                order_time = order['time']                # Создаем кнопку для просмотра заказа с инлайн-колбэком, который содержит номер заказа                callback_data = f"view_order_{i}"                button_text = f"{pizza_name} ({order_time.strftime('%Y-%m-%d %H:%M:%S')})"                button = types.InlineKeyboardButton(button_text, callback_data=callback_data)                markup.add(button)            bot.send_message(chat_id, "Выберите заказ для просмотра:", reply_markup=markup)        else:            bot.send_message(chat_id, "У вас пока нет истории заказов.")    else:        bot.send_message(chat_id, "У вас пока нет истории заказов.")@bot.callback_query_handler(func=lambda call: call.data.startswith("view_order_"))def view_order(call):    chat_id = call.message.chat.id    order_number = int(call.data.split("_")[2])    if chat_id in user_data and 'orders' in user_data[chat_id] and 0 < order_number <= len(user_data[chat_id]['orders']):        order = user_data[chat_id]['orders'][order_number - 1]        if 'номер' in order and 'пицца' in order and 'размер' in order and 'адрес' in order and 'время' in order:            order_info = f"Номер: {order['номер']}\nПицца: {order['пицца']}\nРазмер: {order['размер']}\nАдрес: {order['адрес']}\nВремя заказа: {order['время']}"            bot.send_message(chat_id, f"Информация о заказе #{order_number}:\n{order_info}")        else:            bot.send_message(chat_id, "Заказ не содержит всех необходимых данных.")    else:        bot.send_message(chat_id, "Заказ с таким номером не найден.")if __name__ == "__main__":    bot.polling(none_stop=True)