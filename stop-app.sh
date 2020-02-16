#!/bin/bash
echo "Bajando app"
killall php >/dev/null 2>&1
echo "Bajando eliminando sesion de la cámara"
killall python3 >/dev/null 2>&1
echo "Se paró completamente la aplicación"
