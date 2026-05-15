# 📊 AI Layoffs 2026 Executive Dashboard


## 📌 Overview
The **AI Layoffs 2026 Executive Dashboard** is an enterprise-grade analytical tool designed to track and visualize tech industry workforce reductions in Q1 2026. This project goes beyond simple headcount tracking by specifically analyzing the **impact of AI adoption** on corporate restructuring and evaluating how the stock market reacts to these strategic shifts.

This dashboard was built with a premium, clean aesthetic tailored for C-suite executives, providing immediate, high-level business insights.

## ✨ Key Features
- **Executive KPI Row**: Instantly view critical metrics such as Total Jobs Displaced, AI-Driven Restructuring Percentage, and Total AI Investment.
- **Interactive Visualizations**: Built with `Plotly`, featuring hover-enabled, dual-axis timelines, and responsive pie/bar charts.
- **NLP Text Analysis**: Custom natural language processing (regex/collections) to automatically extract and visualize the most frequently disrupted job roles from unstructured text.
- **Market Consensus Scatter Plot**: A bubble chart analyzing the correlation between the severity of workforce cuts and the Day 1 stock market reaction.
- **Premium MNC Design**: A customized `Streamlit` layout utilizing the `plotly_white` theme, modern `Inter` typography, and CSS-styled KPI cards without the clutter of a default sidebar.

## 🛠️ Tech Stack
- **Data Processing & EDA**: `Pandas`, `NumPy`, `Matplotlib`, `Seaborn` (Jupyter Notebook)
- **Web Dashboard**: `Streamlit`
- **Interactive Charts**: `Plotly Express`, `Plotly Graph Objects`
- **Text Analysis**: Python `re` (Regex), `collections.Counter`

## 📂 Project Structure
- `app.py`: The main Streamlit dashboard application containing UI layout, CSS styling, and Plotly visualizations.
- `AI_LAYOFFS_.ipynb`: The original Jupyter Notebook containing the full Exploratory Data Analysis (EDA) and initial static visualizations.
- `tech_layoffs_2026_tracker.csv`: The curated dataset tracking 28 global tech companies, with 26 features per event.
- `INTERVIEW_PREP.md`: A comprehensive guide explaining the technical, analytical, and business decisions behind the project.

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-layoffs-2026.git
   cd ai-layoffs-2026
   ```

2. **Install the required dependencies:**
   Ensure you have Python installed, then run:
   ```bash
   pip install streamlit pandas numpy plotly matplotlib seaborn
   ```

3. **Run the Streamlit Dashboard:**
   ```bash
   streamlit run app.py
   ```
   The dashboard will automatically open in your browser at `http://localhost:8501`.

## 📈 Key Insights & Findings
1. **The Market Rewards AI-Driven Cuts**: Unlike traditional layoffs that signal financial distress, companies in Q1 2026 that cut jobs while simultaneously announcing heavy AI investments often experienced a **positive Day 1 stock bump** (+0.83% average).
2. **AI Restructuring is Pervasive**: Exactly **50%** of the layoffs in the dataset explicitly cited AI implementation as a driver for reducing headcount.
3. **Enterprise Software Hit Hardest**: The Enterprise Software sector accounted for **31,600** job losses, making it the most severely impacted sector by absolute numbers.

---
*Disclaimer: The data used in this project is curated for Q1 2026 tracking purposes and should not be used as official financial advice.*