## Day 0 :

- Initialized the .venv
- Installed all dependencies
- Wrote main.py

Notes:
- for database, use postgresql (make database in postgres)
- just change the URL of DATABASE in database.py
- donot use Base.metadata.create_all(engine) in main.py, now Alembic will handle all those tasks

powershell: [all scripts inside ...\backend>]
``` 
alembic init alembic
```
- alembic.ini -> put the DATABASE URL 
- alembic\env.py :
1. from app.database import Base 
2. from app import models 
3. target_metadata = None -> target_metadata = Base.metadata
- any changes in models.py
```
alembic revision --autogenerate -m "message about what was changed"
alembic upgrade head
```
## Day 1 :

- Created most of the necessary tables for the app
- Fixed nullable issues
- User registration with unique and valid email
- Update user feature
- Update password after verifying the old password feature

## Day 2 :

- Created login route
- Added authentication and authorization using OAuth2
- Updated user update and password update routes according to logged in user
- Added own profile view
- Added public user profile view
- Added account delete after verification

## Day 3 :

- Added user profile picture upload and update
- Added room post
- Added room stats update only by the owner
- Added room view (specific and general)
- Added room delete only by the owner

## Day 4 :

- Added filtered search for room using query parameters
- Added multiple photo uploads of the room

## Day 5 :