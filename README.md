# Car Prediction - Data Science Project

A car dealership company hired us to solve the following problem: Where is the best place to buy cars for resale and what are the best cars to buy for the highest profit?

**This hypothetical problem created just for the project**

### Requirements to run my project:
-----------
- Python 3.10+
- Pandas
- Numpy
- Plotly
- Category-Encoders
- Scikit-Learn
- Streamlit (optional)

``` bash
$ pip install -r requirements.txt
```
and

``` bash
$ source setup.sh
```

### You can run with docker:
-----------
``` bash
docker pull renatodev4/data-science-car-prediction
```

Using this command a docker container will be started with the project running with streamlit in your local machine.

### To start the project, run:
------------

``` bash
$ python -u "your_user/src/data/main.py'
```

### If you want to do webscraping for more data:

``` bash
$ python -u "your_user/src/features/webscraping.py'
```

Webscraping is done through the website www.icarros.com.br, in order to scrape it you will need to make requests through a proxy or through an API like the one I used (Zenrows)

If not, the site will block your IP after a few requests.


Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │
    │
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download and generate data
    │   │   └── main.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   ├── clean_data.py
    │   │   ├── config.py
    │   │   ├── webscraping.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions 
    │   │   ├── train_model.py
    │   │   ├── modelo_predicao_app.py
    │   │
    │   ├── visualization   <- Scripts to check dataframe data in streamlit (Web App)
    │   │   ├── conclusao_projeto.py
    │   │   ├── dashboard.py
    │   │   ├── estatistica.py
    │   │   ├── estudo_de_dados.py
    │   │   ├── problemas_resolvido.py
    └───── setup.sh <- Create the environment variable to run the project

## Made by:

Project made by **Renato Moraes** for his portfolio.<br>
You can check the Data Science project running at: https://projeto-renato-datascience-veiculos.streamlit.app/


--------
