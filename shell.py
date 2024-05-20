from vllm import LLM, SamplingParams
from datasets import load_dataset
import random
import time
import requests
import json
import re
#llm=LLM(model="facebook/opt-125m")

file = open('/DDP/prompts.txt','r')

prompts = ''

Lines = file.readlines()

for line in Lines:

    if len(line)==1 or len(line)==2 or len(line)==3 or len(line)==4:
            
            prompts = ''
            
            continue
  
    prompts=''.join(prompts+line)

    headers = {"Content-Type": "application/json"}

    url="http://0.0.0.0:8000/v1/chat/completions"
    
    da = {
            "model": "meta-llama/Llama-2-7b-chat-hf",
            "messages": [
                    {"role": "system", "content": prompts},
                    {"role": "user", "content": prompts}
                ],
            "tempereture": 0
        }

    print(prompts)

    res = requests.post(url, headers=headers, data=json.dumps(da))


