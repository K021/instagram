FROM        k021/base
MAINTAINER  joo2theeon@gmail.com

ENV         LANG C.UTF-8
ENV         DJANGO_SETTINGS_MODULE config.settings

COPY        . /srv/app
RUN         /root/.pyenv/versions/app/bin/pip install -r \
            /srv/app/requirements.txt

# pyenv local 설정
WORKDIR     /srv/app
RUN         pyenv local app

# Nginx
RUN         cp /srv/app/.config/nginx/nginx.conf /etc/nginx/nginx.conf
RUN         cp /srv/app/.config/nginx/app.conf /etc/nginx/sites-available/
RUN         rm -rf /etc/nginx/sites-enabled/*
RUN         ln -sf /etc/nginx/sites-available/app.conf \
                    /etc/nginx/sites-enabled/app.conf

# uWSGI
RUN         mkdir -p /var/log/uwsgi/app

# manage.py
WORKDIR     /srv/app/instagram
RUN         /root/.pyenv/versions/app/bin/python manage.py collectstatic --noinput
RUN         /root/.pyenv/versions/app/bin/python manage.py migrate --noinput

# supervisor
RUN         cp /srv/app/.config/supervisor/* \
                /etc/supervisor/conf.d/
    # /etc/supervisor/conf.d/ 안에 있는 모든 conf 파일 실행
CMD         supervisord -n

EXPOSE      80