# Requirements

Install `poetry` Python package.

# Create database

`poetry run python manage.py migrate`

# Run in a testing enviroment

`poetry install && poetry run python manage.py runserver`

# Run in a production enviroment

`DEBUG=FALSE LC_ALL=en_US.utf-8 LANG=en_US.utf-8 SECRET_KEY="your_secret_key_here" screen bash -c "poetry run python manage.py collectstatic --noinput && poetry run gunicorn mysite.wsgi --log-file - -b unix:${HOME}/myproject.sock; tail -F /dev/null"`

And then configure nginx to reverse proxy ${HOME}/myproject.sock appropriately, e.g.:

    server {
        location = /favicon.ico { access_log off; log_not_found off; }
        location /staticfiles/ {
            root /home/your-username/worldcup;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/your-username/myproject.sock;
        }
    }
    server {
        listen 80 ;
        listen [::]:80 ;
        server_name websitename.com www.websitename.com;

    }
