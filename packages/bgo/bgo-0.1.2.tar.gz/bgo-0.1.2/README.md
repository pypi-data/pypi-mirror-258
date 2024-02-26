<p align="center">
    <img src=https://github.com/Alchemmist/weather-demo/blob/main/media/logo.jpg width=500/>
    <br />
    <a href="https://t.me/alchemmist" alt="link to telegram account">
        <img alt="Static Badge" src="https://img.shields.io/badge/my%20Telegram-blue?style=for-the-badge&logo=telegram&logoColor=white&link=https%3A%2F%2Ft.me%2Falchemmist" />
    <a />
    <br />
    <a href="https://python.org" alt="Contributors">
        <img alt="Static Badge" src="https://img.shields.io/badge/python%20%F0%9F%90%8D-3.12-blue?style=for-the-badge&link=https%3A%2F%2Fpython.org" />
    <a />
    <a href="https://github.com/aaronrausch/ascii-weather" alt="Contributors">
        <img alt="Static Badge" src="https://img.shields.io/badge/thanks_for_ascii_art-yellow?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Faaronrausch%2Fascii-weather%2F" />
    <a />
    <br />
    <b>Это минималистичная утилита для просмтора погоды прямо в терминале.</b>
</p>


# Документация

[1. Описание](#about)

[2. Пример](#example)

[3. Использование](#usage)

[4. Установка](#install)


<a name="about"/>

# 1. Описание проекта

 weather-cli - это консаольная утилита для просмтотра погоды на данный момент, а также прогноза на блтжайшее время. Программа обладает приятными и удобным интерфейсов взаимодействия. Утилита работает с двумя API:
 
 - OpenWeather (для получения данных о погоде)

 - IpInfo (для расопознования место положени по IP-адрессу

 Исходный код программы напсан на языке программирования Python, с использованием библиотеки rich для наглядного отображения данных. 

<a name="example"/>

# 2. Пример 

https://github.com/Alchemmist/weather-cli/assets/104511335/bbe5826d-8f14-481a-b119-3d7684e69fc5


<a name="usage" />

 # 2. Использование
 
 У утилиты есть две главные команды: 
 ```shell
python weather.py now
python weather.py forecast
```

`now` - показывает погоду на текущий момет, в следующем формате:
```
╭─────────────────────── Москва 🌤  ────────────────────────╮
│                                                           │
│  ( )()_  05:18 AM         Пасмурно                        │
│ (      ) температура: 0°C ощущается как: -5°C             │
│  (  )()  влажность: 91%   источник: OpenWeather           │
│                                                           │
╰───────────────────────────────────────────────────────────╯
```

`forecast` - показывает прогноз погоды в видет таблицы. Есть возможность указать количество дней прогноза (от 1 до 5):
```
python weather.py forecast -d 3
```
А так же можно посмотреть более детальный прогноз, установив фалг `--with-time`:
```
python weather.py forecast -d 2 --with-time
```

Кроме того для обоих команд (now и forecast) можно передавать следоющие флаги:

- `--high-precision` флаг позволяющий увидеть максимально точные значения всех парметров, без округления
- `--full-info` флаг лишающий вас, удобного и наглядного отображения, но заато показывающий абсолютно всю информация о погоде, получаемую из API

Вы можмет в любой момент ознакомиться с актуальной документацией по использования, с помощью команды:
```shell
python src/weather --help
```
Это комнда покажет вам такой (или почти такой) перечень со всеми возможными параметрами:
```
usage: weather [-h] [-d {1,2,3,4,5}] [--high-precision] [--full-info] [--with-time] [command]

positional arguments:
  command               a command showing the forecast for different time periods

options:
  -h, --help            show this help message and exit
  -d {1,2,3,4,5}, --days {1,2,3,4,5}
                        set how long the forecast you want to see (from 1 to 5 days)
  --high-precision      use this field for show value wit max precision
  --full-info           use this field for show all information
  --with-time           use this field for show forecast with time
```

<a name="install" />

# 3. Уставновка

Чтобы запусить проект локально выполнитье следющие команды:
```shell
git clone git@github.com:Alchemmist/weather-cli.git
cd weather-cli
python -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

А затем попробуйте запустить:
```shell
python src/weather -h
```

Если никаких ошибок не произошло, то поздравляю, вы успешно запустили проект в локальный среде. Теперь, для удобства использования, вы можете добавить файл `src/weather` в перменную окружения PATH и отредактировать shebang-строку в начали того же файла, прописав там путь до вашей папке venv и до интерпретатора python в ней. 

Если это сделать получилось, можете запусать утилиту одной командой:
```shell
weather
```

Приятного использования!
