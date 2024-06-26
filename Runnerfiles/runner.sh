#!/bin/bash

# Start runnerFrontend.sh in a new terminal window
osascript <<EOF
tell application "Terminal"
    do script "cd $(pwd)/; ./runnerFrontend.sh"
end tell
EOF

# Navigate to backend directory
cd ..
cd ./backend/

# Check if requirements_satisfied.txt exists
if [ ! -e "requirements_satisfied.txt" ]; then
  echo "requirements installed" > "requirements_satisfied.txt"
  pip install -r requirements.txt
fi

# Run the Python application
python3 app.py
