# Telegram BOT для перевода голосовых сообщений в текст
## Чтобы протестировать его работу Вам необходимо:  
### Клонировать репозиторий  
```bash
git clone https://github.com/fulliam/stt_bot.git
```
#### Перейти в папку репозитория  
```bash
cd /stt_bot 
```
### Создать в корневом каталоге репозитория файл .env  
**Содержимое файла:**  
```bash
TOKEN = "your_token_here"
```
### Запустить сборку контейнерa  
```bash
docker build -t bot .
```
### Запустить контейнер  
```bash
docker run -d bot
```