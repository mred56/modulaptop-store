### To autogenerate new migration run:
```
alembic revision -m "migration name" --autogenerate
```

### To run migrations on a database in config.py file, run:
```
alembic upgrade head
``` 

### To undo a migration run:
```
alembic downgrade -1
```
