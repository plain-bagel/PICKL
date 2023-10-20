import json
from pathlib import Path

from pickl import PROMPT_DIR, TOPIC_DIR
from pickl.conv_generate.model import Bot


# Type aliases
ScoreTypes = dict[str, int]


def evaluate_base(
    system_prompt: str,
    prompt: str,
    conv1: str,
    conv2: str,
    reps: int = 2,
) -> dict[str,]:
    """Run comparison for 'reps' number of times"""
    results: dict[str, list[ScoreTypes]] = {"conv1": [], "conv2": []}
    for i in range(reps):
        # Add conversations to prompt template
        # Switch order of conversations every other time - Reduce positional bias
        base_prompt = prompt.replace("{{conv1}}", conv1 if i % 2 == 0 else conv2)
        base_prompt = base_prompt.replace("{{conv2}}", conv2 if i % 2 == 0 else conv1)

        # Query ChatGPT with conversation comparison payload
        chatgpt = Bot(system_prompt, base_prompt)
        response = chatgpt.generate_response(temperature=0, return_json=True)

        # Check if results are valid
        for _key, result in response.items():
            result["understandable"] = max(min(result["understandable"], 1), 0)
            result["natural"] = max(min(result["natural"], 3), 1)
            result["maintains_context"] = max(min(result["maintains_context"], 3), 1)
            result["conciseness"] = max(min(result["conciseness"], 3), 1)
            result["overall_quality"] = max(min(result["overall_quality"], 5), 1)

        conv1_res = response["conversation1"]
        conv2_res = response["conversation2"]

        # Append results to list according to order
        results["conv1"].append(conv1_res) if i % 2 == 0 else results["conv1"].append(conv2_res)
        results["conv2"].append(conv2_res) if i % 2 == 0 else results["conv2"].append(conv1_res)

    # --- Calculate scores ---
    score_keys = ["understandable", "natural", "maintains_context", "conciseness", "overall_quality"]
    conv1_score: dict[str, int] = {key: sum([res[key] for res in results["conv1"]]) for key in score_keys}
    conv2_score: dict[str, int] = {key: sum([res[key] for res in results["conv2"]]) for key in score_keys}

    # Sum individual scores to get final score
    conv1_final_score = sum(conv1_score.values())
    conv2_final_score = sum(conv2_score.values())

    # Determine winner
    if conv1_final_score > conv2_final_score:
        winner_conv = "Conversation 1"
    elif conv1_final_score < conv2_final_score:
        winner_conv = "Conversation 2"
    else:
        winner_conv = "Tie"

    return {
        "conv1": conv1_score,
        "conv2": conv2_score,
        "winner_conv": winner_conv,
    }


if __name__ == "__main__":
    # --- Load Prompts ---
    sys_prompt = Path(PROMPT_DIR, "evaluation_system.txt").read_text()
    b_prompt = Path(PROMPT_DIR, "evaluation_base.txt").read_text()

    # --- Load Conversations ---
    with Path(TOPIC_DIR, "sample_data.json").open() as f:
        data = json.load(f)

    conversation1 = "\n".join(data[0]["conversations"][0])
    conversation2 = "\n".join(data[0]["conversations"][1])

    # --- Evaluate base prompt ---
    base_results = evaluate_base(sys_prompt, b_prompt, conversation1, conversation2)
