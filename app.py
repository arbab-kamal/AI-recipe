import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables (for API keys)
load_dotenv()

# Set API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit App Title
st.title("AI Recipe Creator & Weekly Diet Planner 🍳")

# Sidebar for Input
st.sidebar.header("Input for Recipe or Diet Plan")
ingredients = st.sidebar.text_area(
    "Enter ingredients (comma-separated):",
    "chicken, rice, broccoli, garlic",
)
preferences = st.sidebar.text_input(
    "Enter dietary preferences (e.g., vegetarian, keto, spicy):", "spicy"
)
cuisine = st.sidebar.text_input(
    "Enter cuisine style (e.g., Italian, Indian, Mexican):", "Indian"
)

# Function to Generate Recipe Using GPT-4
def generate_recipe(ingredients, preferences, cuisine):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a chef AI that generates recipes based on user inputs.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Generate a recipe using these ingredients: {ingredients}. "
                        f"The recipe should match these dietary preferences: {preferences}. "
                        f"The recipe should have a {cuisine} style. Provide a title, ingredients list, and steps."
                    ),
                },
            ],
        )
        recipe = response["choices"][0]["message"]["content"]
        return recipe
    except Exception as e:
        st.error(f"An error occurred while generating the recipe: {e}")
        return None

# Function to Generate Weekly Diet Plan Using GPT-4
def generate_weekly_diet(preferences):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a nutritionist AI that creates weekly diet plans based on user preferences.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Create a weekly diet plan. The diet plan should match these dietary preferences: {preferences}. "
                        "Include breakfast, lunch, dinner, and snacks for each day of the week. "
                        "Provide specific meal suggestions and their primary ingredients."
                    ),
                },
            ],
        )
        diet_plan = response["choices"][0]["message"]["content"]
        return diet_plan
    except Exception as e:
        st.error(f"An error occurred while generating the diet plan: {e}")
        return None

# Function to Generate Food Image Using DALL·E 3
def generate_food_image(recipe_title):
    try:
        # Use DALL·E 3 to create an image
        response = openai.Image.create(
            prompt=f"A delicious and appetizing photo of {recipe_title}, beautifully plated, professional food photography.",
            n=1,  # Generate one image
            size="512x512",  # Resolution (adjust if needed)
        )
        # Extract the image URL from the response
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        st.error(f"An error occurred while generating the image with DALL·E 3: {e}")
        return None

# Main Logic for Recipe Generation
if st.button("Generate Recipe and Visual"):
    with st.spinner("Generating recipe..."):
        # Generate Recipe
        recipe = generate_recipe(ingredients, preferences, cuisine)
        if recipe:
            st.subheader("Generated Recipe")
            st.text(recipe)

            # Extract Recipe Title
            recipe_title = recipe.split("\n")[0]  # Assume the first line is the title

            with st.spinner("Generating food image..."):
                # Generate Food Image
                image_url = generate_food_image(recipe_title)
                if image_url:
                    st.image(image_url, caption=recipe_title, use_container_width=True)
                else:
                    st.warning("Image generation failed.")
        else:
            st.warning("Recipe generation failed.")

# Main Logic for Weekly Diet Plan
if st.button("Generate Weekly Diet Plan"):
    with st.spinner("Generating weekly diet plan..."):
        diet_plan = generate_weekly_diet(preferences)
        if diet_plan:
            st.subheader("Generated Weekly Diet Plan")
            st.text(diet_plan)
        else:
            st.warning("Weekly diet plan generation failed.")
