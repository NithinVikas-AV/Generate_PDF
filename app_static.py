"""
Example Prompt:

Create a quotation for client Priya Sharma from GreenBuild Solutions located at 45 Industrial Estate, Bengaluru. Their contact number is +91-9123456780.

They want:

200 steel rods at ₹150 each

75 concrete slabs at ₹450 each

25 liters of paint at ₹120 each

https://wkhtmltopdf.org/downloads.html

"""


import re
import pdfkit
import json
import os
import uuid
from datetime import datetime
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
    action = request.form["action"]

    
    template = """

        ** Use this information below to provide the output format for the user ***

        You are an intelligent assistant helping generate a quotation.  
        Your task is to extract structured details from the user's request in the exact JSON format described below.

        From the input, extract:

        - client → the client's full name  
        - company → the client's company name  
        - address → the full address  
        - phone → the phone number  
        - items → list of items (each item includes item_name, quantity, unit_price, total)  
        - item_total → sum of all item totals  
        - tax → 18% GST on item_total  
        - grand_total → item_total + tax

        Rules:
        - Do NOT add any explanation, comments, or extra text.
        - Format strictly as valid JSON.

        ### Expected JSON Output Format:

        {{
        "quotation_details": {{
            "client": "Full Name",
            "company": "Company Name",
            "address": "Full Address",
            "phone": "+91-XXXXXXXXXX",
            "items": [
            {{
                "item_name": "Item A",
                "quantity": 10,
                "unit_price": 50,
                "total": 500
            }},
            ...
            ],
            "item_total": 500,
            "tax": 90.0,
            "grand_total": 590.0
        }}
        }}

        Now extract the information from this input:

        Input: {usermessage}
        """

    prompt_template = ChatPromptTemplate.from_template(template)

    prompt = prompt_template.invoke({"usermessage": user_input})

    response = model.invoke(prompt)

    data = {}

    try:
        match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
        else:
            print("No valid JSON object found in the response.")

    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)

    date = datetime.now().strftime("%d/%m/%Y")
    quotation_number = str(uuid.uuid4().int)[:6]
    customer_id = "CUST" + str(uuid.uuid4().int)[:5]

    quotation_details = data["quotation_details"]
    client_name = quotation_details["client"]
    company_name = quotation_details.get("company_name", "")
    address = quotation_details.get("address", "")
    phone = quotation_details.get("phone", "")
    item_total = sum(item["total"] for item in quotation_details["items"])
    tax = round(item_total * 0.18, 2)  # 18% GST
    grand_total = round(item_total + tax, 2)

    quotation_details["item_total"] = item_total
    quotation_details["tax"] = tax
    quotation_details["grand_total"] = grand_total

    # Render HTML with data
    html = render_template(
        "quotation2.html",
        client=quotation_details["client"],
        company_name=company_name,
        address=address,
        phone=phone,
        items=quotation_details["items"],
        item_total=item_total,
        tax=tax,
        grand_total=grand_total,
        date=date,
        quotation_number=quotation_number,
        customer_id=customer_id
    )


     # Step 3: Handle preview or download
    if action == "preview":
        return html  # Show rendered HTML in browser

    elif action == "download":
        pdf_file = f"{client_name}_quotation.pdf"
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)  # adjust for your OS
        pdfkit.from_string(html, pdf_file, configuration=config)
        return send_file(pdf_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)