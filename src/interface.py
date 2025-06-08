import gradio as gr

def detect_fraud(transaction_amount, median_spend, dist_home, dist_last, repeat, chip, pin, online):
    try:
        # Validate inputs
        required_inputs = [transaction_amount, median_spend, dist_home, dist_last]
        if any(val is None for val in required_inputs):
            return "Please fill in all numeric fields before submitting."

        if any(val < 0 for val in required_inputs):
            return "Negative values are not allowed for distances or amounts."

        if not (0 <= repeat <= 1) or not (0 <= chip <= 1) or not (0 <= pin <= 1) or not (0 <= online <= 1):
            return "One of the binary fields is outside the expected range (0-1)."

        # If all good, proceed
        print("Got values:", transaction_amount, median_spend, dist_home, dist_last, repeat, chip, pin, online)
        return f"Input accepted.\nAmount: {transaction_amount}, Median: {median_spend}, etc."
    
    except Exception as e:
        return f"An error occurred: {str(e)}"


css = """
:root {
    --primary-color: rgba(0, 0, 0, 1);
    --secondary-color: rgba(255, 255, 255);
    --tertiary-color: rgba(0, 0, 0, 0.5);
}

.app-title {
    text-align: center;
    margin-bottom: 1rem;
}

.outer-container {
    gap: 2.5rem;
}

.main-col-one {
    gap: 3rem;
}

.input-elem-row {
    align-items: center;
    gap: 2rem;
}

.input-elem-header p {
    font-weight: 700;
    font-size: 1.15rem;
}

.input-elem-desc p {
    font-size: 0.9rem;
    color: var(--tertiary-color);
}

.input-elem-col-one {
    gap: 0;
}

.custom-input-elem-one {
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
    background: transparent !important;
}

.custom-input-elem-one span {
    display: none;
}

.custom-input-elem-two input[type=number],
.custom-input-elem-two button,
.custom-input-elem-two .wrap label {
    display: none !important;
}

.custom-input-elem-one input[type=number] {
    border: 1px solid #000 !important;
    border-bottom-width: 3px !important;
    border-radius: 6px !important;
}

.custom-input-elem-one input[type=number]:focus {
    outline: none !important;
    box-shadow: none !important;
    border-color: var(--primary-color) !important;
}

.custom-input-elem-two {
    all: unset;
    display: flex;
    flex-direction: column;
    background-color: white;
}

.custom-input-elem-two .head[class*="svelte-"] {
    display: none !important;
}

.form[class*="svelte-"] {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

.custom-input-elem-two .wrap {
    border: none !important;
}

.custom-input-elem-two input[type=range] {
    appearance: none !important;
    display: block;
    width: 100% !important;
    max-width: none;
    height: 1.75rem !important;
    background: var(--secondary-color) !important;
    border-radius: 1.75rem !important;
    border: 1px solid var(--primary-color) !important;
    padding: 0.25rem 0.15rem 0.3rem !important;
    cursor: pointer !important;
    transition: background 0.3s ease-in-out;
}

.custom-input-elem-two input[type=range]::-webkit-slider-runnable-track {
    width: 3.25rem !important;
    background: transparent !important;    
    border: none !important;
    margin: 0 !important;
}

.custom-input-elem-two input[type=range]::-moz-range-track {
    background: transparent !important;
    border: none !important;
}

.custom-input-elem-two input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 1.25rem;
    height: 1.25rem;
    background: var(--primary-color);
    border-radius: 50%;
    transition: transform 0.3s ease;    
    z-index: 10;
}

.custom-input-elem-two input[type=range]::-moz-range-thumb {
    width: 1.25rem;
    height: 1.25rem;
    background: var(--primary-color);
    border-radius: 50%;
    border: none;
    transition: transform 0.3s ease;
    z-index: 10;
}

.custom-input-elem-two .slider_input_container span {
    display: none;
}

.fraud-button {
    background-color: var(--primary-color);
    color: var(--secondary-color);
    font-weight: 700;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    font-size: 1.15rem;
    max-width: 60%;
    display: block;
    margin: 0 auto;
    transition: 0.3s ease;
}

.fraud-button:hover,
.fraud-button:focus {
    outline: none;
    background-color: var(--secondary-color);
    color: var(--primary-color);
    box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}

.input-elem-row > .gr-box {
    flex: 1;
    min-width: 0;
}

.custom-input-elem-two {
    width: 100%;
    max-width: 3.25rem;
}

@media screen and (max-width: 600px) {
    .fraud-button {
        width: 100%;
    }
}

.output-box textarea {
    font-size: 1rem;
    color: black;
}

"""


