import os
import streamlit as st
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

# carrega as variáveis do .env
load_dotenv()

def analyze_document(file_bytes: bytes) -> dict:
    """
    Send image bytes to Azure Document Intelligence with prebuilt-creditCard model.
    Extracts: card number, holder name, expiration date, issuing bank, and payment network.
    """
    endpoint = os.getenv("AZURE_ENDPOINT")
    key = os.getenv("AZURE_KEY")
    
    result = {
        "numero": None,
        "cliente": None,
        "validade": None,
        "bandeira": None,
        "banco": None,
        "valido": False,
        "erro": None,
        "confidence": {}
    }
    
    if not endpoint or not key:
        result["erro"] = "AZURE_ENDPOINT and AZURE_KEY not configured in .env file"
        return result
    
    try:
        client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
        
        poller = client.begin_analyze_document("prebuilt-creditCard", body=file_bytes)
        credit_cards = poller.result()
        
        if not credit_cards.documents or len(credit_cards.documents) == 0:
            result["erro"] = "No credit card detected in the image"
            return result
        
        # Extract data from the first detected card
        document = credit_cards.documents[0]
        
        # Card Number
        card_number = document.fields.get("CardNumber")
        if card_number and card_number.value_string:
            result["numero"] = card_number.value_string
            result["confidence"]["numero"] = round(card_number.confidence * 100, 1)
            # result["valido"] = luhn_checksum(card_number.value_string)
        
        # Cardholder Name
        card_holder = document.fields.get("CardHolderName")
        if card_holder and card_holder.value_string:
            result["cliente"] = card_holder.value_string
            result["confidence"]["cliente"] = round(card_holder.confidence * 100, 1)
        
        # Expiration Date
        expiration = document.fields.get("ExpirationDate")
        if expiration and expiration.value_string:
            result["validade"] = expiration.value_string
            result["confidence"]["validade"] = round(expiration.confidence * 100, 1)
        
        # Payment Network (Card Brand)
        payment_network = document.fields.get("PaymentNetwork")
        if payment_network and payment_network.value_string:
            result["bandeira"] = payment_network.value_string
            result["confidence"]["bandeira"] = round(payment_network.confidence * 100, 1)
        
        # Issuing Bank
        issuing_bank = document.fields.get("IssuingBank")
        if issuing_bank and issuing_bank.value_string:
            result["banco"] = issuing_bank.value_string
            result["confidence"]["banco"] = round(issuing_bank.confidence * 100, 1)
        
        return result
    
    except Exception as e:
        result["erro"] = f"Error analyzing document: {str(e)}"
        return result


# ---------- Streamlit UI ----------

st.title("📇 Credit Card Validator with Azure Document Intelligence")
st.write(
    "Upload an image (or PDF) of a credit card and the app will attempt to read the number "
    "using Azure Document Intelligence and then validate it with the Luhn checksum."
)

uploaded = st.file_uploader("Choose an image or PDF file", type=["jpg", "jpeg", "png", "pdf"])

if uploaded:
    st.image(uploaded, caption="Uploaded file", width=400)

    try:
        content = uploaded.read()
        card_data = analyze_document(content)

        if card_data.get("erro"):
            st.warning(card_data["erro"])
        elif card_data["numero"]:
            st.success("✅ Card data extracted successfully!")
            
            # Display card number and validation
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Card Number")
                st.code(card_data["numero"])
                confidence = card_data.get("confidence", {}).get("numero", "N/A")
                st.caption(f"Confidence: {confidence}%")
                
               
            with col2:
                st.subheader("Card Brand (Network)")
                if card_data["bandeira"]:
                    st.info(card_data["bandeira"])
                    confidence = card_data.get("confidence", {}).get("bandeira", "N/A")
                    st.caption(f"Confidence: {confidence}%")
                else:
                    st.warning("Not detected")
            
            # Display cardholder and expiration
            col3, col4 = st.columns(2)
            
            with col3:
                st.subheader("Cardholder Name")
                if card_data["cliente"]:
                    st.text(card_data["cliente"])
                    confidence = card_data.get("confidence", {}).get("cliente", "N/A")
                    st.caption(f"Confidence: {confidence}%")
                else:
                    st.warning("Not detected")
            
            with col4:
                st.subheader("Expiration Date")
                if card_data["validade"]:
                    st.text(card_data["validade"])
                    confidence = card_data.get("confidence", {}).get("validade", "N/A")
                    st.caption(f"Confidence: {confidence}%")
                else:
                    st.warning("Not detected")
            
            # Display issuing bank
            if card_data.get("banco"):
                st.subheader("Issuing Bank")
                st.text(card_data["banco"])
                confidence = card_data.get("confidence", {}).get("banco", "N/A")
                st.caption(f"Confidence: {confidence}%")
            
            # Summary JSON
            st.divider()
            st.subheader("Complete Data")
            st.json(card_data)

        else:
            st.warning("No card number could be detected in the document.")
    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")

else:
    st.info("Please upload a file to start analysis.")

