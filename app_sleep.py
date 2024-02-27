import numpy as np
import seaborn as sns

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
###################
# create and save database
execfile("Database Setup.py")
# database setup
engine = create_engine("sqlite:///database.sqlite")
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
        f"/api/v1.0/route1 <br/>"
        f"/api/v1.0/route2 <br/>"
    )
@app.route("/api/v1.0/route1")
def ():
    session= Session(engine)
    #query all whatevers
    session.close()
