# SPDX-License-Identifier: MIT

import redis as Redis

from drain3.persistence_handler import PersistenceHandler


class RedisPersistence(PersistenceHandler):
    def __init__(self, redis_key, redis_host='localhost', redis_port=6379, redis_db=0, redis_pass=None, is_ssl=False, redis=None):
        self.redis_key = redis_key

        if redis is not None:
            self.r = redis
        else:
            self.r = Redis(host=redis_host,
                                port=redis_port,
                                db=redis_db,
                                password=redis_pass,
                                ssl=is_ssl)

    def save_state(self, state):
        self.r.set(self.redis_key, state)

    def load_state(self):
        return self.r.get(self.redis_key)


# persistance = RedisPersistence(
#     redis= Redis(
#         host='localhost',
#         port=6379,
#         db=0,
#         password=None,
#         ssl=False
#     ),
#     redis_key='drain3'
# )