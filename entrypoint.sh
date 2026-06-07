#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until python -c "
import os, sys
import sqlalchemy as db
engine = db.create_engine(os.environ['DATABASE_URL'])
with engine.connect() as conn:
    conn.execute(db.text('SELECT 1'))
" 2>/dev/null; do
  sleep 1
done
echo "PostgreSQL is ready."

python database.py
python seed-db.py
exec python app.py
