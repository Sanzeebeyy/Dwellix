## Day 0 :

- Initialized the .venv
- Installed all dependencies
- Wrote main.py

Notes:
- for database, use postgresql (make database in postgres)
- just change the URL of DATABASE in database.py
- donot use Base.metadata.create_all(engine) in main.py, Now Alembic will handle all those tasks

powershell: [all scripts inside ...\backend>]
``` 
alembic init alembic
```
- alembic.ini -> put the DATABASE URL 
- alembic/env.py, 
    from app.database import Base 
    from app import models 
    target_metadata = None -> target_metadata = Base.metadata
- any changes in models.py
```
alembic revision --autogenerate -m "message about what was changed"
alembic upgrade head
```
## Day 1 :
