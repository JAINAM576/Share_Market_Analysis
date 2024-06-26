#!/bin/bash

# Navigate to the Frontend directory
cd ..
cd ./Frontend/

# Check if node_modules.txt exists
if [ ! -e "node_modules.txt" ]; then
  echo "Node modules installed" > node_modules.txt
  npm install && npm run dev
else
  npm run dev
fi
