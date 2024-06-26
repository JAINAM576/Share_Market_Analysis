cd ..
cd .\Frontend\

if exist "node_modules.txt" goto already_run

echo "Node modules installed" >  node_modules.txt
npm i && npm run dev 
goto finish

:already_run 
npm run dev 

:finish
