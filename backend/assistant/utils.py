import os
import requests
import aisuite as ai
from ollama import Client
from general_settings.settings import env

# Configure environment variables for API access
os.environ["HUGGINGFACE_API_KEY"] = env("HUGGINGFACE_API_KEY")

# Initialize global clients for performance (reusing connections)
client = ai.Client()
ollama_client = Client(
    host=env("OLLAMA_CLOUD_HOST"),
    headers={
        "Authorization": f"Bearer {env('OLLAMA_API_KEY')}",
    },
)


def get_llm_response(prompt: str, tools: list = None, temperature: float = 0.7) -> str:
    """
    Retrieves a response from a model managed by aisuite (typically HuggingFace).

    Args:
        prompt (str): The user input or system prompt to send to the model.
        tools (list, optional): A list of tools/functions the model can call. Defaults to None.
        temperature (float, optional): Sampling temperature for response variability. Defaults to 0.7.

    Returns:
        str: The generated message content from the model.
    """
    response = client.chat.completions.create(
        model=env("HUGGINGFACE_MODEL_NAME"),
        messages=[{"role": "user", "content": prompt}],
        tools=tools,
        temperature=temperature,
        max_turns=5,
    )
    return response.choices[0].message.content


def get_local_ollama_response(
    prompt: str, model: str = env("LOCAL_OLLAMA_MODEL")
) -> str:
    """
    Queries a locally running Ollama instance using its REST API.

    Args:
        prompt (str): The prompt to send to the local model.
        model (str): The name of the model to use. Defaults to the LOCAL_OLLAMA_MODEL setting.

    Returns:
        str: The generated response text or an error message if the connection fails.
    """
    url = f"{env('OLLAMA_LOCAL_HOST')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}"


def get_cloud_ollama_response(
    prompt: str, model: str = env("CLOUD_OLLAMA_MODEL")
) -> str:
    """
    Queries a cloud-based Ollama instance using the official Ollama Python client.

    Args:
        prompt (str): The prompt to send to the cloud model.
        model (str): The name of the model to use. Defaults to the CLOUD_OLLAMA_MODEL setting.

    Returns:
        str: The content of the generated response.
    """
    messages = [{"role": "user", "content": prompt}]
    response = ollama_client.chat(model, messages=messages, stream=False)
    content = response["message"]["content"]
    return content


# ===============================
# Prompts
# ===============================


def build_prompt(question: str, KNOWLEDGE_BASE: str) -> str:
    return f"""
You are a sharp customer support assistant. No guessing. No creativity. Just facts.

RULES:
1. Read the USER QUESTION carefully.
2. Look ONLY inside the KNOWLEDGE BASE.
3. If the answer exists:
   - Reply clearly.
   - Be short.
   - Be helpful.
   - Sound polite with a tiny touch of light humor.
   - Do NOT mention the knowledge base.
4. If the answer does NOT exist:
   - Reply with EXACTLY this word:
     web_search
   - No punctuation.
   - No explanation.
   - No extra words.

USER QUESTION:
{question}

KNOWLEDGE BASE:
{KNOWLEDGE_BASE}
"""


def build_web_prompt(question: str, content: str) -> str:
    return f"""
You are a fast, clever customer support assistant.

MISSION:
- Clean and summarize the CONTENT.
- Answer the USER QUESTION clearly.
- Keep it short.
- Be respectful.
- Add a light, friendly touch of humor.
- Do NOT mention tools, scraping, or sources.
- Deliver a final, ready-to-send answer.

CONTENT:
{content}

USER QUESTION:
{question}
"""
