# drf_microservice_deploy

Учебный проект интернет-магазина на основе микросервисной архитектуры. Бэкенд построен на Django REST Framework, фронтенд на Vue 3, всё оркестрировано через Docker Compose.

## Архитектура

```
Frontend (Nginx :80)
       │
  API Gateway (:8000)
       │
  ┌────┴────────────────────┐
  │         │               │           │
User     Product          Cart        Order
Service  Service         Service     Service
(:8004)  (:8001)         (:8002)     (:8003)
                              │
                           Redis
```

Все запросы с фронтенда идут через API Gateway, который проксирует их к нужному сервису по префиксу URL.

## Сервисы

| Сервис | Порт | Описание |
|---|---|---|
| `frontend` | 80 | Vue 3 + Nginx |
| `api-gateway` | 8000 | Маршрутизация запросов |
| `user-service` | 8004 | Регистрация, авторизация, JWT |
| `product-service` | 8001 | Каталог товаров и категорий |
| `cart-service` | 8002 | Корзина пользователя |
| `order-service` | 8003 | Оформление и история заказов |
| `shop-redis` | 6379 | Очередь событий между сервисами |

## Стек

- **Backend:** Python, Django REST Framework
- **Frontend:** Vue 3, Pinia, Axios, Tailwind CSS
- **БД:** SQLite (отдельная для каждого сервиса)
- **Брокер:** Redis (pub/sub между сервисами)
- **Деплой:** Docker, Docker Compose

## Запуск

```bash
git clone https://github.com/IlyaH148/drf_microservice_deploy
cd drf_microservice_deploy

# Собрать и запустить все сервисы
docker-compose up --build -d

# Применить миграции и загрузить фикстуры
docker exec -it product-service-1 bash -c "python manage.py migrate && python manage.py loaddata fixtures/products.json"
docker exec -it user-service-1 bash -c "python manage.py migrate"
docker exec -it cart-service-1 bash -c "python manage.py migrate"
docker exec -it order-service-1 bash -c "python manage.py migrate"
```

Открыть в браузере: [http://localhost](http://localhost)

## API

### Auth
| Метод | URL | Описание |
|---|---|---|
| POST | `/api/auth/login/` | Получить JWT токен |
| POST | `/api/users/register/` | Регистрация |
| POST | `/api/auth/refresh/` | Обновить токен |
| GET | `/api/users/profile/` | Профиль пользователя |

### Products
| Метод | URL | Описание |
|---|---|---|
| GET | `/api/products/` | Список товаров |
| GET | `/api/products/?search=` | Поиск по названию |
| GET | `/api/products/?min_price=&max_price=` | Фильтр по цене |
| GET | `/api/categories/` | Список категорий |

### Cart
| Метод | URL | Описание |
|---|---|---|
| GET | `/api/cart/` | Корзина пользователя |
| POST | `/api/cart/add/` | Добавить товар |
| DELETE | `/api/cart/clear/` | Очистить корзину |

### Orders
| Метод | URL | Описание |
|---|---|---|
| POST | `/api/orders/create/` | Создать заказ |
| GET | `/api/orders/` | История заказов |
