
docker rm -f nfl-fantasy
docker image rm -f gavthetallone/nfl-fantasy:latest
docker rm -f nfl-fantasy-db

# docker volume rm nfl-fantasy-volume
docker network rm nfl-fantasy-network

docker volume create nfl-fantasy-volume
docker network create nfl-fantasy-network

docker run -d -e MYSQL_ROOT_PASSWORD=squareroot -e MYSQL_DATABASE=data --network nfl-fantasy-network --name nfl-fantasy-db --mount source=nfl-fantasy-volume,target=/var/lib/mysql mysql

docker build -t gavthetallone/nfl-fantasy .

docker run -d --network nfl-fantasy-network --name nfl-fantasy -e DATABASE_URI=mysql+pymysql://root:squareroot@nfl-fantasy-db:3306/data gavthetallone/nfl-fantasy

docker run -d --network nfl-fantasy-network --name nfl-fantasy-proxy -p 80:80 --mount type=bind,source=$(pwd)/nginx/nginx.conf,target=/etc/nginx/nginx.conf nginx:alpine

# docker exec nfl-fantasy python3 create.py