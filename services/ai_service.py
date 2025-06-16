from typing import List, Optional
from PIL import Image
import google.generativeai as genai
from models.recipe import Recipe, parse_ai_response

def get_recipe_prompt(allergies: Optional[str] = None, max_time: Optional[int] = None) -> str:
    """Generate the prompt for recipe creation"""
    return f"""
    Create 3 different recipes using ONLY the provided ingredients.
    Your response MUST be a valid JSON array of recipe objects. If you cannot generate recipes based on the input, return an empty array [].
    Each recipe object in the array MUST have the following keys and value types:
    - "name": string (The name of the dish)
    - "description": string (A brief 1-2 sentence enticing description of the dish)
    - "ingredientsList": string[] (An array of strings, where each string is an ingredient with exact measurements)
    - "instructionsList": string[] (An array of strings, where each string is a step in the cooking instructions)
    - "estimatedTime": string (Estimated total cooking time)
    - "difficultyLevel": string (Must be one of: "Easy", "Medium", "Hard")

    Important constraints:
    - Use ONLY the available ingredients
    - Avoid: {allergies if allergies else 'none'}
    - Max cooking time: {max_time} minutes
    - Make each recipe distinct in style and cooking method
    - Keep descriptions informative but concise
    - Format measurements consistently (e.g., "1 cup", "200g", "2 tablespoons")
    - Include any preparation notes in parentheses (e.g., "1 onion (finely chopped)")
    """

class AIService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.vision_model = genai.GenerativeModel('gemini-2.0-flash')
        self.text_model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_recipes_from_image(
        self,
        image: Image.Image,
        allergies: Optional[str] = None,
        max_time: Optional[int] = None
    ) -> List[Recipe]:
        """Generate recipes from an image input"""
        prompt = get_recipe_prompt(allergies, max_time)
        response = self.vision_model.generate_content([prompt, image])
        return parse_ai_response(response.text)

    def generate_recipes_from_text(
        self,
        ingredients_text: str,
        allergies: Optional[str] = None,
        max_time: Optional[int] = None
    ) -> List[Recipe]:
        """Generate recipes from text input"""
        prompt = get_recipe_prompt(allergies, max_time)
        voice_prompt = f"{prompt}\n\nAvailable ingredients: {ingredients_text}"
        response = self.text_model.generate_content(voice_prompt)
        return parse_ai_response(response.text) 