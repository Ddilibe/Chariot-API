from functools import wraps
from flask import Flask, request

app = Flask(__name__)

def my_decorator(arg):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"The argument passed to the decorator is: {arg}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/my-route/<arg>')
@my_decorator(arg=arg)
def my_route(arg):
    return f"The argument passed to the route is: {arg}"

if __name__ == '__main__':
    app.run(debug=True)
