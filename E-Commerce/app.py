from flask import Flask

from config import Config
from setup import setup

import os

cfg: Config = Config()
app: Flask = Flask(
    'BRA7TAK_ECOMMERCE',
    template_folder=os.path.join(os.path.dirname(__file__), "./templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "./static"),
)
setup(app)

if __name__ == "__main__":
    app.run(
        debug= True,
        port= cfg.port
    )
