FROM python

WORKDIR /root/HyperGames

COPY . .

RUN pip3 install --upgrade pip setuptools

RUN pip3 install -U -r requirements.txt

CMD ["python3","-m","HyperGames"]
