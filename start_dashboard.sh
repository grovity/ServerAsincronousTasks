#!/bin/bash
celery --broker=redis://redis:6379/0 flower --port=5556
