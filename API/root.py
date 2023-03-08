from fastapi import FastAPI, HTTPException, status
import Classes.verify_email as verify
import Classes.user as user_class
import Classes.send_email as send_email
import os

app = FastAPI()
my_password = os.getenv("PASSWORD")
my_email = os.getenv("EMAIL")

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/validate_users/{user_id}")
async def validate_email(user_id: str):
    user = verify.VERIFY_USER()
    user_found = user.get_user(user_id)
    if user_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The link has expired")
    try:
        user_class.USER().create_user(user_found["email"])
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has already signed up")
    user.delete_user(user_found["_id"])
    return {"detail": "You have successfully registered"}


@app.get("/validate_delete_user/{user_id}")
async def validate_delete_email(user_id: str):
    user = user_class.USER()
    user_found = user.get_users_with_id(IDS=user_id)
    if user_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The link has expired")
    try:
        user.delete_user(ids=user_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The link has expired")
    return {"detail": "You have unregistered from our services"}


@app.get("/create_user/{email}")
async def _user(email: str):
    user = user_class.USER()
    user_found = user.get_users(email=email)
    if user_found is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You're already signed up")
    users = verify.VERIFY_USER()
    user_verify = users.create_user(email)
    if user_verify is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please wait 10 minutes before trying again")
    url = f"http://127.0.0.1:8000/validate_users/{user_verify}"
    sending = send_email.EmailSender(my_email, my_password)
    sending.send_verification_create_email(to_email=email, subject="Verify your email account", url=url)
    return {"detail": "Success"}


@app.get("/delete_user/{email}")
async def _user_delete(email: str):
    user = user_class.USER()
    user_found = user.get_users(email=email)
    if user_found is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You're not registered for our services")
    url = f"http://127.0.0.1:8000/validate_delete_user/{user_found['_id']}"
    sending = send_email.EmailSender(my_email, my_password)
    sending.send_verification_delete_email(to_email=email, subject="Verify your email account", url=url)
    return {"detail": "You have successfully unregistered from our services"}

