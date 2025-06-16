import streamlit as st
from models.recipe import Recipe
from typing import List

def apply_custom_css():
    """Apply custom CSS styling for recipe display"""
    st.markdown("""
        <style>
        .recipe-title { color: #1E3C6B; font-size: 24px; margin-bottom: 10px; }
        .recipe-description { color: #2C5282; margin-bottom: 15px; }
        .recipe-metadata { color: #4A5568; margin-bottom: 20px; }
        .section-title { color: #2D3748; font-size: 18px; margin-bottom: 10px; }
        .ingredient-item { color: #4A5568; margin-bottom: 5px; }
        .instruction-item { color: #4A5568; margin-bottom: 10px; }
        .save-button { float: right; }
        </style>
    """, unsafe_allow_html=True)

def display_recipe_header(recipe: Recipe, idx: int):
    """Display recipe title, description, and save button"""
    title_col, save_col = st.columns([5, 1])
    
    with title_col:
        st.markdown(f'<div class="recipe-title">{recipe.name}</div>', unsafe_allow_html=True)
    
    with save_col:
        st.download_button(
            label="💾 Save Recipe",
            data=recipe.to_text_content(),
            file_name=recipe.get_filename(),
            mime="text/plain",
            key=f"save_recipe_{idx}"
        )

def display_recipe_metadata(recipe: Recipe):
    """Display recipe description and metadata"""
    st.markdown(f'<div class="recipe-description">{recipe.description}</div>', unsafe_allow_html=True)
    metadata = [recipe.estimated_time, f"📊 {recipe.difficulty_level}"]
    st.markdown(f'<div class="recipe-metadata">{"    ".join(metadata)}</div>', unsafe_allow_html=True)

def display_recipe_content(recipe: Recipe):
    """Display recipe ingredients and instructions"""
    col1, col2 = st.columns(2)
    
    # Ingredients column
    with col1:
        st.markdown('<div class="section-title">Ingredients</div>', unsafe_allow_html=True)
        for ingredient in recipe.ingredients_list:
            st.markdown(f'<div class="ingredient-item">✓ {ingredient}</div>', unsafe_allow_html=True)

    # Instructions column
    with col2:
        st.markdown('<div class="section-title">Instructions</div>', unsafe_allow_html=True)
        for step_number, instruction in enumerate(recipe.instructions_list, 1):
            st.markdown(f'<div class="instruction-item"><strong>{step_number}</strong> {instruction}</div>', unsafe_allow_html=True)

def display_recipes(recipes: List[Recipe]):
    """Display all recipes with proper formatting"""
    if not recipes:
        return

    st.header("📚 Suggested Recipes")
    apply_custom_css()

    for idx, recipe in enumerate(recipes):
        display_recipe_header(recipe, idx)
        display_recipe_metadata(recipe)
        display_recipe_content(recipe)
        
        # Add divider between recipes
        if idx < len(recipes) - 1:
            st.divider() 