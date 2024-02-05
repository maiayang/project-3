-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

CREATE TABLE "Chicken_Recipes" (
    "Recipe_ID" serial PRIMARY KEY,
    "Recipe_name" char(50) NOT NULL,
    "CuisineType" char(50) NOT NULL,
    "Source" char(30) NOT NULL,
    "Total_time" NUMERIC(8, 2) NOT NULL,
    "Calories" NUMERIC(8, 2) NOT NULL,
    "Calories_per_serving" NUMERIC(8, 2) NOT NULL
);

CREATE TABLE "CO2_Emissions" (
    "Recipe_ID" serial PRIMARY KEY,
    "Total_CO2" NUMERIC(8, 2) NOT NULL,
    "Emissions_class" char(10) NOT NULL,
    "Diet_labels" char(50) NOT NULL,
    "Number_of_ingredients" NUMERIC(8, 2) NOT NULL,
    "Total_weight" NUMERIC(8, 2) NOT NULL
);

ALTER TABLE "Chicken_Recipes" ADD CONSTRAINT "fk_Chicken_Recipes_Recipe_ID"
FOREIGN KEY ("Recipe_ID")
REFERENCES "CO2_Emissions" ("Recipe_ID");
