import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

# Import the Tkinter library for GUI development
import tkinter as tk
from tkinter import *


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/mydatabase2.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# print(Base.classes.keys())

# Save references to each table
recipes=Base.classes.chicken_recipe_data
co2=Base.classes.co2_data

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/all_recipes"
    )

@app.route("/api/v1.0/all_recipes")
def all_recipes():
    # Create our session (link) from Python to the DB
    session=Session(engine)
    sel=[recipes.recipe_name, recipes.cuisine_type, co2.diet_labels, co2.total_co2, co2.emission_class , recipes.total_calories, recipes.total_time, recipes.source]

    results=session.query(*sel).all()

    session.close()

    return_recipes = []
    for recipe_name, cuisine_type, diet_labels, total_co2, emission_class, total_calories, total_time, source in results:
        recipe_dict = {}
        recipe_dict["Name"] = recipe_name
        recipe_dict["Cuisine Type"] = cuisine_type
        recipe_dict["Diet Labels"] = diet_labels
        recipe_dict["Total CO2 Emission"] = total_co2
        recipe_dict["Emission Class"] = emission_class
        recipe_dict["Total Calories"] = total_calories
        recipe_dict["Total Time"] = total_time
        recipe_dict["Source"] = source
        return_recipes.append(recipe_dict)

    return jsonify(return_recipes)

if __name__ == '__main__':
    app.run(debug=True)