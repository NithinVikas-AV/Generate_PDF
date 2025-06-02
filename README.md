**What the code does**

  - This code creates Rate Quotation (PDF) from the data provided by user.
  
  - The data provided by the user is passed to gemini and converted into a JSON variable where all the necessary data from the user prompt is available.
  
  - Then the JSON variable is splitted into many different value and passed to a static HTML file where then all the values are assigned to the placeholders.
  
  - Then using pdfkit library, convert the static HTML into a pdf and return it to the user.

**How to download wkhtmltopdf**

  - visit this site:
  -     https://wkhtmltopdf.org/downloads.html

  - Install the latest version according to your OS.

  - Make sure you add the path for wkhtmltopdf in your .env file. For Example the path for wkthmltopdf looks like this:  C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe

**Values in .env file**  
  - GOOGLE_API_KEY="your-gemini-api-key"
  - WKHTMLTOPDF_PATH=C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe (or) your actual wkhtmlpdf path

**Steps to run the code:**

  - Clone repository:
  -     git clone https://github.com/NithinVikas-AV/Generate_PDF.git

  - Create a virtual environment (pdf_env) if necessary and install all the libraries mentioned in the requirement.txt
  -     python -m venv pdf_env

  - Activate the virtual environment: 
  -     pdf_env/Scripts/activate

  - Download all the necessary libraries
  -     pip install -r requirements.txt

  - Run the code:
  -     python app_static.py

  - Enter a example prompt:
  -     Create a quotation for client Priya Sharma from GreenBuild Solutions located at 45 Industrial Estate, Bengaluru. Their contact number is +91-9123456780.

        They want:
        
        200 steel rods at ₹150 each
        
        75 concrete slabs at ₹450 each
        
        25 liters of paint at ₹120 each

- If you give preview then you can see the preview of the quotation.
- If u give download then the file is downloaded automatically.
