# MeDom Nekretnine - AI Real Estate Assistant

An intelligent AI-powered real estate assistant that helps users search and discover properties using natural language queries. Built with Streamlit, LangChain, and OpenAI, featuring a bilingual interface (Croatian/English) and Retrieval Augmented Generation (RAG) capabilities.

## 🏠 Features

- **Natural Language Search**: Ask questions about properties in plain language
- **Bilingual Interface**: Supports both Croatian (HR) and English (EN)
- **Conversational AI**: Maintains chat history for context-aware responses
- **Source Citations**: Provides links to original property listings
- **Modern UI**: Clean, minimalist black and white design optimized for mobile and desktop
- **RAG-Powered**: Uses Retrieval Augmented Generation for accurate, context-aware answers

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: OpenAI GPT-3.5-turbo
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector Store**: Pinecone (production) / ChromaDB (local)
- **Web Crawling**: Tavily (TavilyCrawl, TavilyMap, TavilyExtract)
- **Framework**: LangChain
- **Language Detection**: langdetect

## 📋 Prerequisites

- Python 3.11.9
- Pipenv (for dependency management)
- OpenAI API key
- Pinecone API key
- Tavily API key

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd medom-pretraga
   ```

2. **Install dependencies using Pipenv**
   ```bash
   pipenv install
   ```

3. **Create a `.env` file** in the root directory with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

4. **Activate the virtual environment**
   ```bash
   pipenv shell
   ```

## 📊 Data Ingestion

The project includes multiple ingestion scripts for populating the vector database:

### Option 1: TavilyCrawl (Recommended)
Crawls and extracts content from a website using Tavily's advanced crawling:
```bash
python ingestion.py
```

### Option 2: TavilyMap + TavilyExtract
Maps website structure first, then extracts content:
```bash
python ingestion_map_extract.py
```

### Option 3: Basic Crawler
Simple web crawler using BeautifulSoup:
```bash
python basic_crawl.py
```

**Note**: The ingestion scripts extract property information from `medom-nekretnine.com` and index it into Pinecone for semantic search.

## 🎯 Usage

### Running the Application

Start the Streamlit application:
```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`.

### Using the Interface

1. **Select Language**: Use the radio buttons in the header to switch between Croatian (HR) and English (EN)
2. **Ask Questions**: Type your property search query in the input field at the bottom
3. **View Results**: The AI will respond with relevant properties, including prices and source URLs
4. **Continue Conversation**: The chat maintains context, so you can ask follow-up questions

### Example Queries

- Croatian: "Trebao bih 5 najskupljih građevinkih zemljišta, sve opcije"
- English: "Show me the 5 most expensive building plots with all options"

## 📁 Project Structure

```
medom-pretraga/
├── backend/
│   ├── __init__.py
│   └── core.py              # LLM chain and RAG implementation
├── chroma_db/               # Local ChromaDB storage
│   └── chroma.sqlite3
├── main.py                  # Streamlit application
├── ingestion.py             # Main ingestion pipeline (TavilyCrawl)
├── ingestion_map_extract.py # Alternative ingestion (TavilyMap + Extract)
├── basic_crawl.py          # Basic web crawler
├── logger.py                # Colored logging utility
├── Pipfile                  # Python dependencies
└── Pipfile.lock            # Locked dependencies
```

## 🔧 Configuration

### Vector Store Settings

The application uses Pinecone as the primary vector store. Configure the index name in `backend/core.py`:
```python
INDEX_NAME = "langchain-doc-index"
```

### Embedding Model

The embedding model can be configured in both `backend/core.py` and `ingestion.py`:
```python
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
```

### Text Splitting

Chunk size and overlap can be adjusted in the ingestion scripts:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=5000, 
    chunk_overlap=500
)
```

## 🎨 Customization

### UI Styling

The Streamlit UI uses custom CSS defined in `main.py`. You can modify the styles in the `st.markdown()` section starting around line 37.

### System Prompt

The AI's behavior can be customized by modifying the system prompt in `backend/core.py` (lines 28-40).

## 📝 Development

### Running Tests

Test the LLM chain directly:
```bash
python backend/core.py
```

### Logging

The project includes a custom logging utility (`logger.py`) with colored output:
- `log_info()` - Cyan info messages
- `log_success()` - Green success messages
- `log_error()` - Red error messages
- `log_warning()` - Yellow warning messages
- `log_header()` - Purple header messages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- UI powered by [Streamlit](https://streamlit.io/)
- Vector storage by [Pinecone](https://www.pinecone.io/)
- Web crawling by [Tavily](https://tavily.com/)

## 📧 Contact

For questions or support, please open an issue in the repository.

