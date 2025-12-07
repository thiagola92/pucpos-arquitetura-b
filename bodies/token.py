from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm


PostBody = Annotated[OAuth2PasswordRequestForm, Depends()]
