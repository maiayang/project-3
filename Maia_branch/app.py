import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/recipe_data.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
recipes=Base.classes.recipe_data3

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
        f"/api/v1.0/cuisineType/dietLabels/healthLabels<br/>"
        f"/api/v1.0/all_recipes"
    )

@app.route("/api/v1.0/all_recipes")
def all_recipes():
    # Create our session (link) from Python to the DB
    session=Session(engine)
    sel=[recipes.name, recipes.dishType, recipes.cuisineType, recipes.dietLabels, recipes.healthLabels, recipes.calories, recipes.totalTime]

    results=session.query(*sel).all()

    session.close()

    return_recipes = []
    for name, dishType, cuisineType, dietLabels, healthLabels, calories, totalTime in results:
        recipe_dict = {}
        recipe_dict["Name"] = name
        recipe_dict["Dish Type"] = dishType
        recipe_dict["Cuisine Type"] = cuisineType
        recipe_dict["Diet Labels"] = dietLabels
        recipe_dict["Health Labels"] = healthLabels
        recipe_dict["Calories"] = calories
        recipe_dict["Total Time"] = totalTime
        return_recipes.append(recipe_dict)

    return jsonify(return_recipes)


@app.route("/api/v1.0/<cuisineType>/<dietLabels>/<healthLabels>")

def filter(cuisineType, dietLabels, healthLabels):
    # Create our session (link) from Python to the DB
    session=Session(engine)
    sel=[recipes.name, recipes.dishType, recipes.cuisineType, recipes.dietLabels, recipes.healthLabels, recipes.calories, recipes.totalTime]

    results=session.query(*sel).\
            filter(recipes.cuisineType == cuisineType).\
            filter(recipes.healthLabels == healthLabels).\
            filter(recipes.dietLabels == dietLabels).all()

    session.close()

    return_recipes = []
    for name, dishType, cuisineType, dietLabels, healthLabels, calories, totalTime in results:
        recipe_dict = {}
        recipe_dict["Name"] = name
        recipe_dict["Dish Type"] = dishType
        recipe_dict["Cuisine Type"] = cuisineType
        recipe_dict["Diet Labels"] = dietLabels
        recipe_dict["Health Labels"] = healthLabels
        recipe_dict["Calories"] = calories
        recipe_dict["Total Time"] = totalTime
        return_recipes.append(recipe_dict)

    return jsonify(return_recipes)

if __name__ == '__main__':
    app.run(debug=True)