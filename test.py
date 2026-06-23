from sqlalchemy import inspect
from backend.database import engine

print(inspect(engine).get_table_names())