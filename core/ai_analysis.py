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
        timeout=45.0,
        max_retries=0,
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
- Keep the analysis concise.

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
        model="nvidia/nemotron-3.5-lightning-30b-a3b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
        max_tokens=1000,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("NVIDIA returned no final response.")

    content = content.strip()

    if content.startswith("```json"):
        content = content[7:]

    if content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    return json.loads(content.strip())
