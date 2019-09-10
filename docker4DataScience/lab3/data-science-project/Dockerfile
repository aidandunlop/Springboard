FROM python:3.6.5-slim

WORKDIR /app

RUN pip --no-cache-dir install pandas jupyter

EXPOSE 8888

VOLUME /app

CMD ["jupyter", "notebook", "--ip='*'", "--port=8888", "--no-browser", "--allow-root"]
