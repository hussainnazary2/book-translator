from llama_cpp import Llama

# Path to your downloaded GGUF model
model_path = "./models/Mistral-7B-Instruct-v0.3.Q4_K_M.gguf"
# Initialize the model
llm = Llama(
    model_path=model_path,
    n_ctx=512,        # You can increase this if needed
    n_threads=8,      # Use as many CPU threads as your system allows
    verbose=True      # Optional: Shows loading logs
)

# Ask a simple test prompt
prompt = "Q: What is the capital of France?\nA:"
response = llm(prompt, max_tokens=64)

# Print output
print("\n=== Response ===")
print(response["choices"][0]["text"].strip())
