FROM python

# Create app directory
WORKDIR /usr/src/app

COPY requirements.* ./

RUN pip install -r requirements.txt && pip install -r requirements.bot.txt

# Bundle app source
COPY . .

CMD [ "sh", "-c", "python -m discord_bot" ]
