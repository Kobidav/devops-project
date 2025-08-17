FROM python:3.12
COPY . /app
WORKDIR /app
RUN pip install -r req.txt
EXPOSE 8080
CMD ["python", "frontend_app.py"]