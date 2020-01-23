# app.py - a minimal flask api using flask_restful
import time
import redis

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
cache = redis.Redis(host='redis', port=6379)

class HelloWorld(Resource):
    def get_hit_count():
        retries = 5
        while True:
            try:
                return cache.incr('hits')
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)

    def get(self):
        count = self.get_hit_count()
        return 'Whale, Hello there for the {} time!!'.format(count)

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
