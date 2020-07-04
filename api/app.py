'''
temporary entry point for the slack karma api.
'''

from api import app


if __name__ == '__main__':
    app.run(debug=True, port=4000)
