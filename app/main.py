import gradio as gr

def analyze_company(company):
    return f"Analyzing: {company}"

demo = gr.Interface(
    fn=analyze_company,
    inputs=gr.Textbox(label="Company"),
    outputs=gr.Textbox(label="B2B Bridge AI Analysis"),
    title="B2B Bridge AI",
    description="From thousands of companies to the few that matter."
)

demo.launch()
