import gradio as gr
from reason import assess_fraud

css = """
.app-title {
    margin: 1rem auto;
    text-align: center;
}

.outer-container {
    gap: 3rem;
}

.main-col-one, .main-col-two {
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
    opacity: 0.6;
}

.input-elem-col-one {
    gap: 0;
}

.custom-input-elem-one span {
    display: none;
}

.custom-input-elem-one input {
    border-radius: 6px !important;
}

.custom-input-elem-one input::-webkit-outer-spin-button,
.custom-input-elem-one input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

.custom-input-elem-one input[type=number] {
    -moz-appearance: textfield;
}

div:has(.custom-input-elem-one), div:has(.custom-input-two), .custom-input-elem-one, .custom-input-two {
    padding: 0;
    margin: 0;
    border: none;
    background: none;
}

.custom-input-two {
    display: flex;
    justify-content: center;
}

.custom-input-two input[type=checkbox] {
    height: 1.5rem;
    width: 1.5rem;
    border-width: 2px;
}

.button-row {
    margin: 3rem auto;
}

.fraud-button {
    font-weight: 700;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    font-size: 1.15rem;
    width: 100%;
    max-width: 500px;
    display: block;
    margin: 0 auto;
    transition: 0.3s ease;
}

.fraud-button:hover,
.fraud-button:focus {
    outline: none;
    box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}

@media screen and (max-width: 600px) {
    .fraud-button {
        width: 100%;
        max-width: 100%;
    }

    .custom-input-two {
        justify-content: flex-start !important;
    }
}

.output-box textarea {
    font-size: 1rem;
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
                    transactionAmount = gr.Number(value=None, elem_classes="custom-input-elem-one")

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Customer Median Spend ($)", elem_classes="input-elem-header")
                    gr.Markdown("This customer’s typical (median) purchase amount. Used to detect unusual spending.", elem_classes="input-elem-desc")
                with gr.Column():
                    customerMedianSpend = gr.Number(value=None, elem_classes="custom-input-elem-one")

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Distance From Home (km)", elem_classes="input-elem-header")
                    gr.Markdown("How far the customer was from their registered address when the transaction occurred.", elem_classes="input-elem-desc")
                with gr.Column():
                    distanceFromHome = gr.Number(value=None, elem_classes="custom-input-elem-one")

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Distance From Last Transaction (km)", elem_classes="input-elem-header")
                    gr.Markdown("Distance between this transaction and the customer's previous one, in kilometers. Helps detect impossible travel.", elem_classes="input-elem-desc")
                with gr.Column():
                    distanceFromLastTransaction = gr.Number(value=None, elem_classes="custom-input-elem-one") 
                

        with gr.Column(elem_classes="main-col-two"):
            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Repeat Retailer", elem_classes="input-elem-header")
                    gr.Markdown("Has the customer made purchases from this merchant before?", elem_classes="input-elem-desc")
                with gr.Column():
                    repeatRetailer = gr.Checkbox(label="", elem_classes="custom-input-two") 

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Used Chip", elem_classes="input-elem-header")
                    gr.Markdown("Was the transaction done using the credit card's chip (EMV) instead of swipe or manual entry?", elem_classes="input-elem-desc")
                with gr.Column():
                    usedChip = gr.Checkbox(label="", elem_classes="custom-input-two")

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Used PIN", elem_classes="input-elem-header")
                    gr.Markdown("Was a PIN number entered during the transaction?", elem_classes="input-elem-desc")
                with gr.Column():
                    usedPin = gr.Checkbox(label="", elem_classes="custom-input-two")

            with gr.Row(elem_classes="input-elem-row"):
                with gr.Column(elem_classes="input-elem-col-one"):
                    gr.Markdown("Online Order", elem_classes="input-elem-header")
                    gr.Markdown("Was this transaction placed through an online store (e.g. e-commerce, app)?", elem_classes="input-elem-desc")
                with gr.Column():
                    onlineOrder = gr.Checkbox(label="", elem_classes="custom-input-two") 

    with gr.Row(elem_classes="button-row"):
                checkFraud = gr.Button("Check for Fraud", elem_classes="fraud-button")
    
    with gr.Row():
        output_box = gr.Textbox(label="Output", lines=3, elem_classes="output-box")
        checkFraud.click(
                    fn=assess_fraud,
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
