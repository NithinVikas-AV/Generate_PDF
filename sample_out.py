import os
import re
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model = ChatGoogleGenerativeAI(model = 'gemini-2.0-flash', google_api_key = api_key)

template = """
        *** Generate an HTML quotation document based on the following input. ***

        The HTML should:
        - Use clean, readable formatting.
        - Include the client name.
        - Display a table for each item with: name, quantity, unit price, and total.
        - Show the grand total at the end.
        - Use ₹ as the currency symbol.

        Respond ONLY with a complete, valid HTML document.
         
        ** Dont specify anything like '''html ... ''' before the code. Only the html code should be there.**

        User Input: {usermessage}
        """

user_input="""Generate a quotation for 3 fans at ₹1500 each and 4 LED lights at ₹800 each for client Nithin."""

prompt_template = ChatPromptTemplate.from_template(template)
prompt = prompt_template.invoke({"usermessage": user_input})
response = model.invoke(prompt)

html_content = response.content.strip()

if html_content.startswith("'''html") or html_content.startswith("```html"):
        html_content = re.sub(r"^(['`]{3}html\s*)", "", html_content)
        html_content = re.sub(r"(['`]{3})\s*$", "", html_content)

print(html_content)