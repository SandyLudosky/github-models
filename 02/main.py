import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()

# 1. Récupérer le token GitHub
github_token = os.getenv("GITHUB_TOKEN")
if not github_token:
    raise ValueError(
        "GITHUB_TOKEN environment variable is not set. "
        "Please set it with: export GITHUB_TOKEN='your_token_here'"
    )

# 2. Initialiser le client pour GitHub Models
client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=github_token,
    default_query={
        "api-version": "2024-08-01-preview",
    },
)

def main():
    print("Assistant IA (GitHub Models) – taper 'quit' pour sortir.\n")

    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "Tu es un assistant utile, clair et concis, qui répond en français.",
                },
            ],
        }
    ]

    while True:
        user_input = input("Vous: ")
        if user_input.lower() in ("quit", "exit", "q"):
            print("Assistant: À bientôt 👋")
            break

        # Ajouter le message utilisateur à l'historique
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_input,
                },
            ],
        })

        # Appel au modèle GitHub
        response = client.chat.completions.create(
            messages=messages,
            model="openai/gpt-5",      # ou un autre modèle GitHub
            reasoning_effort="medium", # optionnel selon le modèle
        )

        assistant_message = response.choices[0].message
        content = response.choices[0].message.content

        # Récupérer le texte de la réponse
        text_parts = []
        for part in assistant_message.content:
            if isinstance(content, str):
                assistant_text = content
            else:
                assistant_text = "\n".join(
                part.text for part in content
            if hasattr(part, "type") and part.type == "text"
            )

        print("Assistant:", assistant_text)
        print()

        # Ajouter la réponse du modèle à l'historique
        messages.append({
            "role": "assistant",
            "content": assistant_message.content,
        })

if __name__ == "__main__":
    main()
