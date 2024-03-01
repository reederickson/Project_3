import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template, jsonify
import base64
from io import BytesIO

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
        f"/sleep_and_stress <br/>" #reed route
        f"/jobs_and_sleep <br/>" #andrew route
        f"/health <br/>" #tom route
        f"/bryan_route <br/>" #bryan route

    )

def index():
    plots_html = generate_plot_html()
    return render_template('index.html', plots_html=plots_html)

###########Reed Route##############################

@app.route("/sleep_and_stress")
def analysis_route():
    result = perform_analysis()
    return f"Analysis Reesult: {result}"

##################################################

################Andrew Route#######################
@app.route("/jobs_and_sleep")
# Load your dataset
dataset_path = r"Resources\Sleep_health_and_lifestyle_dataset.csv" #switch to the engine rather than local machine
df = pd.read_csv(dataset_path)

# Generate HTML for each plot
def generate_plot_html():
    plots_html = []

    # Set a custom color palette
    sns.set_palette("husl")

    # 1. Sleep Duration/Quality vs Occupation
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Occupation', y='Sleep Duration', hue='Quality of Sleep')
    plt.title('Sleep Duration/Quality vs Occupation')
    plt.xlabel('Occupation')
    plt.ylabel('Sleep Duration')
    plt.xticks(rotation=45)
    plt.legend(title='Quality of Sleep', loc='upper right', fontsize='small')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    plots_html.append('<img src="data:image/png;base64,{}">'.format(img_str))
    plt.close()

    return plots_html
##################################################

##################Tom Route########################
@app.route("/health")
def analysis_route():
##################################################


#################Bryan Route#######################
@app.route("/bryan_route")
def analysis_route():
##################################################


if __name__ == '__main__':
    app.run(debug=True)