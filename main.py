import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4.1-mini"
token = os.environ["GITHUB_TOKEN"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)


def generate():
    response = client.complete(
        messages=[
            SystemMessage(""),
            UserMessage("What is the capital of France?"),
        ],
        temperature=1,
        top_p=1,
        model=model
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    print(generate())