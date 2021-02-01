#!/bin/bash

echo ""
echo "Use: $0 ./constrained_rw.py"
echo ""

echo "Executing $1 ..."

EXIT_CODE=1
(while [ $EXIT_CODE -gt 0 ]; do
    $1
    EXIT_CODE=$?
done)
