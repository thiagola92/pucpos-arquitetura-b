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

This will watch the project directory and restart as necessary.

Access through http://127.0.0.1:8000

> [!IMPORTANT]
> Environment variable `SECRET_KEY` is used to encrypt JWT. If not defined, it
> will use a default a hardcoded key (which is not recommended).

# Container

```shell
# Create network (if doesn't exist)
sudo docker network create --driver bridge pucpos

# Build image
sudo docker image build --tag "pucpos-b" .

# Create container
sudo docker container create --network pucpos --publish 8000:8000 --name "pucpos-b" pucpos-b

# Start container
sudo docker container start --attach pucpos-b
```

```shell
# Remove container and image
sudo docker container stop pucpos-b
sudo docker container rm pucpos-b
sudo docker image rm pucpos-b
sudo docker network rm pucpos
```

# References

- https://fastapi.tiangolo.com/
- https://fakestoreapi.com/
- https://fastapi.tiangolo.com/tutorial/security/first-steps/
- https://fastapi.tiangolo.com/advanced/additional-status-codes/
