from llama_cpp import Llama
import pandas as pd
from model import load_model, extract_top_features
 
# load fraud classifier from src/model.py
fraud_model = None
def get_fraud_model():
    global fraud_model
    if fraud_model is None:
        fraud_model = load_model()
    return fraud_model


# initialize the LLM and tokenizer
# using the model from Hugging Face
llm = Llama.from_pretrained(
            repo_id="lmstudio-community/Nemotron-Research-Reasoning-Qwen-1.5B-GGUF",
            filename="Nemotron-Research-Reasoning-Qwen-1.5B-Q4_K_M.gguf",
            verbose=False,
            n_ctx=131072,  # Match training context length
            #n_gpu_layers=24 ## Optional for GPU acceleration
            )

# runs the LLM reasoning
def llm_reason(prompt: str) -> str:
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

    return llm_reason(prompt)



# ─── ENTRYPOINT ───────────────────────────────────────────────────────────────—
def assess_fraud(distanceFromHome, distanceFromLastTransaction, transactionAmount, customerMedianSpend, repeatRetailer, usedChip, usedPin, onlineOrder):
    
    data = {
            "distance_from_home": distanceFromHome,
            "distance_from_last_transaction": distanceFromLastTransaction,
            "ratio_to_median_purchase_price": transactionAmount / customerMedianSpend, # Ratio of purchased price transaction to median purchase price.
            "repeat_retailer": repeatRetailer,
            "used_chip": usedChip,
            "used_pin_number": usedPin,
            "online_order": onlineOrder,
    }
    df_row = pd.DataFrame([data])


    # load data, build context, and await the LLM’s explanation
    explanation = build_and_call_llm(df_row)
    
    parts = explanation.split('</think>', 1)

    if len(parts) > 1:
        after_think = parts[1].strip()
        return(after_think)
    else:
        return("No </think> tag found.")

# if __name__ == "__main__":
#     df = pd.read_csv('src/card_transdata.csv').drop(columns=['fraud']).iloc[0:1] ## Data for testing
#     assess_fraud(df)