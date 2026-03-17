# Golden Record Validator

A multi-company insurance data verification tool. Ensure policy data adheres strictly to authoritative "Golden Records" across Max Life, Tata, HDFC, ICICI, and Bajaj Allianz.

## 🚀 Quick Start (Local Setup)

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

## 🛠 Project Structure

- `api.py`: FastAPI backend containing the core validation logic and Golden Records.
- `client/`: React frontend (Vite + Tailwind CSS + Framer Motion).
- `setup.sh`: One-click environment setup script.
- `run.sh`: One-click application launch script.
- `requirements.txt`: Python dependencies.

## 🔒 Security Note
- `credentials.json` and `token.pickle` are ignored by Git. If you need to use the Google Sheets sync features (found in `validator.py`), ensure you place your authorized `credentials.json` in the root directory.
- The default "Audit Portal" uses hardcoded Golden Records in `api.py` for maximum reliability during demonstrations.

## ✅ Stakeholder Prototype Ready
This project is configured with a local proxy to handle API calls seamlessly. It is ready for high-fidelity demonstrations of the multi-company selection and CSV validation workflow.
