from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Agent to write SEO-optimized blog content
blog_writer_agent = Agent(
    name="BlogWriterAgent",
    model=Groq(
        api_key=api_key,
        id="llama-3.3-70b-versatile"
    ),
    instructions=[        
        "You are a professional blog writer.",
        "Your task is to write a detailed, SEO-friendly blog on the given topic.",
        "The blog should be well-structured, engaging, and informative.",
        "Include an introduction, multiple subheadings, bullet points, and a conclusion.",
        "Use a conversational tone and make the content easy to understand.",
        "Incorporate relevant keywords naturally throughout the blog to enhance SEO.",
        "Ensure the blog is factually accurate and up-to-date.",
        "The blog should be at least 500 words long.",
        "Use markdown formatting for the blog.",
        "Use the following structure: Introduction, Subheading 1, Content for Subheading 1, Subheading 2, Content for Subheading 2, Subheading 3, Content for Subheading 3, Conclusion.",
    ],
    show_tool_calls=False,
    markdown=True,
)
def write_blog(topic):
    prompt = f"Write a well-structured, SEO-optimized blog on the topic: {topic}"
    try:
        return blog_writer_agent.run(prompt)
    except Exception as e:
        return f"Error generating blog: {e}"

if __name__ == "__main__":
    topic = "Top AI Tools for Content Creation in 2025"
    blog = write_blog(topic)

    # Check if the response is a RunResponse object with a 'content' attribute
    if hasattr(blog, 'content'):
        print(blog.content)
    else:
        print(blog.content)
