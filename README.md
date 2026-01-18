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
```bash
git clone https://github.com/aishani-s20/TOPSIS_Web_App.git
cd topsis-web-service
pip install -r requirements.txt
streamlit run app.py
```

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