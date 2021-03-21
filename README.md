## REST API сервис

### Подготовка
Если на машине отсутствует следующее ПО (python3.7, postgresql, git), то его необходимо установить.
1. Установить Python версии 3.7 и выше: `sudo apt install python3.7`
1. Установить базу данных PostgreSQL: `sudo apt install postgresql`
   1. Создать базу `candy_delivery`
   1. Создать пользователя `candyshop`
1. Установить Git: `sudo apt install git`
1. Установить nginx: `sudo apt install nginx`
   1. Настроить nginx
   
### Установка

Запустите скрипт: `./home/candyshop/soft/candyshop_api/install.sh` 
Данный скрипт автоматически создаст необходимые директории, скопирует конфигурационные файлы, проект с репозитория, и запустит сервис.

### Описание сервиса

Все API доступны по адресу `http://0.0.0.0:8080/api/...`

1. POST /couriers - `http://0.0.0.0:8080/api/couriers`
1. PATCH /couriers/$courier_id - `http://0.0.0.0:8080/api/couriers/$courier_id`
1. POST /orders - `http://0.0.0.0:8080/api/orders`
1. POST /orders/assign - `http://0.0.0.0:8080/api/orders/assign`
1. POST /orders/complete - `http://0.0.0.0:8080/api/orders/complete`
1. GET /couriers/$courier_id - `http://0.0.0.0:8080/api/couriers/$courier_id`

