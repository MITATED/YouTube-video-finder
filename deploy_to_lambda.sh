#!/bin/bash
if [ ! -d "venv" ]; then
  rm deploy.zip
  python3.8 venv venv
  source venv/bin/activate
  pip install -r requirements.txt
fi

if [ -z "$1" ] && [ -f "deploy.zip" ]; then
  mkdir "tmp"
  cp *.py ./tmp/
  cd tmp
  zip -ur ../deploy.zip *.py
  cd ..
  rm -r tmp
  aws lambda update-function-code --function-name YouTube --zip-file fileb://deploy.zip
else
  rm deploy.zip
  mkdir "tmp"
  cp *.py ./tmp/
  cp -r ./venv/lib/python3.8/site-packages/* ./tmp/
  cd tmp
  zip -r9 ../deploy.zip *
  cd ..
  rm -r tmp
  aws lambda update-function-code --function-name YouTube --zip-file fileb://deploy.zip
fi

