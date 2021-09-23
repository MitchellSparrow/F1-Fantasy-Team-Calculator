# F1 Fantasy Best Theoretical Team Application

The following repository is for an application to determine the statistically best F1 fantasy team to select for the next grand prix. There are two ways in which you can run this application, either as a flask app in your web browser (recommended) or by just running the python script. The application takes streaks into account and also provides the turbo driver recommendation. 

# Running the application

## 1.) Flask application (recommended)

Run the app.py file, which will then display the local URL of the application such as:

```http://127.0.0.1:8000/```

(This may be different on your computer. If there is an issue with the port number, you can change this)

Then navigate to the views page as follows:

```http://127.0.0.1:8000/views/```

You should then be able to use the web application as normal.

## 2.) Running the raw python script

Modify the COMBINED_COST_LIMIT in main.py to your maximum budget. Then run the following command.

```python main.py```

# Installation and Usage

## Install dependencies 

Make sure you have cloned the repository and are in the right directory. Then run the following command to install all the required dependencies.

```pip install -r requirements.txt```
