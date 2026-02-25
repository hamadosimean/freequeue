#! /bin/sh

# deploying to production
clear
echo "Deploying to production..."
docker compose down
docker compose up --build -d 


