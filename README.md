# Vector Search App

A smart vector search application that combines the power of Hugging Face's language models with Azure Cosmos DB's vector capabilities to provide semantic search functionality.

![image](https://github.com/user-attachments/assets/76ed5248-bdf3-4ee0-8ec2-c4aa323fda57)

![image](https://github.com/user-attachments/assets/8b3187ed-2d9f-4b09-a422-19152662b437)


## Features

- **Semantic Search**: Understanding meaning beyond keywords
- **Vector Similarity**: Advanced document comparison
- **Category Management**: Smart content organization
- **User-Friendly Interface**: Built with Streamlit
- **Search History**: Track and manage searches

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: Azure Cosmos DB
- **ML Model**: Hugging Face Sentence Transformers
- **Vector Processing**: NumPy
- **Language**: Python

## 📋 Project Structure
```vbnet
vector-search-app/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── document.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cosmos_service.py
│   │   └── embedding_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py
│   └── config/
│       ├── __init__.py
│       └── settings.py
├── app.py
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.8+
- Azure Cosmos DB account
- Git

### Installation

1. Clone the repository
```bash
git clone https://github.com/FarahAbdo/vector-search-app.git
cd vector-search-app
```


2. Create and activate virtual environment
```bash
python -m venv venv

## Windows
venv\Scripts\activate

## Unix/MacOS
source venv/bin/activate
```


3. Install dependencies
```bash
pip install -r requirements.txt
```


4. Create .env file
```bash
COSMOS_ENDPOINT="your_cosmos_db_endpoint"
COSMOS_KEY="your_cosmos_db_key"
DATABASE_NAME="vector-search-db"
CONTAINER_NAME="documents"
MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
```


### Running the Application

1. Start the FastAPI backend
```bash
uvicorn src.api.main:app --reload
```


2. Start the Streamlit frontend (in a new terminal)
```bash
streamlit run app.py
```


3. Access the applications:
- FastAPI backend: http://localhost:8000
- API documentation: http://localhost:8000/docs
- Streamlit frontend: http://localhost:8500

## 📝 Usage

### Adding Documents
Example document addition
```json
{
    "query": {
        "text": "Azure Cosmos DB is a fully managed NoSQL database service",
        "category": "documentation"
    }
}
```

### Searching Documents
Example search query
```json
{
    "query": "how to use cosmos db",
    "top_k": 3,
    "category": "documentation"
}
```

##  Acknowledgments

- Hugging Face for the transformer models
- Azure Cosmos DB for vector storage capabilities
- FastAPI and Streamlit communities

