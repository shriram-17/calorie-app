from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from src.config.prompts import RECIPE_TEMPLATE, INGREDIENT_TEMPLATE, CALORIE_TEMPLATE, INSIGHTS_TEMPLATE
import os

def create_groq_llm(model_name: str):
    """Create a Groq LLM instance."""
    return ChatGroq(
        model_name=model_name,
        temperature=0.7,  # Lower temperature for factual responses
        max_tokens=5000,  # Limit the token count
        groq_api_key=os.getenv("groq_token")
    )

# Initialize LLMs
recipe_llm = create_groq_llm("mixtral-8x7b-32768")
ingredient_llm = create_groq_llm("llama-3.1-8b-instant")
calorie_llm = create_groq_llm("llama3-8b-8192")
insights_llm = create_groq_llm("llama-3.1-70b-versatile")

# Define chains
recipe_chain = (
    RunnablePassthrough.assign(cuisine=lambda x: x["cuisine"])
    | PromptTemplate.from_template(RECIPE_TEMPLATE)
    | recipe_llm
)

ingredient_chain = (
    RunnablePassthrough.assign(ingredients=lambda x: x["ingredients"])
    | PromptTemplate.from_template(INGREDIENT_TEMPLATE)
    | ingredient_llm
)

calorie_chain = (
    RunnablePassthrough.assign(ingredients=lambda x: x["ingredients"])
    | PromptTemplate.from_template(CALORIE_TEMPLATE)
    | calorie_llm
)

insights_chain = (
    RunnablePassthrough.assign(recipe=lambda x: x["recipe"])
    | PromptTemplate.from_template(INSIGHTS_TEMPLATE)
    | insights_llm
)
