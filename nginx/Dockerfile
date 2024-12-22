# Usar a imagem oficial do Nginx
FROM nginx:latest

# Remover configuração padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiar a configuração personalizada do Nginx
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# Copiar arquivos estáticos e de mídia do Django (opcional, pode ser montado como volume)
COPY ./static /app/static

# (Opcional) Copiar certificados SSL
# COPY ./nginx/ssl /etc/nginx/ssl

# Expor a porta 80
EXPOSE 80

# Iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]
