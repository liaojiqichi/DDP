from datasets import load_dataset
from transformers import AutoTokenizer
import numpy as np
import os
from datasets import concatenate_datasets
import argparse
from transformers
from datasets import load_from_disk
import torch
import evaluate

from transformers import AutoTokenizer, TrainingArguments, Trainer, AutoModelForCausalLM, IntervalStrategy, DataCollatorWithPadding


torch.manual_seed(42)

dataset = load_dataset("BookCorpus")

train_size = int(0.9 * len(dataset))

train_dataset, val_dataset = random_split(dataset, [train_size, len(dataset) - train_size])

tokenizer = AutoTokenizer.from_pretrained("facebook/opt-125m")

train = tokenizer(train_dataset)

val = tokenizer(train_dataset)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

training_args = TrainingArguments(output_dir='./results', num_train_epochs=4.3, logging_steps=100, save_strategy=IntervalStrategy.NO,
                                  per_device_train_batch_size=15, per_device_eval_batch_size=15, warmup_steps=100,
                                  weight_decay=0.01, logging_dir='./logs', fp16=True, deepspeed='./ds_config_gpt_j.json')

model = AutoModelForCausalLM.from_pretrained("facebook/opt-125m")


Trainer(model=model, args=training_args, train_dataset=train,
        eval_dataset=val, data_collator=data_collator, tokenizer=tokenizer).train()

tokenizer.save_pretrained(output_dir)
trainer.create_model_card()



