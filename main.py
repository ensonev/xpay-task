from fastapi import HTTPException, status
from database import app, postgres_cursor, postgres_conn, mongo_db
from schema import UserRegistrationRequest, UserResponse

@app.post("/register/", tags=['User'])
async def register_user(user_data: UserRegistrationRequest):
    try:
        # Check if email already exists in PostgreSQL
        postgres_cursor.execute("SELECT email FROM users WHERE email = %s", (user_data.email,))
        existing_email = postgres_cursor.fetchone()

        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Insert user data into PostgreSQL
        postgres_cursor.execute(
            "INSERT INTO users (full_name, email, password, phone) VALUES (%s, %s, %s, %s) RETURNING user_id",
            (user_data.full_name, user_data.email, user_data.password, user_data.phone),
        )
        user_id = postgres_cursor.fetchone()[0]

        # Save profile picture binary data in MongoDB and link it with the user ID
        profile_picture_data = {"user_id": user_id, "profile_picture": user_data.profile_picture}
        mongo_db.profile_pictures.insert_one(profile_picture_data)

        postgres_conn.commit()
        return {"user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

@app.get("/user/{user_id}/", tags=['User'], status_code=status.HTTP_200_OK)
async def get_user_details(user_id: int):
    # Retrieve user details from PostgreSQL
    postgres_cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user_data = postgres_cursor.fetchone()

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Retrieve profile picture from MongoDB
    profile_picture_data = mongo_db.profile_pictures.find_one({"user_id": user_id})
    if profile_picture_data:
        profile_picture = profile_picture_data["profile_picture"]
    else:
        profile_picture = None

    user_details = {
        "user_id": user_id,
        "full_name": user_data[1],
        "email": user_data[2],
        "phone": user_data[4],
        "profile_picture": profile_picture,
    }
    return user_details