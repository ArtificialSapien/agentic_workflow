# **Agentic Workflow**

Agentic Workflow is an innovative platform that leverages AI to identify emerging technologies before they go mainstream and transforms them into engaging content for your audience – including social media posts, videos, and memes.

---

## **Table of Contents**

1. [About the Project](#about-the-project)
2. [Technology Stack](#technology-stack)
3. [Features](#features)
4. [Requirements](#requirements)
5. [Installation](#installation)
6. [Getting Started](#getting-started)
7. [Project Structure](#project-structure)
8. [Contributing](#contributing)
9. [Contact](#contact)
10. [License](#license)

---

## **About the Project**

Agentic Workflow combines a robust backend for data processing and AI models with a responsive frontend for user interaction. Our goal is to make next-generation technologies intuitive and accessible.

The project has two main components:
- **Backend:** Handles data processing, AI analysis, and provides APIs used by the frontend.
- **Frontend:** Offers a user-friendly interface to interact with the platform and view AI analysis results in real-time.

---

## **Technology Stack**

### Backend
- **Programming Language:** Python (3.11.10, 3.12.7)
- **Framework:** FastAPI, Uvicorn
- **Functions:** 
  - AI analysis and processing
  - RESTful API endpoints
  - Real-time interactions via Websockets

### Frontend
- **Technology:** React.js with Vite
- **Programming Language:** TypeScript
- **Features:**
  - Responsive design
  - Real-time visualizations
  - Intuitive navigation

---

## **Features**

- **Automated Technology Trend Detection:** Identifies trends using AI algorithms.
- **Content Generation:** Transforms insights into content like posts, videos, and memes.
- **Real-time Analysis:** Allows users to analyze technologies in real-time and share insights.
- **Interactive Interface:** Delivers an intuitive and smooth user experience with modern frontend technologies.

---

## **Requirements**

Ensure the following software is installed:
- Python (version 3.11.10 or 3.12.7)
- Node.js (version 18+)
- npm (version 8+)
- A package manager like `pip` for Python dependencies

---

## **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/ArtificialSapien/agentic_workflow.git
   cd agentic-workflow
   ```

2. Install backend dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

---

## **Getting Started**

### **Start the Backend**
1. Ensure you are in the project root directory:
   ```bash
   cd agentic-workflow
   ```

2. Start the backend:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Open the API documentation in your browser:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### **Start the Frontend**
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open the application in your browser:
   [http://127.0.0.1:3000](http://127.0.0.1:3000)

---

### **Start Both Frontend and Backend**

Use the provided script to start both components:

1. Ensure the script is executable:
   ```bash
   chmod +x start_project.sh
   ```

2. Run the script:
   ```bash
   ./start_project.sh
   ```

The script checks for open ports, starts the servers, and synchronizes the components.

---

## **Contributing**

We welcome contributions to this project! To get started:

1. Fork the repository.
2. Create a new branch for your changes:
   ```bash
   git checkout -b feature-name
   ```
3. Submit a pull request once your changes are ready.

---

## **Contact**


---

## **License**

This project is licensed under the MIT License. For details, see the [LICENSE](LICENSE) file.
