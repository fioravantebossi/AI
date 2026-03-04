# Credit Card Validator (Streamlit + Azure Document Intelligence)

This small application allows you to upload an image or PDF containing a credit card. It sends the file to Azure Document Intelligence (formerly Form Recognizer), tries to detect a card number.

## 🚀 Setup

### Quick Start (Windows, sem admin)
```powershell
cd c:\Users\fioravantebossi\Dev\AI\card-detector
.\setup.ps1
```

### Manual Setup
1. **Clone or open this folder** in VS Code.
2. **Install requirements** (use a virtual environment):
   ```sh
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```
3. **Set Azure credentials** in `.env` file:
   ```
   AZURE_ENDPOINT=https://<your-resource>.cognitiveservices.azure.com/
   AZURE_KEY=<your-key>
   ```
4. **Run the Streamlit app**:
   ```sh
   streamlit run app.py
   ```

## 📝 How it works

* The UI is built with [Streamlit](https://streamlit.io).
* Uploaded file bytes are sent to Azure using the `prebuilt-document` model.
* We scan returned lines and key/value pairs for sequences of digits resembling a card number.
* Found numbers are cleaned and run through the Luhn algorithm.

## 🛠️ Extending

* You can switch to a specialized custom model if you have one set up for cards.
* Add more heuristics to identify card brands (Visa, MasterCard, etc.) based on prefix.
* Show confidence or other metadata returned by the service.

## ⚠️ Notes

* This demo does **not** store any data; all processing happens in memory.
* Azure may return false positives or fail depending on image quality.
* Always keep your API keys secure.
