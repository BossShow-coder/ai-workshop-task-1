# DE Team Standup Tracker

A daily update board where team members post their work status and blockers, giving the team leader a real-time view of progress and a one-click summary report.

## Running on Windows

To run the application on Windows, follow these steps:

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd ai-workshop-task-1/team-standup-tracker
   ```

2. **Install Dependencies**:
   It is recommended to use a virtual environment, but you can install them directly:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Start the Server**:
   Run the application using the Python module interface to avoid "command not found" errors:
   ```powershell
   python -m uvicorn main:app --port 8000
   ```

4. **Access the App**:
   Open your browser and go to: [http://localhost:8000](http://localhost:8000)

## Running with Docker

If you have Docker installed, you can run the app as a container:

1. **Build the image**:
   ```bash
   docker build -t standup-tracker .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 standup-tracker
   ```

## Features
- **Dashboard**: View latest updates and highlighted blockers.
- **Post Updates**: Submit daily work status.
- **Search**: Find previous updates by keyword.
- **Reports**: Generate summary reports of team activity.
- **Member Management**: Add team members to the tracker.
