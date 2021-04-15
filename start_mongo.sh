# You may need to specify the directory for the database
# The default (/data/db) is read-only for macs

# Creates the directory if it doesn't exist
[ ! -d "./data/db" ] && mkdir ./data; mkdir ./data/db

mongod --dbpath='./data/db' --bind_ip 127.0.0.1 --port 27018

# Access the cli by running 'mongo'
