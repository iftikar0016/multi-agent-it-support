# 🤖 SupportX AI Assist

**SupportX AI Assist** is an intelligent IT support assistant powered by multi-agent orchestration, vector search, and large language models. It automatically classifies IT issues, retrieves relevant solutions from a knowledge base, and escalates unresolved tickets to human support.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🌟 Features

- **🎯 Intelligent Classification**: Automatically categorizes IT issues into predefined categories (Network Issue, Hardware Issue, Software Bug, Access Request, Password Reset, Other)
- **🔍 Vector Search**: Uses Azure AI Search with Gemini embeddings for semantic similarity matching
- **🤝 Multi-Agent Orchestration**: Powered by AutoGen framework for coordinated agent collaboration
- **📊 Interactive UI**: Clean Streamlit interface for seamless user interaction
- **🎫 Ticket Management**: Automatic ticket generation and escalation for unresolved issues
- **📧 Email Notifications**: Sends notifications to IT support when issues require human intervention

---

## 🏗️ Architecture

```
User Query
    ↓
ClassifierAgent (Categorizes the issue)
    ↓
KnowledgeBaseAgent (Searches Azure AI Search with Gemini embeddings)
    ↓
Solution Found? → Yes → Return to User
    ↓
    No
    ↓
NotificationAgent (Escalate via email)
```

### Tech Stack

- **Frontend**: Streamlit
- **Agent Orchestration**: AutoGen (pyautogen)
- **LLM**: Groq (Llama models)
- **Embeddings**: Google Gemini (`gemini-embedding-001`)
- **Vector Database**: Azure AI Search
- **Email**: SMTP (Gmail)

---

## 📋 Prerequisites

- Python 3.8 or higher
- Azure AI Search instance
- Google Gemini API key
- Groq API key
- Gmail account (for email notifications)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SupportX-AI-Assist.git
cd SupportX-AI-Assist
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_KEY=your-azure-search-key

# Google Gemini
GEMINI_API_KEY=your-gemini-api-key

# Groq
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile

# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECEIVER_EMAIL=support@yourcompany.com
```

> **Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

---

## 📊 Setting Up the Knowledge Base

### 1. Prepare Your Data

Edit `data/knowledge_base.json` with your IT solutions. Each entry should have:

```json
{
  "id": "unique-id",
  "category": "Software Bug",
  "problem": "Description of the problem",
  "solution": "Step-by-step solution"
}
```

### 2. Create and Upload Index

```bash
python create_and_upload_index.py
```

This script will:
- Create an Azure AI Search index with vector search capabilities
- Generate embeddings using Gemini for each problem
- Upload all documents to Azure AI Search

---

## 🎮 Usage

### Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

### How It Works

1. **Describe Your Issue**: Enter your IT problem in the text area
2. **AI Processing**: The system classifies and searches for solutions
3. **Review Solution**: Check if the provided solution resolves your issue
4. **Feedback**: 
   - ✅ **Yes**: Issue marked as resolved
   - ❌ **No**: Ticket created and escalated to IT support via email

---

## 📁 Project Structure

```
SupportX-AI-Assist/
├── agents/
│   ├── classifier_agent.py          # Classifies IT issues
│   ├── knowledge_base_agent.py      # Retrieves solutions
│   └── notification_agent.py        # Handles escalations
├── tools/
│   ├── knowledge_base_tool.py       # Azure Search integration
│   └── send_email.py                # Email notification tool
├── utility/
│   ├── llm_config.py                # LLM configuration
│   └── prompt.py                    # Agent prompts
├── data/
│   └── knowledge_base.json          # IT solutions database
├── app.py                           # Streamlit UI
├── group_chat.py                    # Multi-agent orchestration
├── create_and_upload_index.py       # Index creation script
├── style.css                        # Custom styling
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (not in repo)
└── README.md                        # This file
```

---

## 🔧 Customization

### Adding New Categories

1. Update the classifier prompt in `utility/prompt.py`
2. Add corresponding entries in `data/knowledge_base.json`
3. Re-run `create_and_upload_index.py`

### Changing the LLM

Modify `utility/llm_config.py` to use different models or providers:

```python
llm_config = {
    "temperature": 0,
    "config_list": [
        {
            "model": "your-model-name",
            "api_key": "your-api-key",
            "base_url": "your-base-url",
        }
    ]
}
```

### Customizing the UI

Edit `style.css` to change colors, fonts, and layout.

---

## 🧪 Testing

Test the knowledge base search directly:

```bash
python tools/knowledge_base_tool.py
```

Test the multi-agent workflow:

```bash
python group_chat.py
```

---

## 🐛 Troubleshooting

### "No matching solutions found"

- Verify your Azure AI Search index exists and contains data
- Check that the `category` filter matches your knowledge base categories exactly
- Ensure embeddings are generated correctly (dimension should be 3072 for `gemini-embedding-001`)

### Agent Not Calling Tools

- Verify `llm_config` is properly configured
- Check that tools are registered with both `register_for_llm` and `register_for_execution`
- Review agent system messages for clarity

### Email Not Sending

- Confirm Gmail App Password is correct
- Check firewall/antivirus settings
- Verify SMTP settings in `tools/send_email.py`

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [AutoGen](https://github.com/microsoft/autogen) - Multi-agent framework
- [Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search) - Vector search
- [Google Gemini](https://ai.google.dev/) - Embeddings
- [Streamlit](https://streamlit.io/) - UI framework
- [Groq](https://groq.com/) - Fast LLM inference

---

