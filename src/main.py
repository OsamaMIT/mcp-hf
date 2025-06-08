import gradio as gr
import pandas as pd
import modal
import torch # to automate inclusion in requirements.txt for transformers
from src.model import load_model, extract_top_features
from transformers import AutoModelForCausalLM, AutoTokenizer

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
tokenizer = None
MODEL_NAME = "TheFinAI/Fin-o1-8B"

# runs the LLM reasoning on Modal Labs GPU
@app.function(gpu="T4", image=image)
def llm_reason(context: str) -> str:
    global llm, tokenizer
    if llm is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        llm = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    inputs = tokenizer(context, return_tensors="pt")
    outputs = llm.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

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
    return llm_reason.remote(prompt)


# ─── ENTRYPOINT ───────────────────────────────────────────────────────────────—
@app.local_entrypoint()
def main():
    # load a sample, build context, and await the LLM’s explanation
    df = pd.read_csv('src/card_transdata.csv').drop(columns=['fraud']).iloc[0:1]
    explanation = build_and_call_llm(df)
    print("LLM Explanation:\n", explanation)
