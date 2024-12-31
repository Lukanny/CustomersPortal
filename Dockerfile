FROM python:3.12-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    && apt-get clean

# Instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos do projeto
COPY . .

RUN python manage.py collectstatic --noinput --verbosity 3

# Permissões para o entrypoint
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh"]
