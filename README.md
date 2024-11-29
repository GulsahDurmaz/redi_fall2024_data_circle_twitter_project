# US Election 2020 Twitter Sentiment Analysis Dashboard

This project is a Streamlit-based web application that analyzes tweets related to the 2020 US Presidential Election. It allows users to explore and visualize the popularity of candidates and sentiment across different states.

The project employs libraries such as streamlit, pandas, numpy, matplotlib, seaborn, plotly, pycountry, and plost. You can access the dashboard [on Streamlit](https://gulsahdurmaz-streamlit-app-twitter-project-main-pybjne.streamlit.app/). (Please use Google Chrome for a faster experience.)

## Dataset

To view the dashboard, you need to download the dataset used in this project.

You can download the dataset from [this link](https://www.kaggle.com/datasets/manchunhui/us-election-2020-tweets/data).

After downloading the dataset, follow these steps:

1. **Create a Folder for CSV Files:**
   - Inside your project directory, create a folder named `csv`.
   - Place the downloaded CSV files inside the `csv` folder.

## How to Run the Application

1. **Clone the Repository:**
   If you haven't already, clone the project repository:
   ```bash
   git clone https://github.com/YourUsername/redi_fall2024_data_circle_twitter_project.git
   cd redi_fall2024_data_circle_twitter_project
   ```
2. **Set up the Environment:**
   If you haven't already, clone the project repository:
   ```bash
   conda create --name twitter-project-env python=3.10
   conda activate twitter-project-env
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Streamlit Application:**
   ```bash
   streamlit run app.py
   ```

## Project Structure

```bash
.
├── app.py                       # Main Streamlit application
├── us_popularity_analysis.py    # US popularity analysis logic
├── imports.py                   # Importing necessary modules
├── data_cleaning.py             # Data cleaning functions
├── percentage_calculating.py    # Calculation logic for percentages
├── choropleth_map.py            # Choropleth map functions
├── requirements.txt             # Dependencies for the project
└── csv/                         # Folder where the dataset should be placed

```
