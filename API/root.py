'''
This is the main file where the code for the API is written. This is being called by the frontend.
'''

# Importing packages
from fastapi import FastAPI, HTTPException, status
import Classes.verify_email as verify
import Classes.user as user_class
import Classes.send_email as send_email
import os

# Initializing
app = FastAPI()
my_password = os.getenv("PASSWORD")
my_email = os.getenv("EMAIL")

@app.get("/")
async def root():
    return {"message": "hello world"}


# The verification link that will be sent through email will hit this endpoint
@app.get("/validate_users/{user_id}")
async def validate_email(user_id: str):
    # Check if user is present in the verification collection
    user = verify.VERIFY_USER()
    user_found = user.get_user(user_id)
    if user_found is None:
        # If user is not found then the link has expired
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The link has expired")
    # Create the user in the main users collection
    try:
        user_class.USER().create_user(user_found["email"])
    except:
        # If user is already present
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already signed up")
    # Deleting the user from the verification collection
    user.delete_user(user_found["_id"])
    return {"detail": "You have successfully registered"}


# The verification link to delete account will hit this endpoint
@app.get("/validate_delete_user/{user_id}")
async def validate_delete_email(user_id: str):
    # Check if user is present in the main users collection
    user = user_class.USER()
    user_found = user.get_users_with_id(IDS=user_id)
    if user_found is None:
        # If user is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The link has expired")
    # Deleting the user
    try:
        user.delete_user(ids=user_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The link has expired")
    return {"detail": "You have unregistered from our services"}

# This is the endpoint that will be hit by the frontend to create user
@app.get("/create_user/{email}")
async def _user(email: str):
    # Checking if user isn't already signed up
    user = user_class.USER()
    user_found = user.get_users(email=email)
    if user_found is not None:
        # If user is already signed up
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You're already signed up")
    # Checking if user is present in the verification collection
    users = verify.VERIFY_USER()
    user_verify = users.create_user(email)
    if user_verify is None:
        # If user is present then wait 10 minutes before trying to enter your email address again
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please wait 10 minutes before trying again")
    # Preparing the verification url
    url = f"http://127.0.0.1:8000/validate_users/{user_verify}"
    # Sending email
    sending = send_email.EmailSender(my_email, my_password)
    sending.send_verification_create_email(to_email=email, subject="Verify your email account", url=url)
    return {"detail": "Success"}

# This is the endpoint that will be hit by the frontend to delete a user
@app.get("/delete_user/{email}")
async def _user_delete(email: str):
    # Checking if user is present
    user = user_class.USER()
    user_found = user.get_users(email=email)
    if user_found is None:
        # If user is not present
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You're not registered for our services")
    # Preparing the URL
    url = f"http://127.0.0.1:8000/validate_delete_user/{user_found['_id']}"
    # Sending the email
    sending = send_email.EmailSender(my_email, my_password)
    sending.send_verification_delete_email(to_email=email, subject="Verify your email account", url=url)
    return {"detail": "You have successfully unregistered from our services"}

