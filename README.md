### **📌 README.md**
```md
# 🚀 LinkedIn Job Scraper API

This project provides an API to fetch LinkedIn job postings based on a given keyword and time filter. It scrapes job postings dynamically and returns the data as JSON.

---

## 📂 Project Structure

```
📁 linkedin-job-scraper/
│── 📄 get_linkedin_job_data.py  # Web scraping logic for LinkedIn jobs
│── 📄 api_server.py             # FastAPI server to expose the scraping function as an API
│── 📄 README.md                 # Instructions to set up and run the project
```

---

## 📦 Installation

### **1️⃣ Prerequisites**
- **Python 3.7+** must be installed. Check the version:
  ```sh
  python --version
  ```

- Install required dependencies:
  ```sh
  pip install -r requirements.txt
  ```

  If `requirements.txt` is missing, manually install:
  ```sh
  pip install fastapi uvicorn requests beautifulsoup4
  ```

---

## 🚀 Running the API Server

### **2️⃣ Start the FastAPI Server**
Run the following command in the terminal:
```sh
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

- The API will now be running on **`http://127.0.0.1:8000`**

---

## 🛠️ API Usage

### **3️⃣ Fetch Job Listings**
Use the following **GET** request to fetch jobs:
```
http://127.0.0.1:8000/get_jobs?keyword=Data%20Engineer&time_filter=30
```

| Parameter    | Type  | Description |
|-------------|-------|-------------|
| `keyword`   | `str` | Job title or search keyword (e.g., `Data Engineer`) |
| `time_filter` | `int` | Jobs posted within the last X minutes (e.g., `30`) |

---

## 🛠️ Example Response
```json
[
    {
        "Job ID": "123456789",
        "Apply Link": "https://www.linkedin.com/jobs/view/123456789/",
        "Title": "Data Engineer",
        "Company Name": "Tech Corp",
        "Posted Time": "Just now",
        "Job Description": "Job description goes here..."
    }
]
```

---

## 🔄 Stopping the Server
Press `CTRL + C` in the terminal to stop the server.

---

## ❓ Troubleshooting

- If `uvicorn` is not found, try running:
  ```sh
  python -m uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
  ```

- If requests to LinkedIn fail, ensure:
  - You have a stable internet connection.
  - LinkedIn's structure hasn't changed (modify `get_linkedin_job_data.py` if needed).

---

## 📜 License
This project is for **educational purposes only**. Web scraping LinkedIn may violate its **terms of service**. Use responsibly.

---
