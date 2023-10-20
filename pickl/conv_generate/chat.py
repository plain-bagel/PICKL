import json
from pathlib import Path
from typing import Generator

# pickl package for internal use
from pickl import PROMPT_DIR, TOPIC_DIR
from pickl.conv_generate.model import Bot, User


def chat(bot: Bot, user: User, turns: int, primer: str | None = None) -> list[dict[str, str]]:
    """Converse between Bot and User for a given number of turns."""
    # Reset conversation history
    bot.reset_history()
    user.reset_history()

    # Converse for a given number of turns
    for i in range(turns):
        # 1 turn consists of Bot's response(A) and User's response(B) [A, B]
        # --- Bot(A) responds to User(B) ---
        bot_response = bot.add_bot_response(primer if i == 0 else None)
        user.add_bot_response(bot_response)

        # --- User(B) responds to Bot(A)---
        user_response = user.add_user_response()
        bot.add_user_response(user_response)

    return user.conv_history


def generate_conversations(
    user_url: str,
    bot_system_prompt: str,
    bot_prompt: str,
    turns: int,
    primer_list: list[tuple[str, int, str]],
) -> Generator[dict[str, str | int | list[str] | None], None, None]:
    """Generator function that yields a conversation for each topic and primer."""
    # --- Instantiate Bot and User models ---
    bot = Bot(bot_system_prompt, bot_prompt)
    user = User(user_url)

    # --- Iterate over conversation starters and generate conversations ---
    for topic, idx, primer in primer_list:
        # Generate conversation
        try:
            conversation = chat(bot, user, turns, primer)
            yield {
                "user_url": user_url,
                "topic": topic,
                "idx": idx,
                "convo": [f"{x['speaker']}: {x['message']}" for x in conversation],
            }
        except Exception as e:
            print(f"Error (generate_conversation) - {topic}, {idx}, {primer}: {e}")
            yield {"user_url": user_url, "topic": topic, "idx": idx, "convo": None}


if __name__ == "__main__":
    # --- Create a conversation starter list ---
    with Path(TOPIC_DIR, "sample_data.json").open("r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    primers = [(topic["topic"], idx, primer) for topic in data for idx, primer in enumerate(topic["primer"])]

    # --- Load prompts ---
    sys_prompt = Path(PROMPT_DIR, "bot_model_system.txt").read_text()
    prompt = Path(PROMPT_DIR, "bot_model.txt").read_text()

    # Generation parameters
    test_api_url = "http://127.0.0.1:8000/chatgpt"
    conv_turns = 2

    # --- Generate conversations ---
    # Collect responses from Generator function
    conversation_list = []
    conversations = generate_conversations(test_api_url, sys_prompt, prompt, conv_turns, primers)
    for convo in conversations:
        conversation_list.append(convo)
