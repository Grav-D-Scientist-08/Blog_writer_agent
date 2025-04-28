from phi.agent import Agent
from phi.model.groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# Agent to validate the blog for content quality and relevance
blog_validator_agent = Agent(
    name="BlogValidatorAgent",
    model=Groq(
        api_key=os.getenv("GROQ_API_KEY"),
        id="llama-3.3-70b-versatile"
    ),
    instructions=[
        "Review the blog for accuracy, relevance, SEO compliance, and reader engagement.",
        "If it is not valid, suggest that the blog needs to be regenerated."
    ],
    show_tool_calls=False,
    markdown=True,
)

def validate_blog(blog_text):
    prompt = f"Review the following blog:\n\n{blog_text}\n\nIs this blog appropriate, accurate, SEO-optimized, and engaging? If not, mention the problems."
    return blog_validator_agent.run(prompt)

if __name__ == "__main__":
    sample_blog = "This is a dummy blog about AI that is too short."
    print(validate_blog(sample_blog))