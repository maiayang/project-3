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
        f"/api/v1.0/all_recipes<br/>"
        f"/api/v1.0/recipe_details<br/>"
        f"/api/v1.0/recipe_search"
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

@app.route("/api/v1.0/recipe_details", methods=['GET'])
def recipe_details():
    # Get the recipe name from the query parameters
    recipe_name = request.args.get('recipe_name')

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the database to get details for the specified recipe name
    sel = [recipes.recipe_name, co2.total_co2, recipes.total_time, recipes.cuisine_type]
    results = session.query(*sel).filter(recipes.recipe_name == recipe_name).all()

    session.close()

    if not results:
        return jsonify({"error": "Recipe not found"}), 404

    # Extract information from the query results
    recipe_name, total_co2, total_time, cuisine_type = results[0]

    # Return the details as JSON
    return jsonify({
        "Name": recipe_name,
        "CO2 Content": total_co2,
        "Total Time per Recipe": total_time,
        "Cuisine Type": cuisine_type
    })

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

        # Create a StringVar to hold the selected option and store them in a variable
    selected_option1 = tk.StringVar(value="Calories Per Serving")
    selected_option2 = tk.StringVar(value="CO2 Emission")
    # selected_option3 = tk.StringVar(value="Health Labels")
        
        #Access text from StringVar and store to a variable
    selection1 = selected_option1.get()
    selection2 = selected_option2.get()
    # selection3 = selected_option3.get()

        # Create the dropdown menu
    calories_per_serving = ["<300", "<500", "<750", "<1000", "<1500"]
    dropdown1 = tk.OptionMenu(root, selected_option1, *calories_per_serving)
    dropdown1.pack(pady=10)

    CO2_emission = ["<1000", "<5000", "<10000", "<15000"]
    dropdown2 = tk.OptionMenu(root, selected_option2, *CO2_emission)
    dropdown2.pack(pady=10)

    # health_options = ["Vegan", "Sugar-Conscious", "Vegetarian"]
    # dropdown3 = tk.OptionMenu(root, selected_option3, *health_options)
    # dropdown3.pack(pady=10)

        # Add a quit button
    show_button = tk.Button(root, text="Submit", command=root.quit)
    show_button.pack()

    root.mainloop()
    
    root.destroy()

    ### Code to return json ###
        # Create our session (link) from Python to the DB
    session=Session(engine)
    sel=[recipes.recipe_name, recipes.cuisine_type, co2.diet_labels, recipes.calories_per_serving, recipes.source, co2.total_co2, co2.emission_class]

    results=session.query(*sel).\
        filter(recipes.calories_per_serving < selection1.replace('<','')).\
        filter(co2.total_co2 < selection2.replace('<','')).all()
        # filter(recipes.healthLabels == selection3).all()
    
    session.close()

    return_recipes = []
    for recipe_name, cuisine_type, diet_labels, calories_per_serving, source, total_co2, emission_class in results:
        recipe_dict = {}
        recipe_dict["Name"] = recipe_name
        recipe_dict["Cuisine Type"] = cuisine_type
        recipe_dict["Diet Labels"] = diet_labels
        recipe_dict["Calories Per Serving"] = calories_per_serving
        recipe_dict["Source"] = source
        recipe_dict["Total CO2 Emission"] = total_co2
        recipe_dict["Emission Class"] = emission_class
        return_recipes.append(recipe_dict)
    
    return jsonify(return_recipes)


if __name__ == '__main__':
    app.run(debug=True)