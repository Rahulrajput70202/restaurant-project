import streamlit as st
import google.generativeai as genai
import os
import dotenv
from typing import Optional, Dict, Any
import time

# Load .env file (make sure .env is in the same folder as app.py)
dotenv.load_dotenv()

# Configure Google Gemini API
def setup_gemini() -> None:
    """Configure Google Gemini API with the API key from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("❌ API key not found! Please check your .env file and ensure GOOGLE_API_KEY is set.")
        st.stop()
    genai.configure(api_key=api_key)

# Initialize Gemini
setup_gemini()

# Constants
POPULAR_COUNTRIES = [
    "🇮🇳 India", "🇺🇸 United States", "🇮🇹 Italy", "🇯🇵 Japan", 
    "🇫🇷 France", "🇨🇳 China", "🇹🇭 Thailand", "🇲🇽 Mexico", 
    "🇬🇷 Greece", "🇪🇸 Spain", "🇰🇷 South Korea", "🇧🇷 Brazil",
    "🇬🇧 United Kingdom", "🇩🇪 Germany", "🇹🇷 Turkey", "Other"
]

RESTAURANT_STYLES = [
    "🏛️ Traditional", "✨ Modern", "🌮 Street Food", "👑 Luxury", 
    "🌍 Fusion", "☕ Café", "🍕 Casual Dining", "🍣 Fine Dining"
]

@st.cache_data(ttl=3600)  # Cache for 1 hour
def generate_restaurant_name(country: str, style: str) -> str:
    """
    Generate a unique restaurant name using Google Gemini AI.
    
    Args:
        country: The country for the restaurant
        style: The restaurant style/theme
        
    Returns:
        Generated restaurant name
    """
    prompt = f"Suggest a unique and catchy restaurant name for a {style} style restaurant in {country}. Make it creative and memorable."
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, "text") else "No response"

@st.cache_data(ttl=3600)  # Cache for 1 hour
def generate_menu(country: str, style: str) -> str:
    """
    Generate a detailed menu using Google Gemini AI.
    
    Args:
        country: The country for the restaurant
        style: The restaurant style/theme
        
    Returns:
        Generated menu content
    """
    prompt = (
        f"Create a detailed menu for a {style} style restaurant in {country}. "
        f"Include 5 starters, 5 main courses, 3 desserts, and 3 beverages. "
        f"Format it with clear sections and descriptions. Make it authentic to the cuisine."
    )
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, "text") else "No response"

def format_menu_output(menu_text: str) -> None:
    """
    Format and display the menu with proper sections and styling.
    
    Args:
        menu_text: Raw menu text from AI
    """
    # Split menu into sections
    sections = {
        "🥗 Starters": [],
        "🍛 Main Courses": [],
        "🍰 Desserts": [],
        "🍹 Beverages": []
    }
    
    lines = menu_text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for section headers
        if any(keyword in line.lower() for keyword in ['starter', 'appetizer', 'entree']):
            current_section = "🥗 Starters"
        elif any(keyword in line.lower() for keyword in ['main', 'course', 'dish']):
            current_section = "🍛 Main Courses"
        elif any(keyword in line.lower() for keyword in ['dessert', 'sweet']):
            current_section = "🍰 Desserts"
        elif any(keyword in line.lower() for keyword in ['beverage', 'drink', 'beverage']):
            current_section = "🍹 Beverages"
        elif current_section and line and not line.startswith('#'):
            sections[current_section].append(line)
    
    # Display formatted menu
    for section_name, items in sections.items():
        if items:
            st.markdown(f"### {section_name}")
            for item in items:
                if item.strip():
                    st.markdown(f"• {item.strip()}")

def create_download_button(restaurant_name: str, menu_text: str) -> None:
    """
    Create a download button for the generated menu.
    
    Args:
        restaurant_name: Name of the restaurant
        menu_text: Menu content to download
    """
    content = f"Restaurant: {restaurant_name}\n\n{menu_text}"
    st.download_button(
        label="📥 Download Menu as TXT",
        data=content,
        file_name=f"{restaurant_name.replace(' ', '_')}_menu.txt",
        mime="text/plain"
    )

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .input-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid #e0e0e0;
    }
    
    .result-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
    
    .restaurant-name {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin: 1rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
    }
    
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem 0;
            margin-bottom: 1rem;
        }
        
        .input-card, .result-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .restaurant-name {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Streamlit UI
st.set_page_config(
    page_title="Restaurant & Menu Generator", 
    page_icon="🍽", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🍽️ Restaurant Name & Menu Generator</h1>
    <p style="font-size: 1.2rem; margin: 0;">Create unique restaurant concepts with AI-powered menu generation</p>
</div>
""", unsafe_allow_html=True)

# Input form in a card
with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 Choose Country")
        country_selection = st.selectbox(
            "Select a popular country or choose 'Other'",
            options=POPULAR_COUNTRIES,
            index=0,
            help="Choose from popular countries or select 'Other' for custom input"
        )
        
        if country_selection == "Other":
            country = st.text_input("Enter Country:", placeholder="e.g., Italy, Japan, India")
        else:
            country = country_selection.split(" ", 1)[1]  # Remove emoji and get country name
    
    with col2:
        st.markdown("### 🎨 Restaurant Style")
        style = st.selectbox(
            "Choose restaurant style",
            options=RESTAURANT_STYLES,
            index=0,
            help="Select the type of restaurant you want to create"
        )
        style = style.split(" ", 1)[1]  # Remove emoji and get style name
    
    st.markdown('</div>', unsafe_allow_html=True)

# Generate button
if st.button("✨ Generate Restaurant & Menu", type="primary"):
    if country and style:
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Generate restaurant name
        status_text.text("🎯 Generating restaurant name...")
        progress_bar.progress(25)
        
        with st.spinner("Creating your unique restaurant name..."):
            name = generate_restaurant_name(country, style)
        
        progress_bar.progress(50)
        status_text.text("📋 Generating menu...")
        
        # Generate menu
        with st.spinner("Crafting your delicious menu..."):
            menu = generate_menu(country, style)
        
        progress_bar.progress(100)
        status_text.text("✅ Complete!")
        
        # Display results
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        
        # Restaurant name header
        st.markdown(f'<div class="restaurant-name">{name}</div>', unsafe_allow_html=True)
        
        # Menu sections
        st.markdown("### 📋 Menu")
        format_menu_output(menu)
        
        # Download button
        st.markdown("---")
        create_download_button(name, menu)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Clear progress
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
    else:
        st.warning("⚠️ Please fill in both country and style fields.")
