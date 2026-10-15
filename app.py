import streamlit as st
import boto3
import pandas as pd
from botocore.config import Config

# --- SECURE CREDENTIALS (DO NOT HARDCODE REAL KEYS HERE) ---
# This pulls the credentials safely from the Streamlit Cloud environment
ACCOUNT_ID = st.secrets["ACCOUNT_ID"]
ACCESS_KEY = st.secrets["ACCESS_KEY"]
SECRET_KEY = st.secrets["SECRET_KEY"]

# --- STRICT CONFIGURATION ---
# Hardcode the bucket and file name to prevent unauthorized file access
BUCKET_NAME = "hackathon-ev-data"
ALLOWED_FILE = "export.csv" 

# --- R2 CLIENT SETUP ---
s3_client = boto3.client(
    "s3",
    endpoint_url=f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name="auto",
    config=Config(signature_version="s3v4")
)

# --- DASHBOARD UI ---
st.title("⚡ Secure EV Data Portal")
st.write("Temporary Object Sharing Architecture")

if st.button("Generate 5-Minute Access Link"):
    
    # Generate the URL strictly for the ALLOWED_FILE
    url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": BUCKET_NAME, 
            "Key": ALLOWED_FILE
        },
        ExpiresIn=300
    )
    
    st.success("✅ Secure Link Generated Successfully!")
    st.code(url, language="text")
    
    st.subheader("Data Preview (Loaded via Secure Link)")
    try:
        data = pd.read_csv(url)
        st.dataframe(data.head(10)) 
        st.bar_chart(data['Electric Vehicle Type'].value_counts())
    except Exception as e:
        st.error("Could not load data. Link may be expired.")