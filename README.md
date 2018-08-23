Simple echo server written in python

to run simply build the docker image through docker compose and run it

```
docker-compose build
docker-compose up
```

you can also change the listening port through docker-compose config

or if you want to run the code outside a docker container, change the global variable `LISTEN_PORT` at the top of `main.py`

