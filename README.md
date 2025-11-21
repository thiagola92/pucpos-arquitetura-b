# pucpos-arquitetura-b

# Usage

Make sure to install uv: https://docs.astral.sh/uv/getting-started/installation/

Install dependencies:

```
uv sync
```

Then start the project in development mode:

```
uv run fastapi dev app.py
```

# Container

```
# Build image
sudo docker image build --tag "pucpos-b" .

# Create container
sudo docker container create --publish 8000:8000 --name "pucpos-b" pucpos-b

# Start container
sudo docker container start --attach pucpos-b
```

```
# Remove container and image
sudo docker container stop pucpos-b
sudo docker container rm pucpos-b
sudo docker image rm pucpos-b
```

# References

- https://fastapi.tiangolo.com/
- https://fakestoreapi.com/
