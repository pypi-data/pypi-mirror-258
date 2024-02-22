import json
import threading
import time

import tornado.ioloop
import tornado.web

# define("port", default=8114, help="run on the given port", type=int)


class TableSelectionHandler(tornado.web.RequestHandler):
    def post(self):
        data = self.request.body.decode("utf-8")
        print("data", data)
        json_data = json.loads(data)
        self.write(json.dumps(json_data))

    def options(self):
        self.set_status(200)
        self.finish()

    def set_default_headers(self):
        super().set_default_headers()
        # origin_url = self.request.headers.get('Origin')
        self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header(
            "Access-Control-Allow-Headers",
            "Content-Type,Content-Length,Authorization, Accept,X-Requested-With",
        )
        self.set_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        # self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Content-type", "application/json")


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/tableAreaSelect", TableSelectionHandler),
        ],
    )


_app = None
_thread = None


def start_interaction_app():
    global _app
    if _app is not None:
        print("app already started!")
        return
    _app = make_app()
    _app.listen(8114)
    tornado.ioloop.IOLoop.current().start()


def start_interaction_threaded():
    global _thread
    if _thread is not None:
        return
    _thread = threading.Thread(target=start_interaction_app)
    _thread.daemon = True
    _thread.start()


if __name__ == "__main__":
    start_interaction_threaded()
    while 1:
        time.time()
