# Building SupportX AI Assist: A Multi-Agent IT Support System

**Published:** February 9, 2026  
**Author:** Iftikhar  
**Tags:** AI, Multi-Agent Systems, AutoGen, Azure AI Search, IT Support, LLMs

---

## 🚀 Introduction

Have you ever been stuck waiting for IT support to resolve a simple issue like a password reset or a network configuration problem? What if an AI assistant could instantly classify your problem, search through a comprehensive knowledge base, and provide you with a solution in seconds?

Meet **SupportX AI Assist** — an intelligent IT support system that leverages multi-agent orchestration, vector search, and large language models to provide instant, accurate solutions to common IT problems. And when it can't solve an issue? It automatically escalates it to human IT support with a detailed ticket.

In this blog post, I'll walk you through how I built this system, the technologies I used, and the architectural decisions that make it work seamlessly.

---

## 💡 The Problem

Traditional IT support systems face several challenges:

1. **High Response Times**: Users often wait hours or days for simple issues
2. **Repetitive Tickets**: Support teams spend time answering the same questions repeatedly
3. **Manual Classification**: Issues must be manually categorized and routed
4. **Knowledge Silos**: Solutions are scattered across wikis, emails, and documents
5. **Inefficient Escalation**: No automated way to escalate unresolved issues

I wanted to build a solution that addresses all these pain points using modern AI technologies.

---

## 🏗️ The Solution: Multi-Agent Architecture

SupportX AI Assist uses a **multi-agent system** where specialized AI agents work together to solve IT issues. Here's how the workflow works:

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

### The Three Agents

1. **Classifier Agent** 🎯  
   - Automatically categorizes IT issues into predefined categories (Network Issue, Hardware Issue, Software Bug, Access Request, Password Reset, Other)
   - Uses LLM-based classification for accurate categorization
   - Ensures the right knowledge base section is searched

2. **Knowledge Base Agent** 🔍  
   - Performs semantic search using Azure AI Search with vector embeddings
   - Uses Google Gemini's `gemini-embedding-001` model for embeddings (3072 dimensions)
   - Matches user queries with relevant solutions using cosine similarity
   - Filters results by category for precision

3. **Notification Agent** 📧  
   - Handles ticket creation when no solution is found
   - Sends detailed email notifications to IT support
   - Includes user query, ticket ID, and context for quick resolution

---

## 🛠️ Tech Stack

Building a system like this requires a carefully chosen tech stack. Here's what powers SupportX:

### Frontend
- **Streamlit**: Provides a clean, interactive web interface with minimal code
- **Custom CSS**: Polished UI with modern design elements

### AI & LLM
- **AutoGen (pyautogen)**: Microsoft's multi-agent orchestration framework
- **Groq**: Ultra-fast LLM inference using Llama models (`llama-3.3-70b-versatile`)
- **Google Gemini**: High-quality embeddings for semantic search

### Vector Search
- **Azure AI Search**: Enterprise-grade vector database with hybrid search capabilities
- Supports semantic similarity search with filtering

### Notifications
- **SMTP (Gmail)**: Email notifications for escalations

---

## 🔑 Key Technical Decisions

### 1. Why Multi-Agent Architecture?

Instead of a monolithic LLM approach, I chose a multi-agent system for several reasons:

- **Separation of Concerns**: Each agent has a specific responsibility
- **Modularity**: Easy to update or replace individual agents
- **Explainability**: Clear understanding of which agent made what decision
- **Reliability**: If one agent fails, others can continue working

### 2. Why Azure AI Search for Vector Storage?

I evaluated several vector databases (Pinecone, Weaviate, Qdrant) but chose Azure AI Search because:

- **Hybrid Search**: Combines vector search with traditional keyword search
- **Filtering**: Can filter by category before semantic search
- **Scalability**: Enterprise-ready with minimal configuration
- **Integration**: Native Azure ecosystem compatibility

### 3. Why Gemini Embeddings?

Google's Gemini `gemini-embedding-001` model offers:

- **High Dimensionality**: 3072-dimensional embeddings capture more nuance
- **Quality**: Superior semantic understanding compared to older embedding models
- **Cost-Effective**: Generous free tier for development and testing

### 4. Why Groq for LLM Inference?

Groq provides the fastest LLM inference available:

- **Speed**: ~300 tokens/second (vs ~30-50 for typical APIs)
- **User Experience**: Near-instant responses feel conversational
- **Cost**: Competitive pricing with excellent performance

