import logging;
from app.main import setup;
from datetime import datetime, timezone;

app = setup()
dt_now = datetime.now(timezone.utc).strftime("%d-%m-%Y_%H-%M-%S")
logging.basicConfig(level = logging.DEBUG, filename = f"logging/logger_{dt_now}.txt", filemode = "w")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4008, debug=True)