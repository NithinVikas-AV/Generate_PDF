
# 📄 Generate Quotation PDF using Gemini AI and Flask

This project allows users to generate **rate quotation PDFs** dynamically based on natural language input. It uses **Google Gemini AI** to extract structured data from user prompts, renders the data into an HTML template, and converts it into a downloadable PDF using `pdfkit`.

---

## 🚀 Features

- Extracts client and item details from natural language input using Gemini AI.
- Automatically calculates item totals, 18% GST, and grand total.
- Generates a professional quotation in PDF format.
- Offers both preview and download options.
- Simple web interface built with Flask.

---

## 🛠 Requirements

- Python 3.8+
- Google Gemini API Key
- `wkhtmltopdf` installed and properly configured

---

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/NithinVikas-AV/Generate_PDF.git
cd Generate_PDF
```

### 2. Create a Virtual Environment
```bash
python -m venv pdf_env
```

### 3. Activate the Environment

- On Windows:
```bash
pdf_env\Scripts\activate
```

- On macOS/Linux:
```bash
source pdf_env/bin/activate
```

### 4. Install Required Packages
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 1. Download and Install `wkhtmltopdf`

- Visit: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)
- Download and install the latest version for your OS.
- Copy the path to the `wkhtmltopdf` executable. Example for Windows:
  ```
  C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe
  ```

### 2. Create a `.env` File in the Project Root

Add the following:
```env
GOOGLE_API_KEY=your-gemini-api-key
WKHTMLTOPDF_PATH=full-path-to-wkhtmltopdf
```

---

## ▶️ Running the Application

```bash
python app_static.py
```

Visit `http://127.0.0.1:5000/` in your browser.

---

## 📝 Example Prompt

```text
Create a quotation for client Priya Sharma from GreenBuild Solutions located at 45 Industrial Estate, Bengaluru. Their contact number is +91-9123456780.

They want:

200 steel rods at ₹150 each

75 concrete slabs at ₹450 each

25 liters of paint at ₹120 each
```

- Select **Preview** to view the quotation in the browser.
- Select **Download** to receive a downloadable PDF file.

---

## 📂 Project Structure

```
Generate_PDF/
│
├── templates/
│   └── form.html          # Input form page
│   └── quotation2.html    # HTML template for the quotation
│
├── app_static.py          # Main Flask application
├── requirements.txt       # List of dependencies
├── .env                   # Environment variables (add manually)
```

---

## ✅ Output Fields (Extracted from Prompt)

The AI extracts and generates:

- **Client Name**
- **Company Name**
- **Address**
- **Phone Number**
- **Itemized List** (with name, quantity, unit price, total)
- **Item Total**
- **18% GST**
- **Grand Total**

---

## 📬 Contact

For any queries or feedback, feel free to reach out via [GitHub Issues](https://github.com/NithinVikas-AV/Generate_PDF/issues).
