from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model path
model_path = os.path.join(os.path.dirname(__file__), "model_output")

# Load model and tokenizer
model = GPT2LMHeadModel.from_pretrained(model_path, local_files_only=True)
tokenizer = GPT2Tokenizer.from_pretrained(model_path, local_files_only=True)

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def ask_question(question: str):
    prompt = f"Question: {question}\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    outputs = model.generate(
        **inputs,
        max_length=inputs["input_ids"].shape[1] + 64,
        do_sample=True,
        top_p=0.95,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id
    )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract only the answer
    if "Answer:" in decoded:
        answer = decoded.split("Answer:")[1].strip()
    else:
        answer = decoded.strip()

    return answer

if __name__ == "__main__":
    logger.info("Model is ready. Type a question.")
    while True:
        user_input = input("Question (type 'exit' to quit): ")
        if user_input.lower() in ["q", "exit", "quit"]:
            break
        try:
            response = ask_question(user_input)
            print(f"Answer: {response}\n")
        except Exception as e:
            logger.error(f"Error while generating answer: {e}")
