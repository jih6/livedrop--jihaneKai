import requests
import json
from datetime import datetime

print("DEBUG: Script started")

NGROK_URL = "https://unbasted-virally-rylie.ngrok-free.dev"
LOG_FILE = "chat_logs.txt"  # file where we save the logs
MAX_LINES = 5  # maximum lines to display/log

def log_conversation(question, answer, sources, confidence):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Q: {question}\n")
        f.write(f"A: {answer}\n")
        f.write(f"Sources: {sources}\n")
        f.write(f"Confidence: {confidence}\n")
        f.write("---\n")

def truncate_answer(answer, max_lines=MAX_LINES):
    """Limit the answer to a maximum number of lines."""
    lines = answer.splitlines()
    truncated = lines[:max_lines]
    if len(lines) > max_lines:
        truncated.append("... [truncated]")
    return "\n".join(truncated)

def send_question(question):
    print(f"DEBUG: Sending question: {question}")
    payload = {"query": question}
    try:
        response = requests.post(f"{NGROK_URL}/chat", json=payload)
        print(f"DEBUG: Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            # Deduplicate answer if backend misbehaves
            answer = data.get("answer", "").strip()
            answer = " ".join(dict.fromkeys(answer.splitlines()))  # remove repeated lines
            answer = truncate_answer(answer)  # truncate to MAX_LINES
            sources = list(dict.fromkeys(data.get("sources", [])))  # deduplicate sources
            confidence = data.get("confidence", "Unknown")

            # Print to terminal
            print("\nAnswer:", answer)
            print("Sources:", sources)
            print("Confidence:", confidence)

            # Save to log
            log_conversation(question, answer, sources, confidence)

        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Connection error:", e)
        log_conversation(question, f"Connection error: {e}", [], "Unknown")

if __name__ == "__main__":
    print("Welcome to the Shoplite RAG Assistant!")
    print("Type 'exit' to quit.\n")

    while True:
        user_question = input("> ")
        if user_question.lower() == "exit":
            print("Goodbye!")
            break
        print("[Retrieving context...]")
        print("[Calling LLM...]")
        send_question(user_question)
