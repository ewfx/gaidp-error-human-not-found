# 🚀 Project Name

## 📌 Table of Contents
- [Introduction](https://github.com/ewfx/gaidp-error-human-not-found/blob/main/README.md#-introduction)
- [Demo](https://github.com/ewfx/gaidp-error-human-not-found/blob/main/README.md#-demo)
- [Inspiration](https://github.com/ewfx/gaidp-error-human-not-found/blob/main/README.md#-inspiration)
- [What It Does](https://github.com/ewfx/gaidp-error-human-not-found/blob/main/README.md#%EF%B8%8F-what-it-does)
- [How We Built It](https://github.com/ewfx/gaidp-error-human-not-found/blob/main/README.md#%EF%B8%8F-how-we-built-it)
- [Challenges We Faced](https://github.com/ewfx/gaidp-error-human-not-found/blob/main/README.md#-challenges-we-faced)
- [How to Run](https://github.com/ewfx/gaidp-error-human-not-found/blob/main/README.md#-how-to-run)
- [Tech Stack](https://github.com/ewfx/gaidp-error-human-not-found/blob/main/README.md#%EF%B8%8F-tech-stack)
- [Team](https://github.com/ewfx/gaidp-error-human-not-found/blob/main/README.md#%EF%B8%8F-tech-stack)

---

## 🎯 Introduction
Our project - Gen AI-based data profiling leverages generative AI to automate and enhance the process of analyzing, understanding, and improving data quality. 

Purpose - Automated Rule Discovery - Uses AI to extract rules and constraints from datasets or documents (e.g., PDFs) and reduces manual effort in defining data validation rules.
        - Context-Aware Profiling - Customizes profiling results based on business requirements.
        - Scalable and Adaptive Profiling - Adapts to changes in data sources without extensive reconfiguration.

## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 1](link-to-image)

## 💡 Inspiration
In the banking domain, ensuring accurate and rule-compliant customer data profiling is critical. Traditionally, this process requires significant manual effort to categorize and validate data while adhering to strict regulatory and business rules. However, manual checks are time-consuming, error-prone, and difficult to scale.

Our goal with Gen AI-based data profiling is to explore whether AI can effectively interpret and enforce complex rules while improving efficiency and accuracy. By leveraging AI, we aim to automate data categorization, reduce human intervention, and enhance compliance—ultimately delivering more reliable results.

## ⚙️ What It Does

The solution follows a structured workflow to ensure seamless data profiling:

1. Rule Extraction
- The client provides a PDF document containing business and regulatory rules.
- LLM models extract these rules from the PDF and convert them into a structured format.

2. Rule Storage
- The extracted rules are stored in a structured database, ensuring easy retrieval and scalability.
- These rules define the criteria that customer data must adhere to for compliance.

3. Data Ingestion
- The client submits a dataset that needs to be profiled.
- This dataset contains customer information, transactions, or other financial data.

4. Rule Application
- The stored rules are applied to the client’s dataset.
- The system checks whether each data record complies with the extracted rules.

5. Anomaly Detection
- The system identifies and flags records that do not adhere to the given rules.

## 🛠️ How We Built It
LLM's - OpenAI GPT (free-tier API)

Data Processing - Python libraries - Pandas, NumPy

Code Generation - GPTbased Python Code Generation

Visualization and Interactivity - Streamlit

## 🚧 Challenges We Faced

1. Inaccurate Rule Extraction
In the initial stages, the AI-based rule extraction process was not entirely accurate.

Some extracted rules were incomplete or misinterpreted, leading to discrepancies in data categorization.

This required manual validation and corrections, increasing the effort needed to refine the AI model.

2. Lack of Ready-to-Use Datasets
A major challenge was the absence of real-world datasets for testing the extracted rules.

Client datasets were either unavailable or too sensitive to use directly due to privacy and compliance concerns.

To address this, we implemented Synthetic Dataset Generation, creating test datasets that mimicked real-world scenarios while maintaining privacy and compliance considerations.

3. Need for Manual Verification
Despite AI-driven automation, manual validation was necessary to ensure that the dataset adhered to the extracted rules.

AI misinterpretations or edge cases occasionally led to false positives or negatives in anomaly detection.

## 🏃 How to Run
1. Clone the repository  
   ```sh
   git clone https://github.com/your-repo.git
   ```
2. Install dependencies  
   ```sh
   npm install  # or pip install -r requirements.txt (for Python)
   ```
3. Run the project  
   ```sh
   npm start  # or python app.py
   ```

## 🏗️ Tech Stack
- 🔹 Frontend: React / Vue / Angular
- 🔹 Backend: Node.js / FastAPI / Django
- 🔹 Database: PostgreSQL / Firebase
- 🔹 Other: OpenAI API / Twilio / Stripe

## 👥 Team
- **Your Name** - [GitHub](#) | [LinkedIn](#)
- **Teammate 2** - [GitHub](#) | [LinkedIn](#)
