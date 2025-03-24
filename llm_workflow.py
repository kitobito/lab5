import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load API keys
load_dotenv()

API_KEY = os.getenv("NGU_API_KEY")
BASE_URL = os.getenv("NGU_BASE_URL")
LLM_MODEL = os.getenv("NGU_MODEL")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def call_llm(messages, tools=None, tool_choice=None):
    """Make an LLM API call."""
    kwargs = {"model": LLM_MODEL, "messages": messages}
    if tools:
        kwargs["tools"] = tools
    if tool_choice:
        kwargs["tool_choice"] = tool_choice
    response = client.chat.completions.create(**kwargs)
    return response

def get_sample_blog_post():
    """Read the sample blog post from a JSON file."""
    try:
        with open('sample-blog-post.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: sample-blog-post.json file not found.")
        return None

# Tool Schemas
extract_key_points_schema = {"type": "function", "function": {"name": "extract_key_points", "parameters": {"type": "object", "properties": {"key_points": {"type": "array", "items": {"type": "string"}}}, "required": ["key_points"]}}}

generate_summary_schema = {"type": "function", "function": {"name": "generate_summary", "parameters": {"type": "object", "properties": {"summary": {"type": "string"}}, "required": ["summary"]}}}

def task_extract_key_points(blog_post):
    messages = [
        {"role": "system", "content": "Extract key points from the blog post."},
        {"role": "user", "content": f"Title: {blog_post['title']}\n\nContent: {blog_post['content']}"}
    ]
    response = call_llm(messages, tools=[extract_key_points_schema], tool_choice={"type": "function", "function": {"name": "extract_key_points"}})
    return response.choices[0].message.tool_calls[0].function.arguments if response.choices[0].message.tool_calls else []

def task_generate_summary(key_points):
    messages = [
        {"role": "system", "content": "Summarize the key points concisely."},
        {"role": "user", "content": f"Key points:\n" + "\n".join(f"- {point}" for point in key_points)}
    ]
    response = call_llm(messages, tools=[generate_summary_schema], tool_choice={"type": "function", "function": {"name": "generate_summary"}})
    return response.choices[0].message.tool_calls[0].function.arguments if response.choices[0].message.tool_calls else ""

def run_pipeline_workflow(blog_post):
    key_points = task_extract_key_points(blog_post)
    summary = task_generate_summary(key_points)
    return {"key_points": key_points, "summary": summary}

def evaluate_content(content):
    messages = [{"role": "user", "content": f"Evaluate the quality of this content:\n{content}"}]
    response = call_llm(messages)
    return response.choices[0].message.content

def generate_with_reflexion(generator_func, *args):
    content = generator_func(*args)
    evaluation = evaluate_content(content)
    return evaluation if "good quality" in evaluation else generator_func(*args)

def run_agent_workflow(blog_post):
    system_message = "You are a content repurposing agent."
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Process this blog post:\n\n{blog_post['content']}"}
    ]
    tools = [extract_key_points_schema, generate_summary_schema]
    
    for _ in range(5):
        response = call_llm(messages, tools)
        if not response.choices[0].message.tool_calls:
            break
        for tool_call in response.choices[0].message.tool_calls:
            tool_name = tool_call.function.name
            tool_result = globals()[f"task_{tool_name}"](blog_post)
            messages.append({"role": "assistant", "content": json.dumps(tool_result)})
    return messages[-1]

if __name__ == "__main__":
    blog_post = get_sample_blog_post()
    if blog_post:
        pipeline_output = run_pipeline_workflow(blog_post)
        agent_output = run_agent_workflow(blog_post)
        print("Pipeline Output:", pipeline_output)
        print("Agent Output:", agent_output)
