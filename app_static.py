# user_request =  "Create a quotation for 100 bricks at ₹20 each and 50 bags of cement at ₹300 each for client John."

import re
import pdfkit
import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template, send_file, request
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model = ChatGoogleGenerativeAI(model = 'gemini-2.0-flash', google_api_key = api_key)
wkhtmltopdf_path = os.getenv("WKHTMLTOPDF_PATH")

app = Flask(__name__)

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():

    user_input = request.form["user_input"]

    template = """
        *** Use this information below to provide the output format for the user ***

        I want to generate a quotation PDF. Extract the following information from the input:
        - Client name
        - List of items with name, quantity, unit price, and total
        - Grand total

        The output should be JSON in this format:
        {{
        "quotation_details": {{
            "client": "John Doe",
            "items": [
            {{
                "item_name": "wood",
                "quantity": 10,
                "unit_price": 50,
                "total": 500
            }}
            ],
            "grand_total": 500
        }}
        }}

        Respond ONLY with valid JSON. Do NOT include any explanation or extra text.

        Input: {usermessage}
        """     

    prompt_template = ChatPromptTemplate.from_template(template)

    prompt = prompt_template.invoke({"usermessage": user_input})

    response = model.invoke(prompt)

    try:
        match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
        else:
            print("No valid JSON object found in the response.")

    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)

    quotation_details = data["quotation_details"]

    client_name = quotation_details["client"]

    # Render HTML with data
    html = render_template(
    "quotation.html",
    client=quotation_details["client"],
    items=quotation_details["items"],
    grand_total=quotation_details["grand_total"]
    )

    # Save PDF
    pdf_file = f"{client_name}_quotation.pdf"
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)  # adjust for your OS
    pdfkit.from_string(html, pdf_file, configuration=config)

    # Send the file
    return send_file(pdf_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)