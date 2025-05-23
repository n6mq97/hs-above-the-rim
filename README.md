# Hyperskill. Flask. Above the Rim API

Ссылка на проект:
https://hyperskill.org/projects/336?track=105

В проекте использованы:
- Flask
- SQLAlchemy
- Alembic

В проекте применяются практики:
- Разбивка приложения на контроллеры, сервисы, репозитории.
Разделение ответственности:
  - контроллер - прием, валидация, отправка данных в сервис, возврат ответа пользователю;
  - сервис - реализация бизнес-логики приложения, в том числе управление состоянием БД;
  - репозиторий - получение данных из БД и подготовка БД к изменениям, но без непосредственного изменения (так как состояние контролирует сервис).
- Dependency Injection и фабрики для прозрачности зависимостей и централизации инициализации;
- Unit-тесты и тесты API (в том числе на совместимость версий API);
- Миграции БД через Alembic;
- Версионированние API, с поддержкой обратной совместимости.