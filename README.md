Smart Device Care & Repair Tracker

A Python-based application to manage electronic device repair records and track repair progress through a command-line interface and a web dashboard.

Features

- Add and manage device repair records
- Track repair status: Received, In Progress, Ready for Pickup, and Delivered
- View repair records and repair summaries
- Search and update repair information
- Web dashboard with admin login
- Session-based login protection for dashboard routes
- Store repair records in JSON format

Live Demo

Live Website: https://smart-device-care-tracker.onrender.com

Note: The free hosting service may take some time to start after inactivity. Data stored in a local JSON file may not persist after restarts or redeployments.

Technologies Used

- Python
- Flask
- HTML
- JSON
- Git and GitHub
- Gunicorn
- Render (Deployment)

How to Run the Command-Line Version

1. Install Python.

2. Clone or download this repository.

3. Open the project folder in VS Code.

4. Run:
   
   python app.py

How to Run the Web Version

1. Install the required dependencies:
   
   pip install -r requirements.txt

2. Configure the required environment variables for the admin login and Flask secret key.

3. Start the web application locally:
   
   python web_app.py

4. Open the local address shown in the terminal.

Security note: Use environment variables for secrets and never commit passwords, password hashes, or secret keys to GitHub.

Project Objective

To simplify repair record management, organize repair information, and make it easier to monitor the progress of electronic device repairs.

Author

Rohan Gautam
