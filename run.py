import logging;
from app.main import setup;

app = setup()
logging.basicConfig(level = logging.DEBUG, filename = "logging/logger.txt", filemode = "w")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4008, debug=True)