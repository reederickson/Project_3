import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

import ipywidgets as widgets

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
from IPython.display import display
###################
# create and save database

################### UNCOMMENT THIS BEFORE SUBMITTING!!!!!!
# execfile("Setup and Organization/Database Setup.py")
###################

# database setup
engine = create_engine("sqlite:///Resources/database.sqlite")
conn=engine.connect()

# reflect an existing database into a new model
base= automap_base()
# reflect the tables
base.prepare(autoload_with = engine)

# Flask Setup
app = Flask(__name__)

# Flask Routs
@app.route("/")
def Welcome():
    # available api routes
    return(
        f"Available Routes: <br/>"
        f"/api/v1.0/route1 <br/>"
        f"/api/v1.0/route2 <br/>"
    )
@app.route("/api/v1.0/route1")
def route1():
    data = pd.read_sql(
    f"SELECT * FROM person AS p \
        INNER JOIN occupation AS o ON o.id = p.occupation_id\
        INNER JOIN gender AS g ON p.gender_id = g.id\
        INNER JOIN health AS h ON h.person_id = p.id\
        INNER JOIN bmi AS b ON b.id = h.bmi_id",
        conn
    )

    # Possible numerical columns to choose instead of just 'age'

    dd = widgets.Dropdown(
        options = {"Age": "age", "Stress Level": "stress_level", "Heart Rate": "heart_rate", "Systolic": "systolic", "Diastolic": "diastolic"},
        value = "age",
        description = "Category"
    )

    # genders = data["gender_name"].unique().tolist()

    dd1 = widgets.Dropdown(
        options = ["All", "Male", "Female"],
        value = "All",
        description = "Gender"
    )

    # bmis = data["bmi_name"].unique().tolist()

    dd2 = widgets.Dropdown(
        options = ["All", "Normal", "Overweight", "Obese"],
        value = "All",
        description = "BMI Type"
    )

    def draw_plot(column, item1, item2):    
        plots_html = []
        
        if (item1 == "All"):
            if (item2 == "All"):
                mask = (data["gender_name"].isin(["Male", "Female"])) & (data["bmi_name"].isin(["Normal", "Overweight", "Obese"]))
            else:
                mask = (data["gender_name"].isin(["Male", "Female"])) & (data["bmi_name"] == item2)
        else:
            if (item2 == "All"):
                mask = (data["gender_name"] == item1) & (data["bmi_name"].isin(["Normal", "Overweight", "Obese"]))
            else:
                mask = (data["gender_name"] == item1) & (data["bmi_name"] == item2)
        #sns.set_theme(style = "ticks")
        f, ax = plt.subplots(figsize = (8, 6))
        sns.boxplot(x = data.loc[mask, column],
                    y = data.loc[mask, "occupation_name"], 
                    hue = data["occupation_name"],
                    palette = "Paired",
                    width = 0.6,
                    legend = False
                    )
        sns.stripplot(
            x = data.loc[mask, column],
            y = data.loc[mask, "occupation_name"],
            color = "black",
            dodge = True,
            edgecolor = "black"
        )

        sns.set_style(rc = {"axes.facecolor": "lightyellow"})

        column_proper = column.replace("_", " ").title()
        ax.set_xlabel(column_proper, fontsize = 15)
        ax.set_ylabel("Occupation", fontsize = 15)
        plt.title(f"Distribution of {column_proper} per Occupation ({item1})", fontsize = 18)

        ddbox = widgets.HBox([dd, dd1, dd2])

        out1 = widgets.interactive_output(draw_plot, {"column": dd, "item1": dd1, "item2": dd2})
        
        return display(ddbox, out1)



if __name__ == '__main__':
    app.run(debug=True)
