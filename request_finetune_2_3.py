import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

res = client.fine_tuning.jobs.create(
    training_file="file-0P73viR5ET912p73zCgKrUFw",  # train_data_epoch3.jsonl
    validation_file="file-gdRhYHElAfLjYnWhwkLp1aA9",  # test_data_epoch3.jsonl
    model="ft:gpt-3.5-turbo-0125:personal::923ykW6r",
    hyperparameters={"n_epochs": 1},
)
f = open("ft_req_2_3_info.txt", "w")
f.write(str(res))
f.close()
