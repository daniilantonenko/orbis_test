## Запуск
``` bash
uvicorn src.app:app --reload
```
### Docker
``` bash
docker build -t orbis .    
docker run -p 8000:8000 orbis
``` 

### Время реализации
Разработка приложения заняла около **18-22 ч**:

- Настройку проекта (структура директорий, зависимости) — 3 ч
- Разработку базовой функциональности (CRUD для файлов) — 9 ч
- Тестирование и исправление ошибок — 6 ч
- Документацию и комментарии — 2-3 ч

### Стек

- **Язык программирования:** Python 3.10
- **Web-фреймворк:** FastAPI
- **База данных:** SQLite
- **ORM библиотека:** Peewee
- **Контейнеризация:** Docker 

### Архитектурные решения

**MVC**
- **Model:** `FileModel` представляет сущность файла.
- **View:** Эндпоинты FastAPI предоставляют интерфейс пользователю.
- **Controller:** Логика обработки запросов, например, загрузка, удаление, синхронизация.
  
**Data Mapper:**
- Использование ORM Peewee для абстракции над SQL-запросами и работы с базой данных.
      
**Клиент-серверная архитектура:**
- Web-приложение реализовано как сервер, обрабатывающий запросы от клиентов в формате JSON.