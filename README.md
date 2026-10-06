# 🎬 MovieWala

> **MovieWala** is an AI-powered movie and web-series information extractor that turns a simple title into a clean, structured cinematic report with a funny Hinglish summary.

---

## ✨ Overview

MovieWala uses **LangChain + an LLM + Pydantic structured output** to analyze a movie or web-series title and extract useful information such as:

- 🎬 Movie / Web-series title
- 📅 Release year
- 🎭 Genre
- 🎥 Director
- 👥 Main cast
- ⭐ Rating
- 😂 Funny Hinglish summary

The project is designed to demonstrate how an LLM can be combined with **prompt templates and structured output parsing** to build a practical AI application.

---

## 🚀 Features

### 🎬 Movie Information Extraction

MovieWala extracts:

| Information | Description |
|---|---|
| Title | Movie or web-series title |
| Release Year | Year of release |
| Genre | One or more genres |
| Director | Director name |
| Cast | Main actors and their characters |
| Rating | IMDb-style rating when available |
| Summary | Funny Hinglish explanation |

### 😂 Hinglish Masti Mode

The generated summary is designed to be:

- Written in **Roman Hindi + English**
- Funny and conversational
- Easy to understand
- Lightly sarcastic
- Entertaining rather than Wikipedia-style
- Mostly spoiler-free

Example style:

> "Basically bhai, hero ki life already sorted nahi thi, aur upar se story ne decide kar liya ki thoda aur problem daalte hain. Normal insaan hota toh resignation de deta, lekin hero hai bhai... problems ko solve karne ke bajaye aur problems create karega. 😂"

### 🧠 Structured AI Output

Instead of relying on manually formatted text, MovieWala uses a Pydantic model:

```python
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str
```

This makes the model response easier to process and display in an application.

---

## 🏗️ Project Architecture

```text
                 ┌──────────────────────┐
                 │       User           │
                 │  Movie / Series Name │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │  ChatPromptTemplate  │
                 │   LangChain Prompt   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │      LLM Model       │
                 │ Mistral / Gemini*    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ PydanticOutputParser │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Movie Object     │
                 │      Pydantic        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Streamlit UI       │
                 │  MovieWala Dashboard │
                 └──────────────────────┘
```

> `*` Gemini can be used by replacing the model integration and configuration.

---

## 🛠️ Tech Stack

