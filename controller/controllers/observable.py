class Observable():
    subscribers = []

    def __init__(self):
        self.subscribers = []

    async def subscribe(self, websocket):
        try:
            self.subscribers.index(websocket)
        except ValueError:
            self.subscribers.append(websocket)

    async def unsubscribe(self, websocket):
        try:
            self.subscribers.remove(websocket)
        except ValueError:
            pass

    async def broadcast(self, result):
        for socket in self.subscribers:
            await socket.send_json(result)
