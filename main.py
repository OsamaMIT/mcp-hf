import gradio as gr
def ai_agent_interface(input_text):
    # Replace this with your AI agent logic
    response = f"AI Agent received: {input_text}"
    return response

iface = gr.Interface(
    fn=ai_agent_interface,
    inputs=gr.Textbox(lines=2, placeholder="Enter your message here..."),
    outputs=gr.Textbox(),
    title="AI Agent Interface",
    description="Interact with the AI agent using this Gradio app."
)

if __name__ == "__main__":
    iface.launch()