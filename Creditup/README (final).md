# CreditUp – Empowering Gen Z to Build Creditworthiness & Financial Well‑Being

CreditUp is a web application that helps assess the creditworthiness of young users who lack traditional credit history by using behavioral and academic data inputs. It combines **AHP (Analytic Hierarchy Process)** and **Fuzzy Evaluation** techniques to return a comprehensive credit score and personalized advice.

## 🌐 Features

- User authentication (register/login/logout)
- Credit scoring form with easy-to-use UI
- Real-time calculation using AHP + Fuzzy logic
- Suggestions to improve financial well-being
- Clean results display with credit level indicators

## 📦 Installation

1. **Clone this repository**
```bash
git clone https://github.com/Linh332004/CreditUp-Project.git
cd creditup
```

2. **Create and activate a virtual environment (optional but recommended)**
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## ▶️ Running the App

From the project root (where `main.py` is):

```bash
python main.py
```

Then go to `http://127.0.0.1:5000` in your web browser.

## 📁 Project Structure

```
Creditup/
│
├── main.py               # Flask app entry point
├── requirements.txt
├── README.md
│
├── website/              # Main app code
│   ├── __init__.py
│   ├── views.py
│   ├── auth.py
│   ├── modules/          # AHP & Fuzzy logic
│   ├── templates/        # HTML pages
│   └── static/           # CSS/JS assets
│
└── instance/             # Database (SQLite)
```

## 📊 Technologies Used

- Python, Flask
- Flask-Login, Flask-SQLAlchemy
- scikit-fuzzy (Fuzzy logic)
- pandas, numpy
- HTML, CSS (user-friendly form interface)

## 🙋‍♀️ Contributions

Pull requests are welcome! Please make sure your changes are clearly documented.

## 🛡 Disclaimer

This app is for **educational and prototype purposes only** and does not replace actual credit scoring systems used by financial institutions.

---

Made with ❤️ by Team CreditUp
