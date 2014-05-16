#!/bin/bash
curl -H "Content-Type: application/json" -d "{\"filename\": \"$1\"}" http://localhost:8080
