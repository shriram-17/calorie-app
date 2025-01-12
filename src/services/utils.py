def extract_ingredients(recipe_output: str) -> str:
    """Extract the ingredients section from the recipe output."""
    if "Ingredients:" in recipe_output:
        return recipe_output.split("Ingredients:")[1].split("Instructions:")[0].strip()
    return recipe_output  # Fallback to the entire recipe if extraction fails
