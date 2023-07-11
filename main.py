from aifc import Error
import requests
import math
from database import *

def get_data():
    '''
    Получение данных из API Auchan и вставка их в базу данных
    '''
    # Создание таблицы в базе данных
    try:
        Base.metadata.create_all(engine)
    except (Exception, Error) as error:
        print("Произошла ошибка при создании базы данных", error)

    params = {
        'merchantId': '1',
        'page': '1',
        'perPage': '40',
    }

    json_data = {
        'filter': {
            'category': 'tverdye_i_polutverdye',
            'promo_only': False,
            'active_only': False,
            'cashback_only': False,
        },
    }

    try:
        response = requests.get('https://www.auchan.ru/v1/catalog/products', params=params, json=json_data).json()
    except requests.exceptions.RequestException as error:
        print("Произошла ошибка при получении данных из API Auchan:", error)
        return

    total_items = response.get("activeRange")
    pages_count = math.ceil(total_items / 40)
    for p in range(1, pages_count + 1):
        params = {
            'merchantId': '1',
            'page': p,
            'perPage': '40',
        }
        json_data = {
            'filter': {
                'category': 'tverdye_i_polutverdye',
                'promo_only': False,
                'active_only': False,
                'cashback_only': False,
            },
        }
        try:
            response = requests.get(f'https://www.auchan.ru/v1/catalog/products', params=params, json=json_data).json()
        except requests.exceptions.RequestException as error:
            print("Произошла ошибка при получении данных из API Auchan:", error)
            return

        info = response.get("items")

        for i in info:
            try:
                Id = int(i.get("id"))
                title = i.get("title")
                link = str('https://www.auchan.ru/product/' + i.get("code"))
                price = int(i.get("price").get("value"))
                old_price = i.get("oldPrice").get("value") if i.get("oldPrice") != None else None
                brand = i.get("brand").get("name")
                product = Product(id=Id, title=title, link=link, price=price, old_price=old_price, brand=brand)
                session.add(product)
            except (Exception, Error) as error:
                print("Произошла ошибка при вставке данных:", error)


if __name__ == "__main__":
    try:
        get_data()
    except (Exception, Error) as error:
        # Обработка ошибок и исключений
        print("Произошла ошибка при вставке данных:", error)
    finally:
        # Закрытие курсора и соединения
        if session:
            session.commit()
            session.close()
            print("Соединение с базой данных закрыто.")