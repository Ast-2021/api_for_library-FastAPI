Эндпоинты для авторов
POST /author/ - Создание автора
GET /author/ - Получение списка авторов
GET /author/{id} - Получение информации об авторе по id
PUT /author/{id} - Обновление информации об авторе
DELETE /author/{id} - Удаление автора

Эндпоинты для книг
POST /book/ - Добавление книги
GET /book/ - Получение списка книг
GET /book/{id} - Получение информации о книге по id
PUT /book/{id} - Обновление информации о книге
DELETE /book/{id} - Удаление книги

Эндпоинты для выдач
POST /borrow/ - Создание записи о выдаче книги
GET /borrow/ - Получение списка всех выдач
GET /borrow/{id} - Получение информации о выдаче по id
PATCH /borrow/{id} - Завершение выдачи
