# ![db](https://github.com/DrozdovVladimir1/petprojects/assets/113205862/42eca3e9-b69d-4cd0-9951-d1d83cb73c04) DB_assist бот - это
Телеграм бот, который автоматически собирает (парсит) и присылает информацию по последним матчам
## Используемые технологии
+ [My Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
+ [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
+ Python v.3.10.2 :snake:
## Как использовать бота
1. Юзер присылает свою ссылку на dotabuff.com. Важно!!! Профиль должен быть **НЕ скрытым**
Команда ``/setlink <link>`` 
2. Юзер "подписывается" на обновления, после чего ему <u>автоматически</u> будет присылаться информация о недавних играх. При первом использовании юзер сразу получит информацию о 50 последних играх
3. При необходимости можно "отписаться" от обновлений при помощи команды ``/stop_update``
4. Текущий статус можно посмотреть при помощи команды ``/status``

## Как это работает
- При использовании команды ``/setlink <link>`` за юзером (его user_id в телеграме) сохраняется присланная ссылка в формате JSON
- Когда юзер "подписывается" на обновления, то каждые 60 секунд происходит парсинг страницы с матчами юзера, откуда собирается следующая информация:
![image](https://github.com/DrozdovVladimir1/petprojects/assets/113205862/2bbc9168-1221-4898-8d58-7055b35eb1b9)
- Эта информация собирается в компактный вид и отправляется юзеру
  
## Misc.
- На одного юзера приходится 1440 запросов в сутки, что может привести к потенциальной блокировки бота
- Сайт не предоставляет API, поэтому и появилась идея сделать бота