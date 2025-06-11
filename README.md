
Persian-English QA System

- What This Project Does – AI Book Translator (Offline, Local)

This project is an AI-powered system that helps users read English books, ask questions in Dari, and get accurate answers and translations—all offline, without needing the internet or any API keys.

- How It Works (Step-by-Step):
Reads the Book (PDF)
The system reads the book and splits the text into smaller parts.

Embeds the Text (Vectorization)
Each part of the book is converted into numerical vectors using embedding libraries and stored in a vector database for fast access.

User Asks a Question in Dari
The user types a question in Dari (e.g., "What is the main idea of chapter 2?").

Translates the Question to English
The question is automatically translated into English to match the book’s content.

Finds the Most Relevant Parts of the Book
The system searches and retrieves the most relevant sections related to the question.

Uses an LLM to Answer
A local language model (like Mistral) reads those sections and generates a response.

Translates the Answer Back to Dari
The English answer is translated back to Dari and shown to the user.

 Key Features:
100% Offline – No internet or API needed

Supports Dari language input/output

Private & Secure – All data stays on your local device

Works on mid-range laptops – No expensive hardware required

Based on open-source models and libraries



## Setup

1. Install requirements:
pip install -r requirements.txt

2. Download models:
Mistral-7B-Instruct.gguf to models/
MT5 translation models to models/mt5-fa-en and models/mt5-en-fa

3. Create vector store:
python setup.py

Usage: 

from src.workflow import run_qa

persian_question = "نویسنده این کتاب کیست؟"
answer = run_qa(persian_question)
print(answer)

- Message Examples ( I used "A Brief History of Time" book for testing)
User (Persian): سلام! این سیستم چطور کار می‌کند؟
System: سلام! این سیستم می‌تواند به سوالات شما درباره کتاب‌های انگلیسی پاسخ دهد. لطفا سوال خود را بپرسید.

User (Persian): نویسنده کتاب "تاریخچه زمان" کیست؟
System (Processing Steps):
1. Translating to English: "Who is the author of 'A Brief History of Time'?"
2. Searching PDF content...
3. Found relevant passage: "A Brief History of Time by Stephen Hawking..."
4. Generating answer: "The author is Stephen Hawking."
5. Translating to Persian: "نویسنده استیون هاوکینگ است."

User (Persian): موضوع اصلی کتاب چیست؟
System (Processing Steps):
1. Translating to English: "What is the main subject of the book?"
2. Searching PDF content...
3. Found relevant passage: "This book explores the nature of time, black holes..."
4. Generating answer: "It explores cosmology and theoretical physics."
5. Translating to Persian: "کتاب به بررسی کیهان‌شناسی و فیزیک نظری می‌پردازد."

User (Persian): یک نقل قول معروف از کتاب بگویید
System (Processing Steps):
1. Translating to English: "Tell me a famous quote from the book"
2. Searching PDF content...
3. Found passage: "The universe doesn't allow perfection..."
4. Generating answer: "One famous quote is: 'The universe doesn't allow perfection.'"
5. Translating to Persian: "یک نقل قول معروف: 'جهان به کمال اجازه وجود نمی‌دهد.'"

User (Persian): متشکرم
System: خواهش می‌کنم! برای سوالات دیگر درباره کتاب در خدمت


Workflow Steps:
1. Translate Persian question → English

2. Retrieve relevant context from PDF

3. Generate English answer using Mistral

4. Translate English answer → Persian


### Key Components:

1. **PDF Processing**:
   - Uses PyPDFLoader for text extraction
   - Recursive text splitting preserves context

2. **Translation**:
   - Local MT5 models for Persian ↔ English
   - Separate models for each translation direction

3. **Vector Search**:
   - FAISS for efficient similarity search
   - MiniLM embeddings for document retrieval

4. **LLM Integration**:
   - Mistral-7B via llama.cpp for local inference
   - Prompt engineering for QA tasks

5. **Workflow Orchestration**:
   - LangGraph state management
   - Clear node definitions for each processing step
   - Typed state transitions

To use the system:
1. Run `setup.py` to create the vector store
2. Call `run_qa()` with Persian questions
3. Get Persian answers back

The implementation focuses on:
- Local execution only (no API dependencies)
- Modular components
- Efficient document retrieval
- Clear state transitions
- Minimal external dependencies

Note: Adjust `n_gpu_layers` in `llm_query.py` based on your GPU capabilities.
