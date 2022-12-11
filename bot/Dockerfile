
# Base Image for builder
FROM python:3.9 as builder

# Install Requirements
COPY requirements.txt /
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# Build the bot image
FROM python:3.9

# Create directory for the bot user
RUN mkdir -p /home/bot

# Create the bot user
RUN groupadd bot && useradd -g bot bot

# Create the home directory
ENV HOME=/home/bot
ENV APP_HOME=/home/bot/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Install Requirements
COPY --from=builder /wheels /wheels
COPY --from=builder requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME

RUN chown -R bot:bot $APP_HOME

USER bot

ENTRYPOINT bash