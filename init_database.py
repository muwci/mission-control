from contextlib import closing

from mission_control import app
from mission_control.database import connect_db


def init_db():
    print("\nInitializing database...")

    with closing(connect_db()) as db:
        print("Creating new tables...", end="")
        with app.open_resource('reset.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        print("\t\t DONE.")

        print("Populating database...", end="")
        with app.open_resource('populate.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

        c = db.execute("""
            SELECT username
            FROM users
            WHERE acctype='STU'
        """)

        for (student,) in c.fetchall():
            for term in range(1, 5):
                db.execute("""
                    INSERT INTO grades
                    (username, term)
                    VALUES (?, ?)
                """, (student, term))
        db.commit()
        print("\t\t DONE.")

    print("Done initializing database.")


if __name__ == '__main__':
    print("This will purge the existing database")
    print("and all data will be removed.")
    print("")
    inp = input("ARE YOU SURE YOU WANT TO CONTINUE [y/N]? ")

    if str(inp).lower() == 'y':
        init_db()
