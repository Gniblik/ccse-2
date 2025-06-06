FROM python:3.10.17-alpine3.21

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

EXPOSE 5000 

CMD ["py", ".\manage.py", "runserver"]