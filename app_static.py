# Import necessary libraries
import re  # For regex pattern matching
import pdfkit  # To generate PDF from HTML
import json  # To handle JSON parsing
import os  # To access environment variables
import uuid  # For generating unique IDs
from datetime import datetime  # For current date
from dotenv import load_dotenv  # To load environment variables from a .env file
from flask import Flask, render_template, send_file, request  # Flask web framework
from langchain.prompts import ChatPromptTemplate  # For prompt templating
from langchain_google_genai import ChatGoogleGenerativeAI  # To access Gemini AI model

# Load environment variables from .env file
load_dotenv()

# Get Google Gemini API key and wkhtmltopdf path from environment
api_key = os.getenv("GOOGLE_API_KEY")
wkhtmltopdf_path = os.getenv("WKHTMLTOPDF_PATH")

# Initialize the Gemini model (lightweight version)
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash', google_api_key=api_key)

# Initialize the Flask application
app = Flask(__name__)

# Route to serve the input form
@app.route("/")
def form():
    return render_template("form.html")  # Shows HTML form for user input

# Route to handle form submission and generate quotation
@app.route("/generate_pdf", methods=["POST"])
def generate_pdf():
    user_input = request.form["user_input"]  # Get the input text from the form
    action = request.form["action"]  # Determine if user wants to preview or download

    # Prompt template to instruct Gemini how to extract structured data
    template = """
        ** Use this information below to provide the output format for the user **

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

    # Inject the user's input into the prompt
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.invoke({"usermessage": user_input})

    # Send the prompt to the Gemini model and receive response
    response = model.invoke(prompt)

    data = {}  # Initialize data dictionary

    # Extract the JSON part from the AI's response using regex
    try:
        match = re.search(r'\{.*\}', response.content, re.DOTALL)
        if match:
            json_str = match.group(0)  # Extract matched JSON string
            data = json.loads(json_str)  # Convert JSON string to Python dict
        else:
            print("No valid JSON object found in the response.")
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)

    # Generate metadata
    date = datetime.now().strftime("%d/%m/%Y")  # Current date in dd/mm/yyyy
    quotation_number = str(uuid.uuid4().int)[:6]  # Random 6-digit quotation number
    customer_id = "CUST" + str(uuid.uuid4().int)[:5]  # Random customer ID

    # Extract details from parsed data
    quotation_details = data["quotation_details"]
    client_name = quotation_details["client"]
    company_name = quotation_details.get("company_name", "")  # Optional field
    address = quotation_details.get("address", "")
    phone = quotation_details.get("phone", "")

    # Recalculate totals (in case the model didn’t)
    item_total = sum(item["total"] for item in quotation_details["items"])
    tax = round(item_total * 0.18, 2)  # 18% GST
    grand_total = round(item_total + tax, 2)

    # Add recalculated values to quotation data
    quotation_details["item_total"] = item_total
    quotation_details["tax"] = tax
    quotation_details["grand_total"] = grand_total

    # Render HTML template with all quotation details
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

    # Return HTML preview or downloadable PDF
    if action == "preview":
        return html  # Show quotation in browser as HTML preview

    elif action == "download":
        # Save HTML to PDF using wkhtmltopdf
        pdf_file = f"{client_name}_quotation.pdf"
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)  # Path from .env
        pdfkit.from_string(html, pdf_file, configuration=config)
        return send_file(pdf_file, as_attachment=True)  # Trigger file download

# Run the app on localhost in debug mode
if __name__ == "__main__":
    app.run(debug=True)