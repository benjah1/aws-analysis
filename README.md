> Working in Progress 

# aws-analysis

This package provides a command line interface to analyze AWS resource

## Getting Started

The easiest way to use this package is to use docker:

```
docker run -it --rm -$(pwd):/app python:3.6 bash

export AWS_ACCESS_KEY_ID="XXXXXX"
export AWS_SECRET_ACCESS_KEY="XXXXXX"
export AWS_DEFAULT_REGION="XXXXXX"

apt-get update && apt-get install groff -y

cd /app
pip install -r requirements.txt

python3 -m awsanalysis
```

