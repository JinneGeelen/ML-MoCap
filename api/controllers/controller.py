from controllers.observable import Observable
from db import get_db


class Controller(Observable):
    @property
    def db(self):
        return get_db()
