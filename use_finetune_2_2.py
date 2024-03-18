import os
import json
import pickle
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict


def json2prompt(messages: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    messages = messages["messages"]
    messages = messages[:2]
    return messages


if __name__ == "__main__":
    load_dotenv()

    with open("./jsonl/test_data_epoch3.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f]

    prompts = []
    answers = []

    for messages in dataset:
        prompts.append(json2prompt(messages))

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    cnt = 0
    for prompt in prompts:
        if cnt % 5 == 0:
            print(f"Asked {cnt} questions.")
        completion = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:personal::923ykW6r", messages=prompt
        )
        answers.append(completion.choices[0].message.content)
        cnt += 1

    pickle.dump(
        {"prompts": prompts, "answers": answers},
        open("test_chat_epoch2_2.pickle", "wb"),
    )
