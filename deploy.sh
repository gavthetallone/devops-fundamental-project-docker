
docker rm -f nfl-fantasy
docker image rm -f gavthetallone/nfl-fantasy:latest
docker rm -f nfl-fantasy-db
docker network rm nfl-fantasy-network

docker network create nfl-fantasy-network

docker run -d -e MYSQL_ROOT_PASSWORD=squareroot -e MYSQL_DATABASE=data --network nfl-fantasy-network --name nfl-fantasy-db mysql

docker build -t gavthetallone/nfl-fantasy .

docker run -d -p 5000:5000 --network nfl-fantasy-network --name nfl-fantasy -e DATABASE_URI=mysql+pymysql://root:squareroot@nfl-fantasy-db:3306/data gavthetallone/nfl-fantasy

docker exec nfl-fantasy python3 create.py