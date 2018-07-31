FROM ubuntu

# Update
RUN apt-get update && apt-get upgrade -y

# Install Mysql
RUN echo 'mysql-server-5.5 mysql-server/root_password password Sr19983700' | debconf-set-selections && \
	echo 'mysql-server-5.5 mysql-server/root_password_again password Sr19983700' | debconf-set-selections && \
	apt-get install -y mysql-server mysql-client

# Install Apache2 & PHP7
RUN apt-get -y install apache2 php7.0 libapache2-mod-php7.0 libapache2-mod-php php7.0-mysql php7.0-curl php7.0-json php7.0-cgi php7.0-gd php7.0-intl php-pear php7.0-imap php7.0-mcrypt  php7.0-pspell php7.0-recode php7.0-snmp php7.0-tidy php7.0-xmlrpc php7.0-xsl

# Apache Options
RUN sed -i 's/Options Indexes FollowSymLinks/Options FollowSymLinks/g' /etc/apache2/apache2.conf && echo '#Server Name\nServerName 127.0.0.1:80' >> /etc/apache2/apache2.conf && usermod -u 1000 www-data && rm /var/www/html/index.html && chown root:root /var/www/html

COPY ./html/ /var/www/html
COPY ./start.sh /root/
RUN chmod 740 /root/start.sh

ENTRYPOINT ["bash","/root/start.sh"]

EXPOSE 80