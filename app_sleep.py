import numpy as np
import seaborn as sns

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
###################
# create and save database
execfile("Setup and Organization/Database Setup.py")
# database setup
engine = create_engine("sqlite:///Resources/database.sqlite")
conn=engine.connect()

# reflect an existing database into a new model
base= automap_base()
# reflect the tables
base.prepare(engine,reflect=True)

# Flask Setup
app = Flask(__name__)

# Flask Routs
@app.route("/")
def Welcome():
    # available api routes
    return(
        f"Available Routs: <br/>"
        f"/sleep_and_stress <br/>"
        f"/api/v1.0/route2 <br/>"
    )

from reed import perform_analysis
@app.route("/sleep_and_stress")
def analysis_route():
    result = perform_analysis()
    return f"Analysis Reesult: {result}"

if __name__ == "__main__":
    app.run(debug=True)
    #query all whatevers
    session.close()
