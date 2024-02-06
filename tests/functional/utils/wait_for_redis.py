import time

from redis import Redis

if __name__ == "__main__":
    redis_client = Redis(host="127.0.0.1", port=6379)
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
