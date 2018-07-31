#!/bin/bash
echo '[*] Start service'
service mysql start && service apache2 start;
echo '[+] Service start done.'
/bin/bash