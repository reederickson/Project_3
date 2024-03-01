import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from flask import Flask, render_template
import base64
from io import BytesIO

app = Flask(__name__)

# Load your dataset
dataset_path = r"C:\Users\AKKem\OneDrive\Desktop\Project_3\Resources\Sleep_health_and_lifestyle_dataset.csv"
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

@app.route('/')
def index():
    plots_html = generate_plot_html()
    return render_template('index.html', plots_html=plots_html)

if __name__ == '__main__':
    app.run(debug=True)
