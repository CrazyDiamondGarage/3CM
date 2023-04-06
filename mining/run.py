
import time
import sys
import hashlib
import multiprocessing
# import threading
# import curses

# import websocket
import web3
# import rel
# import eth_hash.auto

import tornado.ioloop
import tornado.gen
import tornado.websocket


def pow(conn):
    start = 0
    try:
        d = 10
        sleep = True
        while True:
            if conn.poll():
                m = conn.recv()
                if m[0] == 'START':
                    print('start')
                    start = m[1]
                    sleep = False
                elif m[0] == 'STOP':
                    sleep = True

            if sleep:
                time.sleep(1)
                print('sleep')
                continue

            # t0 = time.time()
            nonce = start
            for nonce in range(start, start+100000):
                if nonce % 10000 == 0:
                    print(nonce)
                h = hashlib.sha256(str(nonce).encode('utf8')).hexdigest()
                if h.startswith('0'*d):
                    # print(h, nonce)
                    conn.send(['FOUND', nonce])

            conn.send(['DONE', start, start+100000])
            sleep = True
    except:
        pass


current_mining = None
next_mining = []


class Client:
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.ws = None
        self.connect()
        tornado.ioloop.PeriodicCallback(self.keep_alive, 20000).start()
        tornado.ioloop.PeriodicCallback(self.pool, 500).start()
        self.ioloop.start()

    @tornado.gen.coroutine
    def connect(self):
        print("trying to connect")
        try:
            self.ws = yield tornado.websocket.websocket_connect(self.url)
        except Exception:
            print("connection error")
        else:
            print("connected")
            self.run()

    @tornado.gen.coroutine
    def run(self):
        global current_mining
        global next_mining
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                print("connection closed")
                self.ws = None
                break
            else:
                print(msg)
                conn.send(['START', 0])

    def keep_alive(self):
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep alive")

    def pool(self):
        for conn in cs:
            if conn.poll(0.1):
                m = conn.recv()
                if m[0] == 'DONE':
                    print(m)

                elif m[0] == 'FOUND':
                    print(m)

ps = []
cs = []
if __name__ == "__main__":
    conn, child_conn = multiprocessing.Pipe()
    process = multiprocessing.Process(target=pow, args=(child_conn,))
    ps.append(process)
    cs.append(conn)
    process.start()
    client = Client("ws://127.0.0.1:7000/pool", 5)
