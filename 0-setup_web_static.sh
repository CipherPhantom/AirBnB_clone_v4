#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static.

if ! dpkg -l | grep -q "nginx"; then
	apt-get -y update
	apt-get -y install nginx
fi

web_static="/data/web_static"
mkdir -p "$web_static/shared/"
mkdir -p "$web_static/releases/test/"
touch "$web_static/releases/test/index.html"
printf "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
" > "$web_static/releases/test/index.html"

rm -f "$web_static/current"
ln -s "$web_static/releases/test/" "$web_static/current"

chown -R ubuntu:ubuntu /data/

static_url="\n\tlocation /hbnb_static {\n\t\t alias $web_static/current/;\n\t}\n"
nginx_config="/etc/nginx/sites-available/default"
sed -i "/^}$/i\ $static_url" "$nginx_config" 

service nginx restart
