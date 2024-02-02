import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from flask import Flask, jsonify, request

# Import the Tkinter library for GUI development
import tkinter as tk
from tkinter import *


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/recipe_data.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
recipes=Base.classes.recipe_data

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
        f"/api/v1.0/scatter_plot"

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


@app.route("/api/v1.0/recipe_search")
def recipe_search():

    ### Code for user drop-down menu ###
    root = tk.Tk()
    root.title("Recipe Search")
    root.geometry("400x300")
    root.attributes('-topmost',True)
    
    # Add a label
    label = tk.Label(root, text="Search Criteria")
    label.pack(pady=10)  # Add padding to separate the label from other elements

    # Create a StringVar to hold the selected option
    selected_option1 = tk.StringVar(value="Cuisine Type")
    selected_option2 = tk.StringVar(value="Diet Labels")
    selected_option3 = tk.StringVar(value="Health Labels")

    # Create the dropdown menu
    cuisine_options = ["asian", "south east asian", "chinese", "japanese"]
    dropdown1 = tk.OptionMenu(root, selected_option1, *cuisine_options)
    dropdown1.pack(pady=10)

    diet_options = ["Low-Fat", "Balanced", "High-Protein", "High-Fiber"]
    dropdown2 = tk.OptionMenu(root, selected_option2, *diet_options)
    dropdown2.pack(pady=10)

    health_options = ["Vegan", "Sugar-Conscious", "Vegetarian"]
    dropdown3 = tk.OptionMenu(root, selected_option3, *health_options)
    dropdown3.pack(pady=10)

    # Add a quit button
    show_button = tk.Button(root, text="Submit", command=root.quit)
    show_button.pack()

    root.mainloop()
    
    selection1 = selected_option1.get()
    selection2 = selected_option2.get()
    selection3 = selected_option3.get()
    root.destroy()

    ### Code to return json ###
    # Create our session (link) from Python to the DB
    session=Session(engine)
    sel=[recipes.name, recipes.dishType, recipes.cuisineType, recipes.dietLabels, recipes.healthLabels, recipes.calories, recipes.totalTime]

    results=session.query(*sel).\
        filter(recipes.cuisineType == selection1).\
        filter(recipes.dietLabels == selection2).\
        filter(recipes.healthLabels == selection3).all()
    

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

def scatter_plot():
    # Create a session to interact with the database
    session = Session(engine)

    # Query the ChickenRecipe table and load data into a Pandas DataFrame
    result = session.query(func.count(recipes.ingredient_id).label('num_ingredients'),
                            func.avg(recipes.total_co2).label('avg_co2')) \
                    .group_by(recipes.recipe_name) \
                    .all()
    df = pd.DataFrame(result)

    # Close the session
    session.close()

    # Create a scatter plot without a regression line
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='num_ingredients', y='avg_co2', data=df)
    plt.title('Correlation between Number of Ingredients and Total CO2')
    plt.xlabel('Number of Ingredients')
    plt.ylabel('Average Total CO2')

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    
    # Convert the plot to a base64-encoded string
    plot_data = base64.b64encode(image_stream.read()).decode('utf-8')

    # Return the base64-encoded plot as a JSON response
    return jsonify({"scatter_plot": plot_data})

@app.route("/api/v1.0/scatter_plot")
def show_scatter_plot():
    return scatter_plot()

if __name__ == '__main__':
    app.run(debug=True)