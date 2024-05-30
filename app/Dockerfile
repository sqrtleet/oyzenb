FROM python:3.10

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 777

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "777", "--reload"]