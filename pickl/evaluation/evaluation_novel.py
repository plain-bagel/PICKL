import json
from pathlib import Path
from typing import Any

from pickl import PROMPT_DIR, TOPIC_DIR
from pickl.conv_generate.model import Bot


def evaluate_novel(
    system_prompt: str, novel_prompt: str, conv1: str, conv2: str, reps: int = 2
) -> dict[str, str | Any]:
    """Run comparison for 'reps' number of times"""
    results = []
    for i in range(reps):
        # Add conversations to prompt template
        # Switch order of conversations every other time - Reduce positional bias
        prompt = novel_prompt.replace("{{conv1}}", conv1 if i % 2 == 0 else conv2)
        prompt = prompt.replace("{{conv2}}", conv2 if i % 2 == 0 else conv1)

        # Query GPT-4 with conversation comparison payload
        chatgpt = Bot(system_prompt, prompt)
        response = chatgpt.generate_response(temperature=0, return_json=True)
        result = response["result"]

        # Append results to list according to order
        if i % 2 == 0:
            results.append(result)
        else:
            result = ("Draft 2" if result == "Draft 1" else "Draft 1") if result in ["Draft 1", "Draft 2"] else "Both"
            results.append(result)

    # Determine winner
    if results[0] == results[1]:
        winner_conv = results[0]
    elif "Both" in results:
        if "Draft 1" in results:
            winner_conv = "Draft 1"
        else:
            winner_conv = "Conversation 2"
    else:
        winner_conv = "Both"

    # Match wording
    if winner_conv == "Draft 1":
        winner_conv = "Conversation 1"
    elif winner_conv == "Draft 2":
        winner_conv = "Conversation 2"
    else:
        winner_conv = "Tie"

    return {
        "winner_conv": winner_conv,
    }


if __name__ == "__main__":
    # Prepare Conversation pair
    with Path(TOPIC_DIR, "sample_data.json").open() as f:
        data = json.load(f)

    conversation1 = "\n".join(data[0]["conversations"][0])
    conversation2 = "\n".join(data[0]["conversations"][1])

    # Load Prompts
    sys_prompt = Path(PROMPT_DIR, "evaluation_system.txt").read_text()
    nov_prompt = Path(PROMPT_DIR, "evaluation_novel.txt").read_text()

    nov_result = evaluate_novel(sys_prompt, nov_prompt, conversation1, conversation2)
