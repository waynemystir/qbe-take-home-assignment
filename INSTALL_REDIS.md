## Install Redis

Install it on the command line:
```
sudo apt update
sudo apt install redis-server
```

Change the Redis config
```
sudo vi /etc/redis/redis.conf
```
Then uncomment the line `# supervised auto`.


Now start the Redis service:
```
sudo systemctl start redis-server
sudo systemctl enable redis-server
sudo systemctl status redis-server
```
The status command should show that `redis-server` is enabled and active (running).

Finally, verify that Redis is running:
```
redis-cli ping
```
This should return `PONG`.
