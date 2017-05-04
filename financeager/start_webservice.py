#!/usr/bin/env python
from flask import Flask
from flask_restful import Api

from financeager.config import CONFIG
from financeager.resources import (PeriodsResource, PeriodResource,
        EntryResource, ShutdownResource)

app = Flask(__name__)
api = Api(app)

api.add_resource(PeriodsResource, "/financeager/periods")
api.add_resource(PeriodResource, "/financeager/periods/<period_name>")
api.add_resource(EntryResource,
    "/financeager/periods/<period_name>/<table_name>/<eid>")
api.add_resource(ShutdownResource, "/financeager/stop")

if __name__ == "__main__":
    try:
        app.run(debug=CONFIG["SERVICE:FLASK"].getboolean("debug"))
    except OSError as e:
        # socket binding: address already in use
        print(e)
