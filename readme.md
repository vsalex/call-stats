# call-stats

Система анализа телефонных сообщение + фронтэнд Flask.

## Установка
```
mkdir call-stats && cd call-stats
git init
git remote add origin git@github.com:vsalex/call-stats.git
git pull origin master
```

## Зависимости
Python >= 3.4

```
pip install -r requirements.txt
```

## Тесты
Проект занял чуть больше времени, чем я рассчитывал, поэтому написал всего около 20 тестов, что мне не очень нравится, однако затягивать разработку ещё дальше сейчас мне кажется не правильным. Для продакшена тесты конечно стоит полностью дописать.
```
cd call-stats
python -m unittest discover tests
```

## Запуск
```
cd call-stats
python3.4 load_stats.py
```

## Описание
Скрипт будет запущен в бесконечном цикле. Будут постоянно анализироваться директории `input/call` и `input/duration` наналичие новых файлов с данными. Как только новый файл будет найден, он поступит дальше в работу, а сам будет переименован (к имени файла будет добавлено расширение `.ok`).

Чтобы из этого скрипта сделать полноценный сервис я бы использовал `upstart` например вот так:
```
start on filesystem
stop on shutdown

env logf="/var/log/call-stats.log"
script
    ~/call-stats/load_stats.conf >> $logf
end scipt
```

## Фронтэнд
Для отображения обработанной статистики использован Flask.
```
cd frontend_flask
python3.4 frontend_flask.py
```