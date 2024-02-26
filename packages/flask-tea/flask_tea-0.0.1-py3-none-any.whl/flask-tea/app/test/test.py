from app.test import api


@api.route('/')
def test():
    return 'Hello World'