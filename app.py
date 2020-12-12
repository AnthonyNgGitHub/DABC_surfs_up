#  Import the dependency we need. This dependency will enable your code to access all that Flask has to offer.
from flask import Flask

# Create a new Flask app instance; name it as "app"
# "Instance" is a general term in programming to refer to a singular version of something

app = Flask(__name__)

# Variables with underscores before and after them are called magic methods in Python.
# This __name__ variable denotes the name of the current function. 
# You can use the __name__ variable to determine if your code is being run from the command line or if it has been imported into another piece of code. 

# Create Flask Routes

# First, we need to define the starting point, also known as the root.
## The forward slash inside of the app.route denotes that we want to put our data at the root of our routes. 
## The forward slash is commonly known as the highest level of hierarchy in any computer system.

# Next, create a function called hello_world(). 
## Whenever you make a route in Flask, you put the code you want in that specific route below @app.route()

@app.route('/')
def hello_world():
    return 'Hello world'