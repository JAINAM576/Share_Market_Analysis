#!/bin/bash

=osascript <<EOF
tell application "Terminal"
    do script "cd $(pwd)/; ./runnerFrontend.sh"
end tell
EOF



cd ..
cd ./backend/



if [ ! -e "requirements_satisfied.txt" ]; then
  echo "requirements installed" > "requirements_satisfied.txt"
  pip install -r requirements.txt
fi



python3 app.py
