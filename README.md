# qrAutomation

Проект для автоматизации расписаний уборки. <br>
Во многих компаниях, поле уборки кабинета, уборщики заполняют график уборок, на это уходит какое-то количество времени, также на это требутся бумага, эти отчёты надо сохранять. <br>
Чтобы упростить этот процесс и был создан этот проект. <br>
Запустив платформу, начальник добавляет все кабинеты и уборщики могут создать расписание за 5 секунд.<br>
А чтобы каждый раз вручную не указывать номер кабинета, можно распечатать qr код, наведя на него камеру, откроется страница с уже выбранным кабинетом, останется лишь нажать на кнопку "Создать".<br>
Список всех расписаний уборок находится на главной странице. <br>
Помимо всех этих возможностей, можно также удалить расписание, удалить кабинет, посмотреть полный список сотрудников, посмотреть логи.<br>
Имеется кабинет, на котором можно посмотреть статистику по сайту(/dashboard, создано с помощью Flask-MonitoringDashboard)

<br>

## Deploy locally:

Клонируйте этот репозиторий и перейдите в папку с проектом:
```
git clone https://github.com/Ryize/qrAutomation.git
cd qrAutomation
```

Установить зависимости:
```
pip3 install -r requirements.txt
```
> Перейдите в файл config.py и настройте конфиг CustomConfig(При необходимости и другие)

> Убедитесь, что порт 8000 не занят

Выполните миграции:
```
flask db upgrade
```

Запустите проект:
```
python3 app.py
```

> В проекте используются Flask расширения(<a href='https://github.com/akhilharihar/Flask-Maintenance'>Flask-Maintenance</a>, <a href='http://flask-monitoringdashboard.readthedocs.io'>Flask-MonitoringDashboard</a>). Если вы не знаете как ими пользоваться, ознакомьтесь с документацией

> Проект распространяется под лицензией MIT