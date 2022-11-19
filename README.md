# F1 Fantasy Best Theoretical Team Application

![alt text](https://cdn.sanity.io/images/xbn4zmfs/production/1ead0d23cb4778e491d8d5ccb17ba776c586d372-5909x2616.png)

The following repository is for an application to determine the statistically best F1 fantasy team to select for the next grand prix. There are two ways in which you can run this application, either as a flask app in your web browser (recommended) or by just running the python script. The application takes streaks into account and also provides the turbo driver recommendation.

Want to see the application live in action? You can find it [here](http://www.f1fantasyanalysis.com/)!

# Running the application

## 1.) Flask application (recommended)

There are a few ways in which you can run the flask application. These are covered below.

### 1.1) Online

The application is currently live and available to use at the following link:

http://www.f1fantasyanalysis.com/

### 1.2) Locally

Run the following command in your terminal:

`python main.py`

This will then display the local URL of the application such as:

`http://127.0.0.1:6000/`

(This may be different on your computer. If there is an issue with the port number, you can change this)

## 2.) Running the raw python script

Modify the COMBINED_COST_LIMIT in main.py to your maximum budget. Then run the following command.

`python main.py`

# Installation and Usage

## Install dependencies

Make sure you have cloned the repository and are in the right directory. Then run the following command to install all the required dependencies.

`pip install -r requirements.txt`

# References

The HTML page styling was built from a pre existing and free template called Forty by HTML5. This template can be found at the following link:

https://html5up.net/forty
