Нужно будет в шаблоне по директории users/templates/users/results.html внутри тега scripts изменить ссылку base_url <br>
внутри telegram-bot start_bot.py и handlers.py тоже. <br>
Для того чтобы локально поднять сервер нужно зайти в папку где находится manage.py, т.е. основна папка проекта, написать python manage.py runserver. <br>
Чтобы установить все зависимости сперва желательно создать виртуальное окружение рядом с папкой проекта командой python -m venv <название_виртуального_окружения> <br>
Например, python -m venv myvenv, затем активировать его командой myvenv\scripts\acivate в windows, и source myvenv/bin/activate в mac/linux. <br>
Зайти в папку проекта, и написать pip install -r requirements.txt тогда установятся все зависимости. <br>
К базе данных, django подключается сама.
