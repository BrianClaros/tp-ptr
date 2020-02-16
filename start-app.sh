#!/bin/bash
killall php >/dev/null 2>&1
killall python3 >/dev/null 2>&1
echo "Iniciando servidor"
ip=$(ip -o route get to 8.8.8.8 | sed -n 's/.*src \([0-9.]\+\).*/\1/p')
php -S $ip:8080 >/dev/null 2>&1 &
echo "Servidor corriendo en $ip:8080"
