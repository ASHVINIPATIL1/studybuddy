# StudyBuddy — AI-Powered Study Companion

StudyBuddy is a web application that helps students study smarter. Upload your PDF notes or question papers and let AI automatically generate quiz questions, flashcards, and answer your doubts through a chat interface.

---

## What It Can Do

### 📄 PDF Upload
- Upload multiple PDF files under one subject
- All files are combined into one study session
- Add more files to an existing material anytime

### ⚡ AI Content Generation
- Automatically generates MCQ questions from your uploaded material
- Automatically generates Flashcards from your uploaded material
- Customize exactly how many questions and flashcards to generate
- Generate from all files or only selected files

### 🎯 Quiz Platform
- Take a quiz based on your uploaded material
- Filter questions by difficulty — Easy, Medium, or Hard
- Correct answers with explanations revealed after submission
- Retry only the questions you got wrong

### 🃏 Flashcards
- Flip cards to reveal answers
- Mark each card as Know It or Review Again
- Session score shown at the end

### 💬 Chat With Your Material
- Ask questions about your uploaded PDFs
- AI answers strictly based on YOUR material
- Ask cross questions across multiple uploaded files
- Full chat history saved — never loses context

### 📊 Progress Tracking
- Track scores across all quiz attempts
- Visual score history chart
- Daily study streak tracking
- Average score analytics

---

## Tech Stack

Backend:
 Python + Django → Web server, URL routing, business logic, authentication

Database: 
SQLite → Stores users, study materials, questions, scores, chat history

Artificial Intelligence:
 Groq API — Llama 3.3 70B → Generates MCQs, Flashcards, answers chat questions

PDF Processing:
 PyMuPDF (fitz) → Extracts and combines text from uploaded PDF files

Frontend: 
HTML, CSS, Bootstrap, JavaScript → Responsive UI, flashcard animations, quiz navigation, chat interface

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/study-buddy.git
cd study-buddy
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file
Create a `.env` file in the project root and add:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free Groq API key at https://console.groq.com

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Run the server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Requirements

```
Django
groq
PyMuPDF
python-dotenv
```

---

## Project Structure

```
study-buddy/
├── core/          → Project configuration
├── users/         → Login, Register, Logout
├── materials/     → PDF upload, AI chat
├── quiz/          → Questions, Flashcards
├── progress/      → Scores, Analytics
├── templates/     → HTML pages
├── static/        → CSS, JavaScript
└── media/         → Uploaded PDFs
```

---

## Team

- Ashvini Patil
- Bhumika Patil
- Isha Pawar

College: MVPS's Karmaveer Adv. Baburao Ganpatrao Thakre College of Engineering, Nashik.