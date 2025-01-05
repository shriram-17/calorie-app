from fastapi import FastAPI, HTTPException
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough, RunnableSequence
from dotenv import load_dotenv
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LangChain Recipe Generator",
    description="Generate recipes with LangChain and Groq",
    version="7.0.0"
)

# Load environment variables
load_dotenv()

def create_groq_llm(model_name: str):
    """Create a Groq LLM instance."""
    return ChatGroq(
        model_name=model_name,
        temperature=0.7,  # Lower temperature for more factual responses
        max_tokens=5000,  # Reduce tokens for concise outputs
        groq_api_key=os.getenv("groq_token")
    )

# Define prompts for each agent
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
4. Check if the recipe is healthy (yes/no) and why."""

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

# Create LLMs
recipe_llm = create_groq_llm("mixtral-8x7b-32768")  # Recipe Generator
ingredient_llm = create_groq_llm("llama-3.3-70b-versatile")  # Ingredient Checker
calorie_llm = create_groq_llm("llama-3.3-70b-versatile")  # Calorie Agent
insights_llm = create_groq_llm("llama-3.3-70b-versatile")  # Insights Agent

# Create chains using RunnableSequence
recipe_chain = (
    RunnablePassthrough.assign(cuisine=lambda x: x["cuisine"])
    | PromptTemplate.from_template(RECIPE_TEMPLATE)
    | recipe_llm
)

ingredient_chain = (
    RunnablePassthrough.assign(ingredients=lambda x: x["recipe"])
    | PromptTemplate.from_template(INGREDIENT_TEMPLATE)
    | ingredient_llm
)

calorie_chain = (
    RunnablePassthrough.assign(ingredients=lambda x: x["recipe"])
    | PromptTemplate.from_template(CALORIE_TEMPLATE)
    | calorie_llm
)

insights_chain = (
    RunnablePassthrough.assign(recipe=lambda x: x["recipe"])
    | PromptTemplate.from_template(INSIGHTS_TEMPLATE)
    | insights_llm
)

@app.post("/generate-recipe/")
async def generate_recipe(cuisine: str):
    """Generate a recipe with ingredient analysis, calorie analysis, and insights."""
    try:
        logger.info(f"Generating recipe for {cuisine} cuisine")

        # Generate recipe
        recipe_output = recipe_chain.invoke({"cuisine": cuisine})
        logger.info("Recipe generated successfully")

        # Analyze ingredients
        ingredient_output = ingredient_chain.invoke({"recipe": recipe_output})
        logger.info("Ingredients analyzed successfully")

        # Analyze calories
        calorie_output = calorie_chain.invoke({"recipe": recipe_output})
        logger.info("Calorie analysis completed successfully")

        # Generate insights
        insights_output = insights_chain.invoke({"recipe": recipe_output})
        logger.info("Insights generated successfully")

        return {
            "status": "success",
            "cuisine": cuisine,
            "recipe": recipe_output,
            "ingredient_analysis": ingredient_output,
            "calorie_analysis": calorie_output,
            "insights": insights_output
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Simplified health check endpoint."""
    return {
        "status": "healthy",
        "version": "7.0.0",
        "models": {
            "recipe_generator": "mixtral-8x7b-32768",
            "ingredient_checker": "llama-3.1-8b-instant",
            "calorie_agent": "llama-3.3-70b-versatile",
            "insights_agent": "llama-3.1-8b-instant"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)