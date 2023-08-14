#!/bin/bash

if [ "$SERVICE_TYPE" = "web" ]; then
    uvicorn project.main:app --host 0.0.0.0 --port 8004
elif [ "$SERVICE_TYPE" = "worker" ]; then
    celery -A worker.celery worker --loglevel=info --logfile=logs/celery.log
elif [ "$SERVICE_TYPE" = "dashboard" ]; then
    celery --broker=redis://redis:6379/0 flower --port=5555
else
    echo "Invalid service type"
fi
