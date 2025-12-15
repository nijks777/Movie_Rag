#!/bin/bash

echo "Testing FastAPI Endpoints..."
echo ""

echo "1. Health Check:"
curl http://localhost:8000/health
echo -e "\n"

echo "2. Corrective Search:"
curl -X POST http://localhost:8000/search/corrective \
  -H 'Content-Type: application/json' \
  -d '{"query": "action movies", "k": 2}'
echo -e "\n"
