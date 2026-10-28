# 📰 AI News Agent

A fully autonomous news agent that researches topics on the web and generates beautifully styled HTML webpages for your news. 

It is built completely from scratch using **pure Python and `httpx`**. No external AI libraries, SDKs, or frameworks (like LangChain) were used. 

## 🛠️ Tools Used

The agent dynamically decides which of these Python tools to call:
*   **`search_google`**: Searches the web for a query and returns the top URLs.
*   **`fetch_url`**: Fetches a URL and extracts the readable text.
*   **`save_to_file`**: Takes the AI's generated HTML/CSS and saves it as a webpage on your computer.

## 🧠 Why I Built This

This is my final API project. I built this to paractice my understanding of core API concepts, including:
*   HTTP requests and JSON manipulation.
*   Stateful conversation history.
*   Tool calling and error handling .
*   Modular and scalable architecture.

**Note:** To run this, copy the `user_api.py` and `safe_get.py` files from the main folder into this folder, add your `GEMINI_API_KEY` to a `.env` file, and run `main.py`.