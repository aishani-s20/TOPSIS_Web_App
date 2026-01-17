import streamlit as st
import pandas as pd
import numpy as np
import smtplib
import re
import os
from dotenv import load_dotenv  # <--- Import this
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# --- Configuration ---
load_dotenv()  # <--- This loads the variables from .env

# Now we read the secrets using os.getenv
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

if not SENDER_EMAIL or not SENDER_PASSWORD:
    st.error("Error: Email credentials not found. Please check your .env file.")
    st.stop()

# --- Helper Functions ---

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def send_email(receiver_email, result_df, filename="result.csv"):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = "Your TOPSIS Result is Ready"

        body = "Hello,\n\nPlease find the attached result file for your TOPSIS calculation.\n\nBest,\nTOPSIS Web Service"
        msg.attach(MIMEText(body, 'plain'))

        # Convert DataFrame to CSV string
        csv_data = result_df.to_csv(index=False)
        
        # Attachment
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(csv_data)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        msg.attach(part)

        # SMTP Server Setup (For Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, receiver_email, text)
        server.quit()
        return True, "Email sent successfully!"
    except Exception as e:
        return False, str(e)

def calculate_topsis(df, weights, impacts):
    # This logic is adapted from your CLI package
    try:
        # Preprocessing: Drop first column (Object Names) and convert to float
        data = df.iloc[:, 1:].values.astype(float)
        
        # Normalization
        rss = np.sqrt(np.sum(data**2, axis=0))
        normalized_data = data / rss

        # Weighting
        weighted_data = normalized_data * weights

        # Ideal Best and Worst
        ideal_best = []
        ideal_worst = []

        for i in range(len(impacts)):
            if impacts[i] == '+':
                ideal_best.append(np.max(weighted_data[:, i]))
                ideal_worst.append(np.min(weighted_data[:, i]))
            else:
                ideal_best.append(np.min(weighted_data[:, i]))
                ideal_worst.append(np.max(weighted_data[:, i]))

        # Euclidean Distance
        s_best = np.sqrt(np.sum((weighted_data - ideal_best)**2, axis=1))
        s_worst = np.sqrt(np.sum((weighted_data - ideal_worst)**2, axis=1))

        # Topsis Score
        topsis_score = s_worst / (s_best + s_worst)
        
        # Add to DF
        df['Topsis Score'] = topsis_score
        df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)
        
        return df

    except Exception as e:
        st.error(f"Error in calculation: {e}")
        return None

# --- Main App UI ---

st.title("Topsis Web Service")
st.write("Upload your data, define weights/impacts, and get results via email.")

# 1. Inputs
email_id = st.text_input("Email ID (to receive results)", placeholder="name@example.com")
uploaded_file = st.file_uploader("Upload Input File (CSV)", type=["csv"])
weights_input = st.text_input("Weights (comma-separated)", placeholder="1,1,1,2")
impacts_input = st.text_input("Impacts (comma-separated, + or -)", placeholder="+,+,-,+")

# 2. Submit Button
if st.button("Submit"):
    # --- Validations ---
    if not uploaded_file:
        st.error("Please upload a CSV file.")
    elif not email_id or not validate_email(email_id):
        st.error("Please enter a valid email address.")
    elif not weights_input:
        st.error("Please enter weights.")
    elif not impacts_input:
        st.error("Please enter impacts.")
    else:
        # Process Inputs
        try:
            df = pd.read_csv(uploaded_file)
            
            # Parse Weights
            weights = [float(w) for w in weights_input.split(',')]
            
            # Parse Impacts
            impacts = impacts_input.split(',')
            
            # Validation: Column Count
            num_cols = df.shape[1] - 1  # Exclude first column
            if len(weights) != num_cols or len(impacts) != num_cols:
                st.error(f"Count Mismatch! Input file has {num_cols} numerical columns, but you provided {len(weights)} weights and {len(impacts)} impacts.")
            elif not all(i in ['+', '-'] for i in impacts):
                st.error("Impacts must be either '+' or '-'.")
            else:
                # --- Run Logic ---
                st.info("Calculating TOPSIS Score...")
                result_df = calculate_topsis(df, weights, impacts)
                
                if result_df is not None:
                    # --- Send Email ---
                    st.info(f"Sending result to {email_id}...")
                    success, message = send_email(email_id, result_df)
                    
                    if success:
                        st.success("Success! Result file has been sent to your email.")
                        st.dataframe(result_df) # Show preview
                    else:
                        st.error(f"Failed to send email: {message}")

        except ValueError:
            st.error("Weights must be numeric values separated by commas.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")