from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
tokenizer.pad_token = tokenizer.eos_token

# Tokenize the data
def tokenize(example):
    prompt = f"Question: {example['question']}\nAnswer:"
    full_text = prompt + " " + example["answer"].replace("<|endoftext|>", "").strip()
    tokenized = tokenizer(full_text, truncation=True, padding="max_length", max_length=512)
    
    # Important: for causal LM, "labels" must be set like this to avoid padding loss
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

# Load and process the dataset
dataset = load_dataset("json", data_files="llm_finetune/model_output/qa_data.json")
tokenized_dataset = dataset["train"].map(tokenize, remove_columns=dataset["train"].column_names)

# Prepare the model
model = AutoModelForCausalLM.from_pretrained("gpt2-medium")
model.resize_token_embeddings(len(tokenizer))  # Important if tokenizer.pad_token was added

# Training settings
args = TrainingArguments(
    output_dir="llm_finetune/model_output",
    per_device_train_batch_size=2,   # safer for GPU memory
    num_train_epochs=5,
    logging_steps=10,
    save_steps=100,
    save_total_limit=1,
    remove_unused_columns=False,
    fp16=True,  # keep this True if GPU supports
    report_to="none"  # disables wandb or other loggers
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
)

# Start training
trainer.train()

# Save the model and tokenizer
model.save_pretrained("llm_finetune/model_output")
tokenizer.save_pretrained("llm_finetune/model_output")

print("✅ Model trained and saved")
