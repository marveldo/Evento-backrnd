FROM nginx:1.21.3-alpine

ARG CONFIG_FILE=nginx.prod.conf.template


WORKDIR /app


RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/nginx.conf

RUN mkdir /etc/nginx/templates

COPY $CONFIG_FILE /etc/nginx/templates


RUN chgrp -R 0 /etc/nginx/conf.d && \
    chmod -R g=u /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]