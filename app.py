import streamlit as st
import pandas as pd
import numpy as np
import smtplib
import re
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from sklearn.preprocessing import LabelEncoder

# --- Configuration ---
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# --- Helper Functions ---

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def send_email(receiver_email, result_df, filename="result.csv"):
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return False, "Server Error: Email credentials are not configured."
        
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

        # SMTP Server Setup (Using SSL Port 465 for Hugging Face compatibility)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, receiver_email, text)
        server.quit()
        return True, "Email sent successfully!"
    except Exception as e:
        return False, str(e)

def calculate_topsis(data_matrix, weights, impacts):
    """
    Performs the TOPSIS calculation on the numeric data matrix.
    """
    try:
        # Step 1: Vector Normalization
        rss = np.sqrt(np.sum(data_matrix**2, axis=0))
        
        # Handle division by zero
        if (rss == 0).any():
            return None, "Error: One of the columns contains all zeros, cannot normalize."
            
        normalized_matrix = data_matrix / rss

        # Step 2: Weight Assignment
        weighted_matrix = normalized_matrix * weights

        # Step 3: Find Ideal Best and Ideal Worst
        ideal_best = []
        ideal_worst = []

        for i in range(len(impacts)):
            if impacts[i] == '+':
                ideal_best.append(np.max(weighted_matrix[:, i]))
                ideal_worst.append(np.min(weighted_matrix[:, i]))
            else: # Impact is '-'
                ideal_best.append(np.min(weighted_matrix[:, i]))
                ideal_worst.append(np.max(weighted_matrix[:, i]))

        ideal_best = np.array(ideal_best)
        ideal_worst = np.array(ideal_worst)

        # Step 4: Calculate Euclidean Distance
        s_best = np.sqrt(np.sum((weighted_matrix - ideal_best)**2, axis=1))
        s_worst = np.sqrt(np.sum((weighted_matrix - ideal_worst)**2, axis=1))

        # Step 5: Topsis Score
        denom = s_best + s_worst
        
        # Safe division
        topsis_score = np.divide(s_worst, denom, out=np.zeros_like(s_worst), where=denom!=0)
        topsis_score = np.round(topsis_score, 5)
        
        return topsis_score, None

    except Exception as e:
        return None, str(e)

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
    # --- Basic Checks ---
    if not uploaded_file:
        st.error("Please upload a CSV file.")
        st.stop()
    if not email_id or not validate_email(email_id):
        st.error("Please enter a valid email address.")
        st.stop()
    if not weights_input:
        st.error("Please enter weights.")
        st.stop()
    if not impacts_input:
        st.error("Please enter impacts.")
        st.stop()

    try:
        # Load Data
        df = pd.read_csv(uploaded_file)
        
        # --- Validation 1: Column Count ---
        if df.shape[1] < 3:
            st.error("Error: Input file must contain three or more columns.")
            st.stop()

        # --- Validation 2: Parse Weights ---
        try:
            final_weights = [float(w) for w in weights_input.split(',')]
        except ValueError:
            st.error("Error: Weights should be comma-separated numeric values (e.g., '1,2,3').")
            st.stop()

        # --- Validation 3: Parse Impacts ---
        final_impacts = impacts_input.split(',')
        if not all(i in ['+', '-'] for i in final_impacts):
            st.error("Error: Impacts should be either '+' or '-' separated by commas (e.g., '+,-,+').")
            st.stop()

        # --- Validation 4: Preprocessing & Encoding ---
        # Iterate from the 2nd column (index 1) to the last
        encoding_log = []
        for col in df.columns[1:]:
            if not pd.api.types.is_numeric_dtype(df[col]):
                try:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col])
                    
                    # Store mapping for user info
                    mapping = dict(zip(le.classes_, le.transform(le.classes_)))
                    encoding_log.append(f"Encoded '{col}': {mapping}")
                    
                except Exception as e:
                    st.error(f"Error: Could not encode '{col}' column. {e}")
                    st.stop()

        # Show encoding info if any changes happened
        if encoding_log:
            with st.expander("Categorical Values Encoded"):
                for log in encoding_log:
                    st.write(log)

        # Create Data Matrix
        data_matrix = df.iloc[:, 1:].values.astype(float)
        columns = data_matrix.shape[1]

        # --- Validation 5: Length Mismatch ---
        if len(final_weights) != columns:
            st.error(f"Error: Number of weights ({len(final_weights)}) is not equal to number of columns ({columns}).")
            st.stop()
        
        if len(final_impacts) != columns:
            st.error(f"Error: Number of impacts ({len(final_impacts)}) is not equal to number of columns ({columns}).")
            st.stop()

        # --- Run Calculation ---
        st.info("Calculating TOPSIS Score...")
        topsis_score, error_msg = calculate_topsis(data_matrix, final_weights, final_impacts)

        if error_msg:
            st.error(error_msg)
        else:
            # Add results to dataframe
            df['Topsis Score'] = topsis_score
            df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)

            # --- Send Email ---
            st.info(f"Sending result to {email_id}...")
            success, message = send_email(email_id, df)
            
            if success:
                st.success("Success! Result file has been sent to your email.")
                st.dataframe(df) # Show preview
            else:
                st.error(f"Failed to send email: {message}")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")