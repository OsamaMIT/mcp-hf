import gradio as gr
from src.model import load_model, extract_top_features # imports from model.py
import modal
import pandas as pd

# Fraud classifier
fraud_model = load_model() # Takes a row of data as a dataframe and returns a prediction (0=Normal or 1=Fraud)


def is_fradulent(transaction_data):
    """
    Predicts if a transaction is fraudulent or not.
    
    Args:
        transaction_data (pd.DataFrame): A single row DataFrame containing transaction features.
        
    Returns:
        str: Prediction result and top feature contributions.
    """
    prediction = fraud_model.predict(transaction_data)
    top_features = extract_top_features(transaction_data, top_n=3)
    
    return f"Anomaly Model Prediction: {'Fraud' if prediction[0] == 1 else 'Normal'}\nTop Contributing Features:\n{top_features}"


app = modal.App("mcp-hf")
image = (
    modal.Image.debian_slim()
         .pip_install_from_requirements("requirements.txt")
)

@app.function(gpu="T4", image=image)
def llm_reason(data=""):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    model_name = "TheFinAI/Fin-o1-8B"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    input_text = f"Analyze the following transaction data:\n{data}\n\
        Explain the following classification results produced by the LIME python module: \n\
        {is_fradulent(data)}"\
    

    inputs = tokenizer(input_text, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=200)
    print(tokenizer.decode(output[0], skip_special_tokens=True))


# def ai_agent_interface(data):
#     # Replace this with your AI agent logic
#     response = f"AI Agent received: {data}"
#     return response

# iface = gr.Interface(
#     fn=ai_agent_interface,
#     inputs=gr.Textbox(lines=2, placeholder="Enter your message here..."),
#     outputs=gr.Textbox(),
#     title="AI Agent Interface",
#     description="Interact with the AI agent using this Gradio app."
# )

##TEMPORARY EXAMPLE UNTIL UI IS INTERACTIVE:
df = pd.read_csv('card_transdata.csv').drop(columns=['fraud'])
example_transaction = df.iloc[0:1] # example row of data to test the system

@app.local_entrypoint()
def main():
    print("Starting the LLM reasoning process...")
    llm_reason.remote(example_transaction)

# if __name__ == "__main__":
#     iface.launch(share=True)