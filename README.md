# AI-Powered Fraud Detection Agent

`agent-demo-track`
**Track:** 3. Agentic Demo Showcase  
**Built For:** [Hugging Face Hackathon - Multimodal Challenge Playground (MCP)](https://huggingface.co/multimodal-challenge)  
**Team:** Muhammed Hisham, Osama Elmahdy

---

## Overview

This Gradio-based AI Agent helps **merchants, analysts, and fraud teams** assess transaction legitimacy by combining a **fraud detection model** with **reasoning capabilities** powered by Hugging Face’s [`Nemotron-Research-Reasoning-Qwen-1.5B-GGUF`](https://huggingface.co/Nemotron-Research/Reasoning-Qwen-1_5B-GGUF) model.

Users input transaction details, and the system:
1. **Classifies the transaction** as fraudulent or not.
2. Uses LLM reasoning to **explain the decision** and provide **recommendations** for next steps (e.g., flag, approve, monitor).

---

## AI Stack

### Core Idea

> First, check if a transaction is likely fraudulent using a traditional ML model trained on real-world features. Then, invoke an open LLM agent (via GGUF + llama-cpp) to explain and suggest human-friendly actions.

### Components Used

- **Fraud Detection:**  
  - Custom-trained classifier (scikit-learn + LIME explanations)
- **Reasoning & Recommendations:**  
  - Hugging Face’s `Nemotron-Research-Reasoning-Qwen-1.5B-GGUF` running locally via `llama-cpp-python`
- **UI:**  
  - Gradio frontend (v5.33.0)

---

## Demo Video

Watch a quick overview and demo of the application here:  
👉 [Click to Watch on YouTube](https://www.youtube.com)


