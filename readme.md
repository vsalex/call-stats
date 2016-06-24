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