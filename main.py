from entrypoint.api import router
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8080), router)
    http_server.serve_forever()
