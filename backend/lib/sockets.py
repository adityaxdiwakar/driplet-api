import websockets, functools, asyncio, subprocess, zmq, threading, time, sys, os, json, tornado.web, tornado.httpserver, tornado.ioloop, tornado.websocket, tornado.options

class ChannelHandler(tornado.websocket.WebSocketHandler):

    def on_open(self):
        pass

    def on_message(self, message):
        try:
            request = json.loads(message)
        except:
            self.write_message("Malformed request.")
            return
        
        if "creds" not in request or "data" not in request:
            self.write_message("Malformed request.")
            return

        if request['creds']['id'] == "u2852334499":
            self.write_message("Authentication was successful.")
            threading.Thread(target=self.bind, args=[request['data']]).start()
        else:
            self.write_message(json.dumps({
                "message":"Authentication failed",
                "code":401
            }))

    def bind(self, service):
        asyncio.set_event_loop(asyncio.new_event_loop())
        p = subprocess.Popen(service['log_command'], stdout=subprocess.PIPE, bufsize=1, shell=True)
        while True:
            self.write_message(p.stdout.readline())

def main():
    asyncio.set_event_loop(asyncio.new_event_loop())
    # Create tornado application and supply URL routes
    application = tornado.web.Application([
        (r'/', ChannelHandler)
    ])

    # Setup HTTP Server
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(3142, "127.0.0.1")

    # Start IO/Event loop
    tornado.ioloop.IOLoop.instance().start()

def run():
    thread = threading.Thread(target=main, name="socket manager")
    thread.start()