### Frontend / UI
- [Streamlit](https://streamlit.io/)

### AI / LLM
- [LangChain](https://www.langchain.com/)
- Mistral AI via `langchain-mistralai`
- Gemini via `langchain-google-genai` (optional)

### Data Validation
- [Pydantic](https://docs.pydantic.dev/)

### Configuration
- `python-dotenv`

### Language
- Python 3.10+

---

## 📁 Project Structure

```text
MovieWala/
│
├── MovieWala.py
├── .env
├── .gitignore
├── README.md
│
└── .streamlit/
    └── config.toml
```

If your project contains additional files, they can be added to this structure as the application grows.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd MovieWala
```

### 2. Create a virtual environment

Using standard Python:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Or using `uv`:

```bash
uv venv
```

---

## 📦 Install Dependencies

### Using pip

```bash
pip install streamlit python-dotenv langchain langchain-core langchain-mistralai pydantic
```

### Using uv

```bash
uv add streamlit python-dotenv langchain langchain-core langchain-mistralai pydantic
```

If you are using Gemini instead:

```bash
uv add langchain-google-genai
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

### Mistral

```env
MISTRAL_API_KEY=your_mistral_api_key
```

### Gemini

If using the Gemini integration:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

Never commit your `.env` file to GitHub.

Add this to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

---

## ▶️ Running the Application

### Streamlit

```bash
streamlit run MovieWala.py
```

With `uv`:

```bash
uv run streamlit run MovieWala.py
```

Once Streamlit starts, open the local URL shown in the terminal.

---

## 🔄 Automatic Reload

Streamlit automatically reruns the application when the Python file changes.

If file watching causes dependency-related errors, you can use polling:

```bash
uv run streamlit run MovieWala.py --server.fileWatcherType poll
```

To make it permanent, create:

```text
.streamlit/config.toml
```

and add:

```toml
[server]
fileWatcherType = "poll"
```

Then you only need to start Streamlit once.

---

## 🧩 How It Works

### Step 1 — User Input

The user enters a title:

```text
3 Idiots
```

### Step 2 — Prompt Creation

LangChain creates the final prompt:

```python
final_prompt = movie_prompt.invoke({
    "title": title,
    "format_instructions": parser.get_format_instructions()
})
```

### Step 3 — LLM Processing

The prompt is sent to the selected model:

```python
response = model.invoke(final_prompt)
```

### Step 4 — Structured Parsing

The model response is converted into the Pydantic model:

```python
movie = parser.parse(response.content)
```

### Step 5 — Application Output

The application can then directly access:

```python
movie.title
movie.release_year
movie.genre
movie.director
movie.cast
movie.rating
movie.summary
```

---

## 📦 Pydantic Output Schema

The current schema is:

```python
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str
```

### Example structured output

```json
{
  "title": "3 Idiots",
  "release_year": 2009,
  "genre": [
    "Comedy",
    "Drama"
  ],
  "director": "Rajkumar Hirani",
  "cast": [
    "Aamir Khan - Rancho",
    "R. Madhavan - Farhan",
    "Sharman Joshi - Raju"
  ],
  "rating": 8.4,
  "summary": "Basically bhai, ye story hai teen doston ki..."
}
```

---

## ⚠️ Accuracy & Limitations

MovieWala is an **LLM-based application**, so factual accuracy depends on the model and the information available to it.

The application instructs the model:

- Do not invent information.
- Use `null` for unavailable optional fields.
- Do not confuse movies with similar titles.
- Keep the humorous summary based on the factual story.

However, an LLM **does not automatically have live access to movie databases or the internet**.

Therefore, ratings, cast, release information, or plot details may occasionally be outdated or incorrect.

### Recommended Future Improvement

For higher factual reliability:

```text
Movie Title
     ↓
Movie Database / Web Search
     ↓
Verified Movie Information
     ↓
LLM
     ↓
Structured Pydantic Output
     ↓
Streamlit
```

Possible future data sources include movie databases or a controlled web-search/RAG pipeline.

---

## 🔮 Future Improvements

### 🎞️ Movie Poster

Add movie posters using a movie database API.

### ⭐ Real-Time Ratings

Retrieve current ratings from reliable sources instead of depending entirely on model knowledge.

### 🔎 Search / RAG

Use web search or a movie database to ground the LLM response.

### 🎭 Detailed Cast

Add:

- Actor
- Character
- Role
- Biography

### 📺 Web-Series Support

Add:

- Number of seasons
- Number of episodes
- Streaming platform
- Episode information

### ⚠️ Content Analysis

Add:

- Violence
- Language
- Sexual content
- Mature themes
- Age suitability

### 🎯 Recommendation Engine

Allow users to ask:

```text
"Suggest me movies like Interstellar"
```

### 🧠 Structured JSON Export

Allow users to download the extracted information as:

- JSON
- CSV
- PDF

### 💾 Search History

Store previously analyzed movies and allow users to revisit them.

---

## 🎨 UI Concept

The Streamlit version is designed as a cinematic dashboard rather than a normal chatbot.

```text
                 🎬 MOVIEWALA
        AI-powered Movie Intelligence

        ┌─────────────────────────────┐
        │ Enter Movie / Web Series    │
        └─────────────────────────────┘

              🚀 ANALYZE

        🎬 Movie Intelligence

   ┌────────┐ ┌────────┐ ┌────────┐
   │ Genre  │ │  Year  │ │ Rating │
   └────────┘ └────────┘ └────────┘

        🎭 Cast & Crew

        📖 Story

        😂 Masti Mode

        🎯 Best For

        🔥 Final Verdict
```

---

## 🔐 Security

Do not expose API keys in source code.

### ❌ Don't do this:

```python
model = ChatMistralAI(
    api_key="my-secret-api-key"
)
```

### ✅ Use `.env`:

```env
MISTRAL_API_KEY=your_key
```

and:

```python
from dotenv import load_dotenv

load_dotenv()
```

Also make sure `.env` is included in `.gitignore`.

---

## 🧪 Example

Run:

```bash
uv run streamlit run MovieWala.py
```

Enter:

```text
Chhichhore
```

MovieWala generates structured information and a humorous Hinglish explanation such as:

> "Basically bhai, college life mein attendance se zyada important hota hai dost... aur yahan dosti ke saath problems bhi free mein milti hain. 😂"

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new branch.

```bash
git checkout -b feature/new-feature
```

3. Make your changes.
4. Commit:

```bash
git commit -m "Add new movie feature"
```

5. Push:

```bash
git push origin feature/new-feature
```

6. Create a Pull Request.

---

## 📜 License

This project is intended for educational and development purposes.

Add an appropriate open-source license such as MIT if you plan to distribute the project publicly.

---

## 👨‍💻 Author

**MovieWala**

Built with:

**Python • Streamlit • LangChain • Pydantic • Mistral/Gemini**

---

## ⭐ If You Like This Project

If MovieWala helped you learn something about:

- Generative AI
- LangChain
- Prompt Engineering
- Pydantic
- Structured Output
- Streamlit

consider giving the repository a ⭐ on GitHub.

---

### 🎬 MovieWala

> **"Movie information, but make it intelligent... and thoda funny bhi. 🍿😂"**
