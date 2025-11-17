import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()


# Get GitHub token from environment variable
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError(
        "GITHUB_TOKEN environment variable is not set. "
        "Please set it with: export GITHUB_TOKEN='your_token_here'"
    )

client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=github_token,
    default_query={
        "api-version": "2024-08-01-preview",
    },
)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "INSERT_INPUT_HERE",
            },
        ],
    },
]

while True:
    response = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-5",
        reasoning_effort="medium",
    )

    if response.choices[0].message.tool_calls:
        print(response.choices[0].message.tool_calls)
        messages.append(response.choices[0].message)
        for tool_call in response.choices[0].message.tool_calls:
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": [
                    {
                        "type": "text",
                        "text": locals()[tool_call.function.name](),
                    },
                ],
            })
    else:
        print("[Model Response] " + response.choices[0].message.content)
        break
