from llama_cpp import Llama
import gradio as gr
import pandas as pd
import modal
import torch # to automate inclusion in requirements.txt for transformers
from model import load_model, extract_top_features

# modal app configuration
app = modal.App("mcp-hf")

# bake in all requirements + src package
image = (
    modal.Image.debian_slim()
         .pip_install_from_requirements("requirements.txt")
         .add_local_python_source("src", copy=True)
)

# load fraud classifier from src/model.py
fraud_model = None
def get_fraud_model():
    global fraud_model
    if fraud_model is None:
        fraud_model = load_model()
    return fraud_model


# initialize the LLM and tokenizer
# using the model from Hugging Face
llm = None

# runs the LLM reasoning on Modal Labs GPU
#@app.function(gpu="T4", image=image)
def llm_reason(prompt: str) -> str:
    global llm, tokenizer
    if llm is None:
        llm = Llama.from_pretrained(
            repo_id="lmstudio-community/Nemotron-Research-Reasoning-Qwen-1.5B-GGUF",
            filename="Nemotron-Research-Reasoning-Qwen-1.5B-Q4_K_M.gguf",
            verbose=False,
            n_ctx=131072,  # Match training context length
            n_gpu_layers=-1  # Use all GPU layers
        )

    output = llm.create_chat_completion(
    	messages = [
    		{
    			"role": "user",
    			"content": prompt
    		}
    	]
    )

    return output["choices"][0]["message"]["content"]

# wrapper to build context and call the LLM
def build_and_call_llm(transaction_df: pd.DataFrame) -> str:
    # 1) get a fraud prediction + top features 
    model = get_fraud_model()
    pred = model.predict(transaction_df)[0]
    feat_str = extract_top_features(transaction_df, top_n=3)

    # 2) assemble a minimal prompt temporarily
    status = "FRAUD" if pred == 1 else "NORMAL"
    prompt = (
        f"Transaction classified as **{status}**.\n"
        f"Top contributing factors according the LIME module:\n{feat_str}\n\n"
        "Please explain why and recommend next investigative steps."
    )

    # 3) call remote LLM
    return llm_reason(prompt) # llm_reason.remote(prompt)


# ─── ENTRYPOINT ───────────────────────────────────────────────────────────────—
#@app.local_entrypoint()
def main():
    # load a sample, build context, and await the LLM’s explanation
    df = pd.read_csv('src/card_transdata.csv').drop(columns=['fraud']).iloc[0:1]
    explanation = build_and_call_llm(df)
    print("Explanation:\n", explanation)

main()