#!/bin/sh

cd /app
gunicorn index:server -b :8050 -w 12

