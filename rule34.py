import requests
import os

# Базовый URL API
BASE_URL = "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index"

# Функция для загрузки постов
def download_posts(tags, limit=100, page=0, output_dir="downloads"):
    # Создание папки для загрузки изображений
    os.makedirs(output_dir, exist_ok=True)

    # Параметры запроса
    params = {
        "tags": tags,   # Теги для поиска
        "limit": limit, # Количество постов (максимум 1000)
        "pid": page,    # Номер страницы
        "json": 1       # Формат ответа JSON
    }

    # Запрос к API
    response = requests.get(BASE_URL, params=params)

    # Проверка статуса ответа
    if response.status_code == 200:
        posts = response.json()

        # Перебор всех постов
        for post in posts:
            image_url = post.get("file_url")  # Ссылка на изображение
            post_id = post.get("id")         # ID поста

            if image_url:
                try:
                    # Скачивание изображения
                    img_data = requests.get(image_url).content

                    # Определение имени файла
                    file_name = os.path.join(output_dir, f"{post_id}_{image_url.split('/')[-1]}")

                    # Сохранение изображения
                    with open(file_name, 'wb') as file:
                        file.write(img_data)

                    print(f"Скачано: {file_name}")
                except Exception as e:
                    print(f"Ошибка при загрузке {image_url}: {e}")
            else:
                print(f"У поста {post_id} нет файла.")
    else:
        print(f"Ошибка API: {response.status_code}, {response.text}")

# Пример вызова функции
download_posts(tags="miside", limit=1000, output_dir="C:/Games/modding/mita")
