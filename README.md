# Jasmin Web Panel
<p>
	<a href="https://travis-ci.org/101t/jasmin-web-panel"><img src="https://travis-ci.org/101t/jasmin-web-panel.svg?branch=master" alt="travis-ci"></a>
</p>

Jasmin SMS Web Interface for [Jasmin SMS Gateway](https://github.com/jookies/jasmin)

### Table Of Contents:

1. [Installing and Deployment](https://github.com/101t/jasmin-web-panel#installing-and-deployment)
    * [Installation](https://github.com/101t/jasmin-web-panel#installation)
    * [Deployment with NGiNX and Systemd](https://github.com/101t/jasmin-web-panel#deployment-with-nginx-and-systemd)
2. [Release Notes](https://github.com/101t/jasmin-web-panel#release-notes)
3. [Usage](https://github.com/101t/jasmin-web-panel#usage)
4. [Support Developer](https://github.com/101t/jasmin-web-panel#support-developer)
5. [Contact Us](https://github.com/101t/jasmin-web-panel#contact-us)

## Installing and Deployment

Before starting please make sure you have installed and running [Jasmin SMS Gateway](http://docs.jasminsms.com/en/latest/installation/index.html) on your server.

### Installation

Download and Extract folder We recommended installing python dependencies in `virtualenv`

Install dependencies:

> This version using `python >= 3.5` make sure you have installed on your system.

go to `jasmin-web-panel/` and run

```sh
cd jasmin-web-panel/
pip install -r requirements.txt
cp Sample.env .env
```
Preparing your `database` by running migrate commads:
```sh
python deploy.py migrate
python deploy.py load_new # to load new user
python deploy.py collectstatic
```
These commands used in production server, also you may edit **Jasmin SMS Gateway** credential connection
```ini
TELNET_HOST = 127.0.0.1
TELNET_PORT = 8990
TELNET_USERNAME = jcliadmin
TELNET_PW = jclipwd
TELNET_TIMEOUT = 10
```
for production make sure `DEBUG=False` in `.env` file to ensure security.
You may run project manually
```sh
python deploy.py runserver
```

### Deployment with `NGiNX and Systemd`

> Make sure you have installed `gunicorn` using `pip`.

Navigate to `/etc/systemd/system` and create new service called `jasmin-web.service`

```ini
[Unit]
Description=Jasmin Web Panel
Requires=postgresql.service
After=network.target postgresql.service

[Service]
Type=simple
SyslogIdentifier=jasminwebpanel
PermissionsStartOnly=true
User=username
Group=username
Environment="DJANGO_SETTINGS_MODULE=config.settings.pro"
WorkingDirectory=/opt/jasmin-web-panel
ExecStart=/opt/jasmin-web-panel/env/bin/gunicorn --bind 127.0.0.1:8000 config.wsgi -w 3 --timeout=120 --log-level=error
StandardOutput=file:/opt/jasmin-web-panel/logs/gunicorn.log
StandardError=file:/opt/jasmin-web-panel/logs/gunicorn.log
StandardOutput=journal+console
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
Reload systemd

```sh
sudo systemctl daemon-reload
```
Now, you can do:
```sh
sudo systemctl enable jasmin-web.service
sudo systemctl start jasmin-web.service
```
To ensure web app running without issue:
```sh
sudo systemctl status jasmin-web.service
```
For NGiNX go to `/etc/nginx/sites-availiable` and create new file `jasmin_web`

```nginx
upstream jasmin_web{
    server 127.0.0.1:8000;
}
server {
    listen 80;
    charset utf-8;
    server_name example.com www.example.com;
    client_body_timeout 500;
    client_header_timeout 500;
    keepalive_timeout 500 500;
    send_timeout 30;
    access_log /var/log/nginx/jasmin_web_access.log combined;
    error_log /var/log/nginx/jasmin_web_error.log;

    location / {
        proxy_pass http://jasmin_web;
        proxy_http_version 1.1;
        proxy_read_timeout 86400;
        proxy_redirect     off;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_max_temp_file_size 1600m;
        proxy_buffering off;
        proxy_request_buffering on;
        client_max_body_size 20M;
        client_body_buffer_size  256K;
    }

    location ^~ /media/ {
        root /opt/jasmin-web-panel/public/;
        add_header Accept-Ranges bytes;
    }
    location ^~ /static/ {
        root /opt/jasmin-web-panel/public/;
        add_header Pragma public;
        add_header Cache-Control "public";
        expires 30d;
    }
}
```
> Note: Don't forget to replace `example.com` with your real domain

Once you are done, test and restart the Nginx Service with:
```sh
ln -s /etc/nginx/sites-availiable/jasmin_web /etc/nginx/site-enabled/jasmin_web
sudo nginx -t
sudo nginx -s reload 
# or sudo service nginx restart 
# or sudo systemctl restart nginx
```

### Login information:
```shell
Username: admin
Password: secret
```
> Note: Please change password to avoid security issue

## Release Notes

What's new in version 2.0.0
1. UI Improved, jQuery Fixed, jQuery Validation added.
2. Backend fixing, upgrade to python3 and fresh Django version.
3. Telnet connector fixing.
4. Deployment made easier.
5. Fixing common connection issues.
6. Simple dashboard initialized.
7. User Profile, Change Password, Add Avatar.
8. Activity Log, to log your usage.

What's new in version 2.0.1
1. Adding **Submit Log** report (DLR report)
 
What's new in version 2.0.2
1. Adding FailOverRouter supports to MT / MO Router

**TODO:** bug fixes, adding new features

## Usage

This application built as web interface to manage Jasmin SMS Gateway, it is an open source for free and commercial purpose.

## Support Developer

We accept paid support for installation and customization, if you want to help us improve it further, you may support us with a tip, we appreciate all contributions!

## Contact Us

For business inquiries: [tarek.it.eng@gmail.com](mailto:tarek.it.eng@gmail.com), Join Telegram Channel: [https://t.me/jasminwebpanel](https://t.me/jasminwebpanel), all suggestion and questions are welcomed.
