FROM nginx:stable

RUN rm /etc/nginx/conf.d/default.conf

COPY ./default.conf /etc/nginx/conf.d/default.conf

RUN echo "worker_processes auto;" > /etc/nginx/nginx.conf

# Expor a porta 80
EXPOSE 80 443

# Iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]
