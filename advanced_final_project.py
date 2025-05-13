import streamlit as st
import pandas as pd
import requests
import json
import random

col1, col2 = st.columns([1, 2])
with col1:
    st.image("https://img.freepik.com/premium-vector/fitness-food-logo-with-kettlebell-leaves-vector-silhouette-illustration_685330-3282.jpg", width=100)
with col2:
    st.title("Workout & Diet API")

#st.title("Workout & Diet API")

url = 'https://wger.de/api/v2/exerciseinfo/?language=2&limit=20'
response = requests.get(url)
data = response.json()

goal_categories = {
    "Cut": ["Seafood", "Vegetarian", "Side"],
    "Maintenance": ["Chicken", "Pasta", "Miscellaneous"],
    "Bulk": ["Beef", "Lamb", "Pork"]
}
def get_random_meal_from_category(category):
    res = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}").json()
    meals = res['meals']
    return random.choice(meals)

st.subheader("Diet Objective:")
goal = None
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔥 Cut"):
        goal = "Cut"
with col2:
    if st.button("⚖️ Maintenance"):
        goal = "Maintenance"
with col3:
    if st.button("💪 Bulk"):
        goal = "Bulk"


if goal:
    category = random.choice(goal_categories[goal])
    meal = get_random_meal_from_category(category)
    st.subheader(f"{meal['strMeal']} ({category})")
    st.image(meal['strMealThumb'])
    details = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal['idMeal']}").json()
    info = details['meals'][0]
    st.write(info['strInstructions'][:400] + "...") 
    st.markdown(f"[Full Recipe]({info['strSource'] or 'https://www.themealdb.com'})")
    #if st.button("Ingredients & Amounts"): button to show amounts and ingredients, but has to be coded again 
       #### for i in range(1, 21):
       ###     ingredient = info.get(f"strIngredient{i}")
        ##    measure = info.get(f"strMeasure{i}")
       #     if ingredient and ingredient.strip():
         #       st.markdown(f"- **{ingredient.strip()}**: {measure.strip() if measure else ''}")






st.divider()


st.subheader("Training day:")

muscles = requests.get("https://wger.de/api/v2/muscle/").json()['results']
muscle_dict = {m['name_en']: m['id'] for m in muscles if m['name_en']}
chosen = st.selectbox("Choose a muscle", list(muscle_dict))


if st.button("Get Exercises"):
    muscle_id = muscle_dict[chosen]
    results = requests.get("https://wger.de/api/v2/exerciseinfo/?language=2&limit=100").json()['results']
    muscle_lookup = {m['id']: m['name_en'] for m in muscles if m['name_en']}

    matches = [
        (t['name'], t['description'],ex['id'], [muscle_lookup[m['id']] for m in ex['muscles'] if m['id'] in muscle_lookup])
        for ex in results
        if muscle_id in [m['id'] for m in ex['muscles']]
        for t in ex['translations']
        if t['language'] == 2
        ][:3]

    for name, desc,  ex_id, muscle_names in matches:
        st.subheader(name)
        with st.expander("View exercise details"):
            st.write(desc)
        st.write("Targeted muscles:", ', '.join(muscle_names) or "None listed")
        st.markdown(f"[Exercise profile](https://wger.de/api/v2/exerciseinfo/{ex_id}/)")