---

## 📊 Implementation Highlights

### Creating the Vector Index

The knowledge base setup involves:

1. **Loading IT solutions** from `data/knowledge_base.json`
2. **Generating embeddings** for each problem using Gemini
3. **Creating Azure AI Search index** with vector search configuration
4. **Uploading documents** with embeddings and metadata

```python
# Simplified example from create_and_upload_index.py
for entry in knowledge_base:
    # Generate embedding for the problem
    embedding = genai.embed_content(
        model="models/gemini-embedding-001",
        content=entry["problem"]
    )["embedding"]
    
    # Upload to Azure AI Search
    document = {
        "id": entry["id"],
        "category": entry["category"],
        "problem": entry["problem"],
        "solution": entry["solution"],
        "embedding": embedding
    }
```

### Agent Orchestration with AutoGen

AutoGen makes multi-agent coordination elegant:

```python
# Create the agents
classifier_agent = AssistantAgent(
    name="ClassifierAgent",
    system_message=classifier_prompt,
    llm_config=llm_config
)

knowledge_base_agent = AssistantAgent(
    name="KnowledgeBaseAgent",
    system_message=knowledge_base_prompt,
    llm_config=llm_config
)

# Register tools
register_function(
    search_knowledge_base,
    caller=knowledge_base_agent,
    executor=user,
    name="search_knowledge_base",
    description="Search for IT solutions in the knowledge base"
)

# Create group chat for orchestration
groupchat = GroupChat(
    agents=[user, classifier_agent, knowledge_base_agent, notification_agent],
    messages=[],
    max_round=10
)
```

### Streamlit UI Design

The interface is designed to be intuitive:

```python
# User describes the issue
user_input = st.text_area("Describe your IT issue", height=150)

# AI processes and provides solution
if st.button("🚀 Resolve Now"):
    with st.spinner("SupportX AI Assist is resolving your issue..."):
        user.initiate_chat(recipient=manager, message=user_input)
        st.success("✅ AI Response:")
        st.markdown(final_response)

# User provides feedback
if st.button("✅ Yes, issue resolved"):
    st.success("🎉 Great! We're glad your issue is resolved.")
elif st.button("❌ No, not helpful"):
    ticket_id = generate_ticket_id()
    # Escalate to IT support
    notification_agent.generate_reply(...)
```

---

## 🎯 Real-World Use Cases

### Example 1: Password Reset
**User Input:**  
_"I forgot my password and can't log into the system."_

**System Response:**
1. Classifier categorizes as "Password Reset"
2. Knowledge Base finds relevant solution:
   - Step 1: Click "Forgot Password" on login page
   - Step 2: Enter your email address
   - Step 3: Check your email for reset link
   - Step 4: Follow link and create new password
3. User confirms issue resolved ✅

### Example 2: Network Issue
**User Input:**  
_"My laptop can't connect to the company Wi-Fi."_

**System Response:**
1. Classifier categorizes as "Network Issue"
2. Knowledge Base provides troubleshooting steps:
   - Verify Wi-Fi is enabled
   - Check correct network name (CorpWiFi-5G)
   - Verify password (check with IT if unsure)
   - Restart network adapter
   - Contact IT if issue persists
3. User tries solution but still fails ❌
4. System generates Ticket ID: `TKT-A7B3C9`
5. Email sent to IT support with full context

---

## 📈 Performance & Results

### Metrics

- **Average Response Time**: < 3 seconds
- **Classification Accuracy**: ~95% (based on manual testing)
- **Knowledge Base Hit Rate**: ~70% (solutions found without escalation)
- **Escalation Rate**: ~30% (issues requiring human support)

### User Benefits

- ✅ **Instant Answers**: No waiting for support ticket responses
- ✅ **24/7 Availability**: Works outside business hours
- ✅ **Consistent Solutions**: Same high-quality answers every time
- ✅ **Automatic Escalation**: Seamless handoff to human support when needed

### IT Support Benefits

- ✅ **Reduced Ticket Volume**: 70% fewer repetitive tickets
- ✅ **Better Context**: Escalated tickets include attempted solutions
- ✅ **Knowledge Management**: Centralized, searchable solution database
- ✅ **Efficiency**: Support teams focus on complex issues

---

## 🧪 Challenges & Lessons Learned

### Challenge 1: Embedding Dimension Mismatch
**Problem:** Initially used wrong embedding dimensions (768 vs 3072)  
**Solution:** Verified Gemini model documentation and recreated index with correct dimensions

