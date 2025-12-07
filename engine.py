from pathlib import Path

from sqlmodel import create_engine

# Remove-me later.
Path("database.db").unlink(True)

# This will not connect to database, it will only
# create the object to handle connections when needed.
engine = create_engine("sqlite:///database.db")
