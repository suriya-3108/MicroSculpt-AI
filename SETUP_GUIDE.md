════════════════════════════════════════════════════════════════════════════════
                    MICROSCULPT AI 2.0 - SETUP GUIDE
════════════════════════════════════════════════════════════════════════════════

QUICK START GUIDE
════════════════════════════════════════════════════════════════════════════════

This guide will help you set up MicroSculpt AI 2.0 on your local machine.


STEP 1: CLONE THE REPOSITORY
────────────────────────────────────────────────────────────────────────────────

Clone this repository to your local machine:

    git clone <your-repository-url>
    cd new-microsculpt


STEP 2: SET UP PYTHON ENVIRONMENT
────────────────────────────────────────────────────────────────────────────────

Create and activate a virtual environment:

Windows:
    python -m venv venv
    venv\Scripts\activate

Mac/Linux:
    python3 -m venv venv
    source venv/bin/activate


STEP 3: INSTALL DEPENDENCIES
────────────────────────────────────────────────────────────────────────────────

Install required Python packages:

    pip install -r requirements.txt


STEP 4: CONFIGURE API KEYS
────────────────────────────────────────────────────────────────────────────────

IMPORTANT: You need to set up your API keys before running the application.

Option A: Using config.py (Recommended for local development)

    1. Copy the example configuration file:
       
       Windows:
           copy config_example.py config.py
       
       Mac/Linux:
           cp config_example.py config.py
    
    2. Open config.py in your text editor
    
    3. Replace the placeholder values with your actual API keys:
       
       GEMINI_API_KEY = "your_actual_gemini_key_here"
       GROQ_API_KEY = "your_actual_groq_key_here"
       HF_API_KEY = "your_actual_huggingface_key_here"
    
    4. Save the file

Option B: Using Environment Variables (Recommended for production)

    1. Copy the example environment file:
       
       Windows:
           copy .env.example .env
       
       Mac/Linux:
           cp .env.example .env
    
    2. Open .env in your text editor
    
    3. Fill in your actual API keys
    
    4. The application will automatically load these values


WHERE TO GET API KEYS
────────────────────────────────────────────────────────────────────────────────

Google Gemini API Key (Primary - Required):
    • Visit: https://makersuite.google.com/app/apikey
    • Sign in with your Google account
    • Click "Create API Key"
    • Copy the key and paste it in your config

Groq API Key (Secondary - Optional but recommended):
    • Visit: https://console.groq.com/keys
    • Sign up for a free account
    • Generate a new API key
    • Copy and paste in your config

Hugging Face API Key (Tertiary - Optional):
    • Visit: https://huggingface.co/settings/tokens
    • Sign up for a free account
    • Create a new token
    • Copy and paste in your config


STEP 5: RUN THE APPLICATION
────────────────────────────────────────────────────────────────────────────────

Start the Streamlit application:

    streamlit run app.py

The application will open in your default web browser at:
    http://localhost:8501


STEP 6: START USING MICROSCULPT AI
────────────────────────────────────────────────────────────────────────────────

    1. Upload your monolithic code file or paste code directly
    
    2. Follow the 6-phase workflow:
       • Phase 1: Input & Analysis
       • Phase 2: AI Bug Detection
       • Phase 3: Smart Function Naming
       • Phase 4: Dependency Graph
       • Phase 5: Service Grouping
       • Phase 6: Code Generation
    
    3. Download your generated microservices as a ZIP file
    
    4. Extract and run with Docker:
       
           docker-compose up --build


TROUBLESHOOTING
────────────────────────────────────────────────────────────────────────────────

Issue: "Module not found" errors
Solution: Make sure you activated the virtual environment and installed all 
          dependencies using pip install -r requirements.txt

Issue: "API key not found" or authentication errors
Solution: Double-check that you've correctly set up your API keys in config.py
          or .env file. Make sure there are no extra spaces or quotes.

Issue: Streamlit won't start
Solution: Make sure you're in the project directory and the virtual environment
          is activated. Try: python -m streamlit run app.py

Issue: Docker commands not working
Solution: Make sure Docker Desktop is installed and running on your machine.


SECURITY NOTES
────────────────────────────────────────────────────────────────────────────────

IMPORTANT: Never commit your API keys to Git!

    • config.py is in .gitignore and will NOT be pushed to Git
    • .env is in .gitignore and will NOT be pushed to Git
    • Only config_example.py and .env.example are tracked by Git
    • These example files contain NO actual keys, only placeholders


CONTRIBUTING
────────────────────────────────────────────────────────────────────────────────

If you want to contribute to this project:

    1. Fork the repository
    2. Create a new branch for your feature
    3. Make your changes
    4. Test thoroughly
    5. Submit a pull request

Remember: Never include your actual API keys in pull requests!


SUPPORT
────────────────────────────────────────────────────────────────────────────────

For issues, questions, or feature requests, please open an issue on GitHub.


════════════════════════════════════════════════════════════════════════════════
                              HAPPY CODING! 🚀
════════════════════════════════════════════════════════════════════════════════