### Challenge 2: Agent Tool Calling Reliability
**Problem:** Agents sometimes didn't call the search tool  
**Solution:** 
- Improved system prompts with clearer instructions
- Added explicit tool descriptions
- Used `register_for_llm` and `register_for_execution` properly

### Challenge 3: Email Notification Failures
**Problem:** Gmail blocked automated emails  
**Solution:** Switched to Gmail App Passwords instead of regular passwords

### Challenge 4: Category Filtering Issues
**Problem:** Some queries returned no results due to strict category matching  
**Solution:** Improved classifier prompt to use exact category names from knowledge base

---

## 🔮 Future Enhancements

Here are some ideas I'm considering for future versions:

1. **Conversation History**: Allow multi-turn conversations for complex troubleshooting
2. **User Analytics**: Track common issues and improve knowledge base
3. **Integration with Ticketing Systems**: Direct integration with Jira, ServiceNow, etc.
4. **Voice Interface**: Add speech-to-text for hands-free support
5. **Multi-Language Support**: Serve global teams in multiple languages
6. **Feedback Loop**: Automatically improve knowledge base based on user feedback
7. **Administrative Dashboard**: Monitor system performance and agent behavior
8. **Custom Agent Training**: Fine-tune agents on organization-specific data

---

## 🎓 What I Learned

Building SupportX AI Assist taught me several valuable lessons:

1. **Multi-Agent Systems Are Powerful**: Breaking down complex problems into specialized agents makes systems more maintainable and reliable

2. **Embeddings Matter**: High-quality embeddings (like Gemini) significantly improve search relevance

3. **User Experience Is Critical**: Fast responses (thanks to Groq) make the difference between a tool people use and one they avoid

4. **Prompt Engineering Is An Art**: Small changes to agent system messages dramatically affect behavior

5. **Vector Search Isn't Magic**: Proper indexing, filtering, and retrieval strategies are essential

6. **AutoGen Simplifies Complexity**: The framework handles agent coordination, allowing me to focus on business logic

---

## 🚀 Getting Started

Want to build your own version? Here's how:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/SupportX-AI-Assist.git
   cd SupportX-AI-Assist
   ```

2. **Set up environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure API keys** in `.env`:
   - Azure AI Search credentials
   - Google Gemini API key
   - Groq API key
   - Gmail credentials

4. **Create knowledge base index**:
   ```bash
   python create_and_upload_index.py
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Tech Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Interactive web UI |
| **Orchestration** | AutoGen | Multi-agent coordination |
| **LLM** | Groq (Llama 3.3) | Fast inference |
| **Embeddings** | Google Gemini | Semantic understanding |
| **Vector DB** | Azure AI Search | Knowledge retrieval |
| **Notifications** | SMTP (Gmail) | Email escalations |
| **Language** | Python 3.8+ | Core implementation |

---

## 📝 Conclusion

SupportX AI Assist demonstrates how modern AI technologies can transform traditional IT support. By combining multi-agent systems, vector search, and large language models, we can create systems that provide instant, accurate support while seamlessly escalating complex issues to human experts.

The multi-agent architecture makes the system modular, maintainable, and explainable — critical factors for enterprise adoption. The use of cutting-edge technologies like Gemini embeddings and Groq inference ensures the best possible user experience.

Whether you're building an IT support system, customer service bot, or any other knowledge-retrieval application, the patterns and technologies demonstrated here can serve as a solid foundation.

---

## 🔗 Resources

- **GitHub Repository**: [SupportX-AI-Assist](https://github.com/yourusername/SupportX-AI-Assist)
- **AutoGen Documentation**: [microsoft.github.io/autogen](https://microsoft.github.io/autogen/)
- **Azure AI Search**: [azure.microsoft.com/ai-search](https://azure.microsoft.com/en-us/products/ai-services/ai-search)
- **Google Gemini API**: [ai.google.dev](https://ai.google.dev/)
- **Groq**: [groq.com](https://groq.com/)
- **Streamlit**: [streamlit.io](https://streamlit.io/)

---

## 💬 Let's Connect

I'd love to hear your thoughts on this project! Have you built similar multi-agent systems? What challenges did you face? Feel free to reach out or contribute to the project.

**Questions or suggestions?** Open an issue on GitHub or reach out via [your contact method].

---

**Happy Building! 🚀**
