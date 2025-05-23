# 🍕 Liberty Pizza - телеграм бот для заказа пиццы

Liberty Pizza — это Telegram-бот, с помощью которого пользователи могут выбрать пиццу из удобного каталога, добавить товары в корзину, оформить заказ с указанием телефона, адреса доставки и выбрать способ оплаты.

### 📋 Навигация
- [Описание](#description)
- [Стек](#stack)
    - [Бот](#stack-bot)
    - [Бэкенд](#stack-backend)
- [Запуск проекта](#start)
- [Настройка Nginx](#nginx-config)
- [Применение](#usage)
- [Авторы](#authors)

### 🧾 Описание <a id="description"></a>
- Меню разбито по категориям (например, пицца, напитки и т.д.)
- Пользователь может:   
    - Добавлять и удалять товары из корзины
    - Оформить заказ, указав:
        - Номер телефона
        - Адрес доставки
        - Способ оплаты (например, наличными или картой курьеру)


### 🛠️ Стек <a id="stack"></a>
#### 🤖 Бот (Telegram) <a id="stack-bot"></a>
- aiogram==3.17.0 — асинхронный фреймворк для ботов
- celery[redis]==5.4.0 — обработка фоновых задач (например, проверка оплаты)
- redis==5.2.1 — брокер задач и кеш
- asgiref==3.8.1 — вспомогательные утилиты для async приложений
- python-dotenv==1.0.0 — загрузка конфигурации из .env
- psycopg2-binary==2.9.10 — драйвер PostgreSQL
- requests==2.32.3 — HTTP-запросы к backend

#### 🧩 Бэкенд (Django) <a id="stack-backend"></a>
- Django==5.1.6 — web-фреймворк
- djangorestframework==3.15.2 — создание API
- python-dotenv==1.0.0 — конфигурация через .env
- psycopg2-binary==2.9.10 — PostgreSQL
- pillow==11.1.0 — обработка изображений (например, обложки пицц)


### 🚀 Запуск проекта <a id="start"></a>
- Клонируйте репозиторий
```
git clone git@github.com:dentretyakoff/liberty-pizza.git
```
- Установите необходимые компоненты(docker, nginx, certbot)
```
# Docker install
#!/bin/bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo apt-get install -y nginx certbot python3-certbot-nginx
```
- Перейдите в директорию с проектом
```
cd liberty-pizza
```
- Создайте файл .env и заполните необходимые переменные окружения по примеру .env.example
```
cp .env.example .env
```
- Запустите контейнеры 
```
sudo docker compose up -d --build
```
- Войди в админ-панель Django с учетными данными админа из файла `.env`
```
http://your-domain.ru/admin
```
- Скопируй токен бота и заполни его `API_TOKEN` в файле `.env`
```
https://your-domain.ru/admin/authtoken/tokenproxy/
```
- Перезапусти контейнеры
```
sudo docker compose down && sudo docker compose up -d --build
```

### ⚙️ Настройка Nginx <a id="nginx-config"></a>
- Создайте конфигурацию nginx
```
sudo nano /etc/nginx/sites-available/libertypizza.conf
```
```
server {
    listen 80;
    server_name your-domain.ru;
    location / {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Host $http_host;
            proxy_pass http://127.0.0.1:8080/;
    }
}
```
```
sudo ln -s /etc/nginx/sites-available/libertypizza.conf /etc/nginx/sites-enabled
```
- Получите ssl-сертификат для вашего домена
```
sudo certbot --nginx -d your-domain.ru
```

### 📦 Применение <a id="usage"></a>
В следующих разделах админ-панели необходимо создать как минимум один объект:
- Товары -> Категории
- Товары -> Товары
- Точки доставки -> Зоны доставки
- Точки доставки -> Улицы
Далее можно преходить к функционалу бота, просматривать товары, добавлять/удалять товары в корзине, оформлять заказ.

### 👨‍💻 Авторы <a id="authors"></a>
[Денис Третьяков](https://github.com/dentretyakoff)
