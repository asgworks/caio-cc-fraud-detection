#!/bin/bash

# Test the Fraud Detection API

API_URL="http://localhost:8000"

echo "=== Testing Fraud Detection API ==="
echo ""

# 1. Health Check
echo "1. Health Check:"
curl -s ${API_URL}/health | python -m json.tool
echo ""
echo ""

# 2. Predict - Low Risk Transaction
echo "2. Low Risk Transaction (Small amount):"
curl -s -X POST ${API_URL}/predict \
  -H "Content-Type: application/json" \
  -d '{
    "trans_num": "txn_001",
    "cc_num": "1234567890123456",
    "merchant": "Starbucks",
    "amt": 5.50,
    "city_pop": 50000,
    "category_encoded": 8,
    "gender_encoded": 1,
    "state_encoded": 5
  }' | python -m json.tool
echo ""
echo ""

# 3. Predict - High Risk Transaction
echo "3. High Risk Transaction (Large amount):"
curl -s -X POST ${API_URL}/predict \
  -H "Content-Type: application/json" \
  -d '{
    "trans_num": "txn_002",
    "cc_num": "9876543210987654",
    "merchant": "Unknown Store",
    "amt": 9999.99,
    "city_pop": 100,
    "category_encoded": 2,
    "gender_encoded": 0,
    "state_encoded": 10
  }' | python -m json.tool
echo ""
echo ""

# 4. Predict - Normal Transaction
echo "4. Normal Transaction:"
curl -s -X POST ${API_URL}/predict \
  -H "Content-Type: application/json" \
  -d '{
    "trans_num": "txn_003",
    "cc_num": "5555555555555555",
    "merchant": "Amazon",
    "amt": 49.99,
    "city_pop": 250000,
    "category_encoded": 4,
    "gender_encoded": 1,
    "state_encoded": 27
  }' | python -m json.tool

echo ""
echo "=== Tests Complete ==="
