from websockets.sync.server import serve, ServerConnection

from services.websocket.data_transfer import message_handler

class WebsocketServer:
    server = None

    def _websocket_reciver(self, websocket:ServerConnection):
        for message in websocket:
            result = message_handler(message)
            if isinstance(result, str):
                websocket.send(result)
            elif result == 2:
                self.server.shutdown()
            elif result == 1:
                pass
            elif result == 0:
                websocket.close()

    def start_websocket_server(self, ip:str, port:int, ssl_context=None):
        with serve(self._websocket_reciver, ip, port, ssl=ssl_context) as _server:
            self.server = _server
            _server.serve_forever()
            