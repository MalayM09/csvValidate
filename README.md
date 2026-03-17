# Golden Record Validator

A multi-company insurance data verification tool. Ensure policy data adheres strictly to authoritative "Golden Records" across Max Life, Tata, HDFC, ICICI, and Bajaj Allianz.

##  Quick Start (Local Setup)

If you are a collaborator cloning this repository, follow these steps to get it running on your Mac:

### 1. Initial Setup
Run the automated setup script to create the virtual environment and install all dependencies:
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Start the Application
Run the start script to launch both the FastAPI backend and the React frontend simultaneously:
```bash
chmod +x run.sh
./run.sh
```
The tool will be available at [http://localhost:5173](http://localhost:5173).

---

##  Project Structure

- `api.py`: FastAPI backend containing the core validation logic and Golden Records.
- `client/`: React frontend (Vite + Tailwind CSS + Framer Motion).
- `setup.sh`: One-click environment setup script.
- `run.sh`: One-click application launch script.
- `requirements.txt`: Python dependencies.

