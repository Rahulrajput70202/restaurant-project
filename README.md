# 🍽️ Restaurant Name & Menu Generator

An AI-powered web app built with **Python 3.11, Streamlit, and Google Gemini AI** that generates **unique restaurant names, catchy taglines, and full menus** based on a selected **country** and **restaurant style**.  


## 🚀 Features
- ✅ Generate **5 unique restaurant name suggestions** with catchy taglines.  
- ✅ AI-generated **full menu** (5 starters, 5 main courses, 3 desserts, 3 beverages).  
- ✅ **Modern UI** with custom CSS & background image.  
- ✅ **Download option** for the generated menu in TXT format.  
- ✅ **Progress bar & caching** for a smooth experience.  
- ✅ Secure **API key management** using `.env` file.  

---

## 🛠️ Tech Stack
- **Python 3.11**  
- **Streamlit** – for interactive UI  
- **Google Gemini AI API** – for text generation  
- **python-dotenv** – for managing API keys  
- **Custom CSS** – for styling and background image  

---

## 📂 Project Structure
├── app.py # Main Streamlit app
├── .env # Environment file containing API key
├── requirements.txt # Python dependencies
└── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/restaurant-menu-generator.git
cd restaurant-menu-generator
2️⃣ Create and activate virtual environment (optional but recommended)
bash
Copy code
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On Mac/Linux
3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Setup environment variables
Create a .env file in the root folder and add your Google Gemini API key:

env
Copy code
GOOGLE_API_KEY=your_api_key_here
5️⃣ Run the app
Make sure to run it on Python 3.11:

bash
Copy code
py -3.11 -m streamlit run app.py
📦 Requirements
Add these to requirements.txt:

nginx
Copy code
streamlit
google-generativeai
python-dotenv
pillow
requests
🎨 UI Preview
Modern card-style input & results

Background image with transparent overlay

Progress bar for name & menu generation

Download button for menu export

🔮 Future Improvements
Add AI-generated restaurant logos

Support multi-language menus

Export menus as PDF

Save user history & favorites

👨‍💻 Author
Rahul Tekchand Bainade

📧 Email: rahulrajput79800@gmail.com

🔗 LinkedIn

📜 License
This project is licensed under the MIT License – free to use and modify.
