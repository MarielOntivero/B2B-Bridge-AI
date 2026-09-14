import gradio as gr


companies = [
    {
        "name": "RoboFactory GmbH",
        "industry": "Industrial Automation",
        "needs": "Robotics, automation and machine vision",
        "market": "Germany",
    },
    {
        "name": "GreenGrid Energy",
        "industry": "Energy Technology",
        "needs": "Industrial energy management and automation",
        "market": "Europe",
    },
    {
        "name": "MedTech Solutions",
        "industry": "Medical Technology",
        "needs": "AI, automation and intelligent manufacturing",
        "market": "Germany",
    },
]


def find_matches(product, industry, market):
    results = []

    for company in companies:
        score = 50
        reasons = []

        if industry.lower() in company["industry"].lower():
            score += 25
            reasons.append("Strong industry fit")

        if market.lower() in company["market"].lower():
            score += 15
            reasons.append("Geographic fit")

        if not reasons:
            reasons.append("Potential strategic fit")

        score = min(score, 100)

        results.append(
            f"### {company['name']}\n"
            f"*Match Score: {score}/100*\n\n"
            f"*Industry:* {company['industry']}\n\n"
            f"*Why this could be an opportunity:*\n"
            f"- {', '.join(reasons)}\n\n"
            f"*Potential need:* {company['needs']}\n"
        )

    return "\n\n---\n\n".join(results)


demo = gr.Interface(
    fn=find_matches,
    inputs=[
        gr.Textbox(
            label="What does your company sell?",
            placeholder="Example: Industrial automation software"
        ),
        gr.Textbox(
            label="Target industry",
            placeholder="Example: Industrial Automation"
        ),
        gr.Textbox(
            label="Target market",
            placeholder="Example: Germany"
        ),
    ],
    outputs=gr.Markdown(label="Potential B2B Opportunities"),
    title="B2B Bridge AI",
    description="From thousands of companies to the few that matter.",
)


demo.launch()
