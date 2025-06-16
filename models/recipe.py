from typing import List, Dict
import json

class Recipe:
    def __init__(
        self,
        name: str,
        description: str,
        ingredients_list: List[str],
        instructions_list: List[str],
        estimated_time: str,
        difficulty_level: str
    ):
        self.name = name
        self.description = description
        self.ingredients_list = ingredients_list
        self.instructions_list = instructions_list
        self.estimated_time = estimated_time
        self.difficulty_level = difficulty_level

    @classmethod
    def from_dict(cls, data: Dict) -> 'Recipe':
        return cls(
            name=data["name"],
            description=data["description"],
            ingredients_list=data["ingredientsList"],
            instructions_list=data["instructionsList"],
            estimated_time=data["estimatedTime"],
            difficulty_level=data["difficultyLevel"]
        )

    def to_text_content(self) -> str:
        """Convert recipe to formatted text content for saving"""
        return f"""
{self.name}

{self.description}

{self.estimated_time}
{self.difficulty_level}

Ingredients:
{chr(10).join(f"• {ingredient}" for ingredient in self.ingredients_list)}

Instructions:
{chr(10).join(f"{i+1}. {instruction}" for i, instruction in enumerate(self.instructions_list))}
"""

    def get_filename(self) -> str:
        """Generate a filename for the recipe"""
        return f"{self.name.lower().replace(' ', '_')}.txt"

def parse_ai_response(response_text: str) -> List[Recipe]:
    """Parse AI response text into Recipe objects"""
    # Clean the response text to get pure JSON
    json_text = response_text.strip()
    if json_text.startswith("```json"):
        json_text = json_text[7:]  # Remove ```json
    if json_text.endswith("```"):
        json_text = json_text[:-3]  # Remove ```
    
    # Parse JSON and convert to Recipe objects
    recipes_data = json.loads(json_text.strip())
    return [Recipe.from_dict(recipe_data) for recipe_data in recipes_data] 