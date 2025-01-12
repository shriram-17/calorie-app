RECIPE_TEMPLATE = """Generate a detailed recipe for {cuisine} cuisine. Include:
1. Recipe name and cultural background.
2. Ingredients with measurements.
3. Step-by-step instructions.
4. Serving suggestions and dietary information."""

INGREDIENT_TEMPLATE = """Analyze these ingredients for potential issues:
{ingredients}
1. Identify allergens.
2. Suggest healthier substitutions.
3. Highlight hard-to-find items.
4. Check if the recipe is healthy (yes/no) and why.
5. Provide a revised recipe that incorporates the suggested changes, ensuring it is healthier, allergen-free, and uses easily available ingredients."""

CALORIE_TEMPLATE = """Estimate the calorie content of this recipe based on the ingredients:
{ingredients}
1. Provide the total calorie count.
2. Break down the calorie contribution of major ingredients.
3. Suggest ways to reduce calories if the recipe is high in calories."""

INSIGHTS_TEMPLATE = """Provide concise insights for this recipe:
{recipe}
1. Is this recipe healthy? (yes/no) and why.
2. Key nutritional highlights.
3. Calorie insights: Total calories and breakdown.
4. One sentence cultural significance."""
