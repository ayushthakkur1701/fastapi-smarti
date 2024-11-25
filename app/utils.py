from passlib.context import CryptContext

# creating content from PassLib to Hash the password
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# Function to retunr hashed password

def hash(some_text:str):
    hashed_text = pwd_context.hash(some_text)
    return hashed_text

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)