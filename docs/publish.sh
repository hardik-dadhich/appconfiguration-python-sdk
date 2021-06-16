#!/bin/bash

cd $(dirname $0)
pwd

echo "Create Docs"
make document
echo "Created docs. Check _build/html folder."