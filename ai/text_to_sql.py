import os
import json
from groq import Groq
from dotenv import load_dotenv
from .sql_instructions import SQL_PROMPT

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_sql(question, dialect, model_name):

    prompt = f"""
{SQL_PROMPT}

SQL Dialect:
{dialect}

User Question:
{question}
"""

    try:

        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        result = response.choices[0].message.content.strip()

        try:

            return json.loads(result)

        except Exception:

            return {
                "query": result,
                "explanation": "SQL generated successfully."
            }

    except Exception as e:

        return {
            "query": "",
            "explanation": f"Error: {str(e)}"
        }