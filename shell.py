from vllm import LLM, SamplingParams
from datasets import load_dataset
import random
import time
import requests

dataset = load_dataset("nateraw/parti-prompts")

dataset2 = load_dataset("succinctly/midjourney-prompts")

#llm=LLM(model="facebook/opt-125m")

#print(dataset)
while True:

    random_choose1=random.randint(1,1632)

    sentence1=dataset["train"]["Prompt"][random_choose1].split()

    length_1=len(dataset["train"]["Prompt"][random_choose1])

#print(sentence1)

#print(type(dataset["train"]["Prompt"][random_choose1]))

#print(length_1)

#print(len(sentence1))

    len1=random.randint(0,len(sentence1))

    part1=random.choices(sentence1,k=len1)

#print(dataset2)

    random_choose2=random.randint(1,12320)

    sentence2=dataset2["test"]["text"][random_choose2].split()

    length_2=len(dataset2["test"]["text"][random_choose2])

    len2=random.randint(0,len(sentence2))

    part2=random.choices(sentence2,k=len2)

#print(part2)

#print(sentence2)

    prompts=' '.join(part1+part2)

    url="http://localhost:8000/generate"
	
    da="{
	"prompt":prompt	
	}"    

    res = requests.post(url,data=da)

    print(res.text)    

    time.sleep(1)
