import os
from datetime import datetime


def save_order_data(chat_id, user_data):
    filename = "orders.txt"
    order_data = {
        "номер": user_data[chat_id]['phone'],
        "пицца": user_data[chat_id]['pizza'],
        "размер": user_data[chat_id]['size'],
        "адрес": user_data[chat_id]['address'],
        "время": user_data[chat_id]['time'].strftime('%Y-%m-%d %H:%M:%S')
    }

    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"Заказ от чата ID: {chat_id}\n")
        for key, value in order_data.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")


def read_orders_from_file():
    orders = []
    try:
        with open("orders.txt", "r", encoding="utf-8") as file:
            lines = file.read().split("\n")
            current_order = None
            for line in lines:
                if line.strip():
                    key, value = line.split(": ")
                    if key == "Заказ от чата ID":
                        if current_order:
                            orders.append(current_order)
                        current_order = {"Чат ID": value.strip()}
                    else:
                        current_order[key] = value.strip()
            if current_order:
                orders.append(current_order)
    except FileNotFoundError:
        pass
    return orders
