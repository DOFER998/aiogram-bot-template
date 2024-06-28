# Aiogram bot template

This is a template to easily start developing an asynchronous bot for Telegram, using FastAPI to run the bot on a webhook and with a connected Telegram bot api

### Dependency installation
```shell
poetry install --no-root
```

### Specify environment variables in .env
```shell
TOKEN="154225:JjhJjllyfcchNjjkln"
RATE_LIMIT=0.7
WEBHOOK_URL="https://exemple.com"
API_ID=23523525
API_HASH="23r23sss2342245421aaaeessd55asa961eb"
REDIS_HOST="localhost"
REDIS_PORT=0000
REDIS_DB=0
TELEGRAM_BOT_API_URL="http://localhost:0000"
```

# Before you run it locally

## You will need to install `ngrok` on your PC, as Webhook for [Telegram](https://core.telegram.org/bots/webhooks) has a number of conditions that you will need to take into account when placing the bot on your hosting provider, then you need to run `ngrok` and specify it in `WEBHOOK_URL`

# Docker-compose
```shell
docker-compose up -d
```

# Project startup
```shell
poetry run fastapi run src/main.py
```

## Development

In further development will be added database `postgresql`, as well as I will gladly accept your `pull request` with the addition, improvement or correction of the functionality of this template
