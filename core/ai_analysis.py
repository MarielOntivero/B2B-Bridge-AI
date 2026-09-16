import os
import json
from openai import OpenAI


def analyze_opportunity(company, candidate):
    """
    Analyze a potential B2B opportunity using NVIDIA NIM.
    """

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=os.environ["NVIDIA_API_KEY"],
    )

    prompt = f"""
You are the AI analysis engine of B2B Bridge AI.

Analyze whether there is a potential B2B business opportunity
between these two companies.

COMPANY A:
{json.dumps(company, indent=2)}

COMPANY B:
{json.dumps(candidate, indent=2)}

Important rules:
- Use only the information provided.
- Do not invent facts.
- Separate FACTS from AI INTERPRETATION.
- Treat information explicitly present in the company data as a fact.
- Treat conclusions about compatibility or business potential as interpretation.
- Never present an interpretation as a fact.
- Identify which provided facts support the opportunity.
- Look for complementary products, needs, markets and technologies.
- If important information is missing, say so explicitly.

Return ONLY valid JSON.

Use exactly this structure:

{{
  "score": 0,
  "opportunity": "short explanation",
  "evidence": [
    "fact from the provided company data"
  ],
  "reasons": [
    "interpretation based on the evidence"
  ],
  "risks": [
    "risk or missing information"
  ],
  "confidence": "high"
}}
"""

    response = client.chat.completions.create(
        model="deepseek-ai/deepseek-v4-flash-0731",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
        max_tokens=1000,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("NVIDIA returned no final response.")

    return json.loads(content)
