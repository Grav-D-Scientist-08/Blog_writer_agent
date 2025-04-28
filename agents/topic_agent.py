from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Initialize the Agent
trending_topic_agent = Agent(
    name="Trending Topic Agent",
    model=Groq(
        api_key=os.getenv("GROQ_API_KEY"),
        id="llama3-70b-8192"  # Make sure you're using a valid model ID
    ),
    tools=[DuckDuckGo()],
    instructions=[
        "Give a list of 15 latest trending topics in AI and technology as short headlines, like news titles. Example format:\n"
        "- AGI is coming sooner than expected\n"
        "- How AI is reshaping healthcare\n"
        "Return only the list, no intro or outro."
    ],
    show_tool_calls=True,
    markdown=True,
)

# Get trending topics function
def get_trending_topics(user_interest="AI"):
    try:
        query = f"Trending topics in {user_interest}"
        response = trending_topic_agent.run(query)

        # Access the response content safely
        content = response.content if hasattr(response, "content") else str(response)

        # Extract lines that look like news headlines
        lines = content.strip().split("\n")
        topics = []

        for line in lines:
            line = line.strip()
            if re.match(r"^[-•*]\s+", line):  # Match bullet points
                clean_line = re.sub(r"^[-•*]\s+", "", line)
                if 10 < len(clean_line) < 120:  # filter for reasonable length
                    topics.append(clean_line)

        return topics[1:15]
    except Exception as e:
        print(f"Error fetching trending topics: {e}")
        return []

# Main run
if __name__ == "__main__":
    topics = get_trending_topics("AI")
    print("📢 Trending Topics in AI:\n")
    for topic in topics:
        print(f"- {topic}")