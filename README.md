# MicroSculpt AI 2.0 🧬

A powerful AI-driven platform for analyzing monolithic code and automatically refactoring it into microservices. Now with multi-language support and AI bug detection!

## 🚀 Features

- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, Go, C#
- **AI Bug Detector**: Finds and fixes bugs using Gemini/Groq
- **Smart Function Naming**: Suggests better names based on business logic
- **Dependency Graph**: Interactive visualization of function calls
- **Service Grouping**: AI-powered clustering of functions into microservices
- **Code Generation**: Exports production-ready code (Flask/Express)

## 🛠️ Installation

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## 🛠️ Step-by-Step Workflow

### Module 1: Input & Analysis
- **Upload File**: Supports `.py`, `.js`, `.ts`, `.java`, `.go`, `.cs` files.
- **Paste Code**: Paste code directly into the editor.
- **Auto-Detection**: The system automatically detects the language and parses functions.

### Module 2: AI Bug Detection 🐛
- Click **"Run AI Analysis"** to check for bugs using Gemini/Groq.
- Review found issues and see the **AI-fixed code**.
- Click **"Apply Fixes"** to update your code automatically.

### Module 3: Smart Function Naming 🏷️
- Click **"Analyze Function Names"**.
- AI suggests descriptive business-logic names (e.g., `calc_tax` instead of `func1`).
- Check the suggestions you like and click **"Apply Renames"**.

### Module 4: Dependency Graph 🕸️
- Visualizes how your functions call each other.
- Interactive graph shows the architecture of your monolithic code.
- Check for "Isolated Functions" that might be dead code.

### Module 5: Service Grouping 📦
- AI groups your functions into logical microservices (e.g., `AuthService`, `OrderService`).
- Uses semantic analysis of function names and code structure.
- Review the grouped services before generating code.

### Module 6: Code Generation 🚀
- Generates production-ready microservice code.
- **Python**: Flask apps with Docker support.
- **JavaScript**: Express.js apps with Docker support.
- Downloads a complete `.zip` file with `docker-compose.yml` to run everything instantly.

## 🏃 Running Generated Microservices

1. Unzip the downloaded file.
2. Open a terminal in the folder.
3. Run:
   ```bash
   docker-compose up --build
   ```
4. Your microservices will be live!

## 🔑 Configuration

API keys (Gemini, Groq, Hugging Face) are managed in `config.py`. You can update them there or set them as environment variables.

---
*Built with Streamlit & Google Gemini*