with gr.Blocks(theme=gr.themes.Base(font=[gr.themes.GoogleFont("Rubik"), "Arial", "sans-serif"]), css=css) as demo:
    gr.Markdown("# AI-Powered Fraud Detection for Merchants & Analysts", elem_classes="app-title")
    with gr.Row(elem_classes="outer-container"):
        with gr.Column(elem_classes="main-col-one"):
            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Transaction Amount ($)", elem_classes="input-elem-header")
                    gr.Markdown("The total amount of the transaction in US dollars", elem_classes="input-elem-desc")
                with gr.Column():
                    transactionAmount = gr.Number(elem_classes="custom-input-elem-one")

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Customer Median Spend ($)", elem_classes="input-elem-header")
                    gr.Markdown("This customer’s typical (median) purchase amount. Used to detect unusual spending.", elem_classes="input-elem-desc")
                with gr.Column():
                    customerMedianSpend = gr.Number(elem_classes="custom-input-elem-one")

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Distance From Home (km)", elem_classes="input-elem-header")
                    gr.Markdown("How far the customer was from their registered address when the transaction occurred.", elem_classes="input-elem-desc")
                with gr.Column():
                    distanceFromHome = gr.Number(elem_classes="custom-input-elem-one")

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Distance From Last Transaction (km)", elem_classes="input-elem-header")
                    gr.Markdown("Distance between this transaction and the customer's previous one, in kilometers. Helps detect impossible travel.", elem_classes="input-elem-desc")
                with gr.Column():
                    distanceFromLastTransaction = gr.Number(elem_classes="custom-input-elem-one") 

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Repeat Retailer", elem_classes="input-elem-header")
                    gr.Markdown("Has the customer made purchases from this merchant before?", elem_classes="input-elem-desc")
                with gr.Column():
                    repeatRetailer = gr.Slider(minimum=0, maximum=1, value=0, step=1, elem_classes="custom-input-elem-two") 

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Used Chip", elem_classes="input-elem-header")
                    gr.Markdown("Was the transaction done using the credit card's chip (EMV) instead of swipe or manual entry?", elem_classes="input-elem-desc")
                with gr.Column():
                    usedChip = gr.Slider(minimum=0, maximum=1, value=0, step=1, elem_classes="custom-input-elem-two")

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Used PIN", elem_classes="input-elem-header")
                    gr.Markdown("Was a PIN number entered during the transaction?", elem_classes="input-elem-desc")
                with gr.Column():
                    usedPin = gr.Slider(minimum=0, maximum=1, value=0, step=1, elem_classes="custom-input-elem-two")

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Online Order", elem_classes="input-elem-header")
                    gr.Markdown("Was this transaction placed through an online store (e.g. e-commerce, app)?", elem_classes="input-elem-desc")
                with gr.Column():
                    onlineOrder = gr.Slider(minimum=0, maximum=1, value=0, step=1, elem_classes="custom-input-elem-two")      

            with gr.Row(elem_classes="input-elem-row"):
                checkFraud = gr.Button("Check for Fraud", elem_classes="fraud-button")
                

        with gr.Column():
            output_box = gr.Textbox(label="Output", lines=3, elem_classes="output-box")

        checkFraud.click(
                    fn=detect_fraud,
                    inputs=[
                        transactionAmount,
                        customerMedianSpend,
                        distanceFromHome,
                        distanceFromLastTransaction,
                        repeatRetailer,
                        usedChip,
                        usedPin,
                        onlineOrder
                    ],
                    outputs=output_box
        )


if __name__ == "__main__":
    demo.launch()
