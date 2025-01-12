from fastapi import FastAPI, HTTPException
from src.services.agents import recipe_chain, ingredient_chain, calorie_chain, insights_chain
from src.services.utils import extract_ingredients
from dotenv import load_dotenv
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# FastAPI application setup
app = FastAPI(
    title="LangChain Recipe Generator",
    description="Generate recipes with LangChain and Groq",
    version="7.0.0"
)

@app.post("/generate-recipe/")
async def generate_recipe(cuisine: str):
    """
    Generate a recipe with ingredient analysis, calorie analysis, and insights.
    """
    try:
        logger.info(f"Generating recipe for {cuisine} cuisine")

        # Step 1: Generate recipe
        recipe_output = recipe_chain.invoke({"cuisine": cuisine})
        logger.info("Recipe generated successfully")

        # Step 2: Extract ingredients from the recipe
        ingredients = extract_ingredients(recipe_output.content)
        logger.info("Ingredients extracted successfully")

        # Step 3: Analyze ingredients and get a revised recipe
        ingredient_output = ingredient_chain.invoke({"ingredients": ingredients})
        logger.info("Ingredients analyzed and revised recipe generated successfully")

        # Step 4: Extract the revised recipe from the ingredient analysis output
        revised_recipe = ingredient_output.content.split("Revised Recipe:")[-1].strip()
        logger.info("Revised recipe extracted successfully")

        # Step 5: Analyze calories for the revised recipe
        calorie_output = calorie_chain.invoke({"ingredients": revised_recipe})
        logger.info("Calorie analysis completed successfully")

        # Step 6: Generate insights for the revised recipe
        insights_output = insights_chain.invoke({"recipe": revised_recipe})
        logger.info("Insights generated successfully")

        # Return the full response
        return {
            "status": "success",
            "cuisine": cuisine,
            "original_recipe": recipe_output.content,
            "ingredient_analysis": ingredient_output.content,
            "revised_recipe": revised_recipe,
            "calorie_analysis": calorie_output.content,
            "insights": insights_output.content
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "version": "7.0.0",
        "models": {
            "recipe_generator": "mixtral-8x7b-32768",
            "ingredient_checker": "llama-3.1-8b-instant",
            "calorie_agent": "llama3-8b-8192",
            "insights_agent": "llama-3.1-70b-versatile"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
