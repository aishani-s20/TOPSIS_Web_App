# 📊 TOPSIS Web Service

A web-based implementation of the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) method that allows users to upload input data, specify weights and impacts, and receive the computed ranking results via email.

🔗 **Deployed Application:** 👉 [https://topsiswebapp.streamlit.app/](https://topsiswebapp.streamlit.app/)

---

## 📘 What is TOPSIS?

**TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** is a multi-criteria decision-making (MCDM) method used to rank alternatives based on their relative closeness to an ideal solution.

### 🔹 Key Idea
The best alternative should:
- Have the **shortest distance from the ideal solution**
- Have the **farthest distance from the negative-ideal solution**

TOPSIS is widely used in:
- Engineering decision-making  
- Business and management analysis  
- Data science and analytics  
- Research and academic projects  

---

## 🚀 Features

- Upload input data file (CSV format)
- Accepts weights and impacts from the user
- Validates inputs strictly:
  - Number of weights = number of impacts
  - Impacts must be `+` or `-`
  - Weights and impacts must be comma-separated
  - Email ID format is validated
- Computes TOPSIS score and ranking
- Result file is emailed automatically to the user
- Simple and interactive Streamlit UI

---

## 📁 Input File Format

- The input file must be a **CSV file**
- **First column:** Alternative names
- **Remaining columns:** Numerical criteria values

**Example:**

| Model | Price | Mileage | Comfort |
|-------|-------|---------|---------|
| A     | 25000 | 20      | 7       |
| B     | 27000 | 22      | 8       |
| C     | 30000 | 18      | 9       |

---

## 🧮 Weights & Impacts Format

### Weights
Comma-separated numerical values

**Example:**
```
0.3,0.4,0.3
```

### Impacts
Comma-separated values (`+` or `-`)

**Example:**
```
-,+,+
```

### Validation Rules
- ✔ Number of weights = number of impacts
- ✔ Impacts must be only `+` or `-`
- ✔ Values must be separated by commas

---

## 📧 Email Requirement

- A valid email ID must be provided
- The result file will be sent to this email after successful computation

---

## 📤 Output

- A **CSV file** containing:
  - TOPSIS Score
  - Rank of each alternative
- Sent directly to the provided email address

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (Web Interface)
- **Pandas / NumPy**
- **SMTP** (Email Service)

---

## ▶️ How to Run Locally

Follow these steps to run the application on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/aishani-s20/TOPSIS_Web_App.git
cd TOPSIS_Web_App
```

### 2. Install Dependencies

Make sure you have Python installed. Then run:
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

To enable the email feature, you must create a `.env` file in the root directory to store your credentials securely.

Create a file named `.env` and add the following:
```ini
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_char_app_password
```

⚠️ **Note:** For Gmail, you must use an **App Password**, not your regular login password.  
[Click here to learn how to create a Google App Password](https://support.google.com/accounts/answer/185833).

### 4. Run the App

Launch the Streamlit server:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 📌 Deployed Link (Live Demo)

🌐 [https://topsiswebapp.streamlit.app/](https://topsiswebapp.streamlit.app/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Aishani Shreya**  
- GitHub: [@aishani-s20](https://github.com/aishani-s20)
- Email: aishani1020@gmail.com

---

## ⭐ Show your support

Give a ⭐️ if this project helped you!