from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

print("Loading model...")

# Load tokenizer + model from local folder
tokenizer = AutoTokenizer.from_pretrained("models/llm")

model = AutoModelForSeq2SeqLM.from_pretrained(
    "models/llm",
    torch_dtype=torch.float32,   # stable on CPU
    device_map="cpu"
)

# 🔍 Sanity checks
print("Model type:", model.config.model_type)
print("Vocab size:", model.config.vocab_size)


def generate(text):
    inputs = tokenizer(text, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_length=60,
        do_sample=False   # ❗ deterministic (VERY IMPORTANT)
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# =========================
# TESTS
# =========================
print("\nRunning tests...\n")

print("Test 1:")
print(generate("Translate English to Hindi: Hello, how are you?"))

print("\nTest 2:")
print(generate("What is machine learning?"))

print("\nTest 3:")
print(generate("Summarize: Machine learning is a field of artificial intelligence."))

print("\nDONE")