import json
import os
import sys

import gradio as gr

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ai_analysis import analyze_opportunity


def analyze_b2b_opportunity(
    company_a_name,
    company_a_products,
    company_a_industry,
    company_a_country,
    company_b_name,
):
    company_a = {
        "name": company_a_name,
        "products": [company_a_products],
        "industry": company_a_industry,
        "country": company_a_country,
    }

    with open("data/companies.json", "r") as file:
        companies = json.load(file)

    candidate = companies[0]

    result = analyze_opportunity(company_a, candidate)

    evidence = "\n".join(
        f"- {item}" for item in result.get("evidence", [])
    )

    reasons = "\n".join(
        f"- {item}" for item in result.get("reasons", [])
    )

    risks = "\n".join(
        f"- {item}" for item in result.get("risks", [])
    )

    return f"""
# Opportunity Score: {result.get("score", "N/A")}/100

**AI Confidence:** {result.get("confidence", "N/A")}

## Potential Opportunity

{result.get("opportunity", "No analysis available.")}

## Evidence

{evidence}

## Why this could be an opportunity

{reasons}

## Risks & Missing Information

{risks}

---

*Analysis powered by NVIDIA NIM.*
"""


demo = gr.Interface(
    fn=analyze_b2b_opportunity,
    inputs=[
        gr.Textbox(
            label="Company A",
            placeholder="Example: My Automation Company",
        ),
        gr.Textbox(
            label="What does Company A sell?",
            placeholder="Example: Industrial automation software",
        ),
        gr.Textbox(
            label="Company A industry",
            placeholder="Example: Industrial Automation",
        ),
        gr.Textbox(
            label="Company A country",
            placeholder="Example: Germany",
        ),
        gr.Textbox(
            label="Company B",
            value="RoboFactory GmbH",
            interactive=False,
        ),
    ],
    outputs=gr.Markdown(
        label="B2B Opportunity Analysis"
    ),
    title="B2B Bridge AI",
    description=(
        "From thousands of companies to the few that matter. "
        "Analyze potential B2B opportunities using NVIDIA AI."
    ),
)


demo.launch()
