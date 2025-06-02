# user_request = "Generate a quotation for 3 fans at ₹1500 each and 4 LED lights at ₹800 each for client Nithin."

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

    # Prompt template to get complete HTML
    template = """
    *** Generate a full HTML quotation document ***

    Format:
    - Include a <style> tag for basic CSS styling (tables, headers).
    - Include a title and heading.
    - Display the client name.
    - Show a table of items with: item, quantity, unit price, total.
    - Display a grand total at the bottom.
    - Currency must be ₹ (Indian Rupee).
    
    Respond ONLY with valid HTML. Do NOT include any explanation or notes.

    User Input: {usermessage}
    """

    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.invoke({"usermessage": user_input})
    response = model.invoke(prompt)

    html_content = response.content.strip()
    
    if html_content.startswith("'''html") or html_content.startswith("```html"):
        html_content = re.sub(r"^(['`]{3}html\s*)", "", html_content)
        html_content = re.sub(r"(['`]{3})\s*$", "", html_content)


    if "<html" not in html_content.lower():
        return "Model did not return valid HTML content.", 500

    pdf_file = "quotation.pdf"
    wkhtmltopdf_path = os.getenv("WKHTMLTOPDF_PATH")
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    pdfkit.from_string(html_content, pdf_file, configuration=config)

    return send_file(pdf_file, as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)