# AI Interviewer

A mock AI-based interview platform designed to conduct interviews across multiple fields.

## Overview

AI Interviewer is a Python-based application that leverages Google's Gemini API to create an interactive interview simulation environment. Users can practice interviews in various domains with an AI-powered interviewer that asks questions and provides feedback.

## Features

- **Multi-field Interview Support**: Practice interviews across different professional fields
- **AI-Powered Questions**: Leverages Google Gemini API to generate contextually relevant interview questions
- **Interactive Interface**: User-friendly interface for conducting mock interviews
- **Real-time Responses**: Get instant feedback and follow-up questions from the AI interviewer

## Technology Stack

- **Language**: Python
- **AI/LLM**: Google Gemini API
- **Backend**: Custom Python backend with Gemini integration

## Project Structure

```
├── main.py                  # Main application entry point
├── gemini_backend.py       # Google Gemini API integration
├── .gitignore              # Git ignore configuration
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.7 or higher
- Google Gemini API key

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Pratham-2105/ai-interviewer.git
   cd ai-interviewer
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google Gemini API key:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

## Usage

Run the application:

```bash
python main.py
```

Follow the on-screen prompts to:
1. Select your interview field
2. Answer interview questions posed by the AI
3. Receive feedback and continue with follow-up questions

## API Configuration

The `gemini_backend.py` module handles all interactions with the Google Gemini API. Ensure your API key is properly configured before running the application.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

[Add your license here - e.g., MIT, Apache 2.0, etc.]

## Author

**Pratham-2105**

## Support

For issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/Pratham-2105/ai-interviewer).