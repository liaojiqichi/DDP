from vllm import LLM, SamplingParams
from datasets import load_dataset
import random
import time
import requests
import json

dataset = load_dataset("nateraw/parti-prompts")

dataset2 = load_dataset("succinctly/midjourney-prompts")

#llm=LLM(model="facebook/opt-125m")
a=0
#print(dataset)
while True:

    random_choose1=random.randint(0,1600)

    sentence1=dataset["train"]["Prompt"][random_choose1].split()
        
    #length_1=len(dataset["train"]["Prompt"][random_choose1])

    #len1=random.randint(int(len(sentence1)/2),len(sentence1))

    #part1=random.choices(sentence1,k=len1)
   
   # print(sentence1)
    #print(part1)
#SENTENCE 2
    random_choose3=random.randint(0,1600)

    sentence3=dataset["train"]["Prompt"][random_choose3].split()

    #length_3=len(dataset["train"]["Prompt"][random_choose3])

    #len3=random.randint(int(len(sentence3)/2),len(sentence3))

    #part3=random.choices(sentence3,k=len3)

#print(dataset2)
    
    random_choose2=random.randint(0,12320)

    sentence2=dataset2["test"]["text"][random_choose2].split()
    
    #length_2=len(dataset2["test"]["text"][random_choose2])

    #len2=random.randint(int(len(sentence2)/2),len(sentence2))

   # part2=random.choices(sentence2,k=len2)
#sentence 4
   # random_choose4=random.randint(0,12320)

    sentence4=dataset2["test"]["text"][random_choose2].split()

  #  length_4=len(dataset2["test"]["text"][random_choose2])

 #   len4=random.randint(int(len(sentence4)/2),len(sentence4))

#    part4=random.choices(sentence4,k=len4)
   
    #prompts=' '.join(part1+part2+part3+part4+sentence2)
   
    prompts=' '.join(sentence1+sentence2+sentence3+sentence4)
   # print("finish")
   # if len(prompts)<200:
    prompts =''.join(prompts+prompts)
    #    continue
    if len(prompts)<300:
        
        prompts =''.join(prompts+prompts)
   

    prompts =''.join(prompts+prompts)

    prompts =''.join(prompts+prompts)
    print(prompts)
    print("\n")   
    with open(r'/DDP/prompts.txt', 'a+') as fp:
        fp.write("%d\n" %a)
        fp.write("%s\n" %prompts)
    fp.close()

#print(part2)

    #print(sentence2)

#    prompts=' '.join(part1+part2)

    headers = {"Content-Type": "application/json"}

    url="http://0.0.0.0:8000/v1/chat/completions"

    da = {
            "model": "meta-llama/Llama-2-7b-chat-hf",
            "messages": [
                    {"role": "system", "content": prompts},
                    {"role": "user", "content": prompts}
                ],
            "temperature": 0
        }


    res = requests.post(url, headers=headers, data=json.dumps(da))
    
    print(res.text)     
    print('\n')
