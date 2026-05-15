import sqlite3
import bcrypt

# -----------------------------------
# DATABASE
# -----------------------------------

conn = sqlite3.connect(

    "users.db",

    check_same_thread=False
)

cursor = conn.cursor()

# -----------------------------------
# CREATE TABLE
# -----------------------------------

cursor.execute(

    """

    CREATE TABLE IF NOT EXISTS users (

        username TEXT PRIMARY KEY,

        password TEXT

    )

    """
)

conn.commit()

# -----------------------------------
# CREATE USER
# -----------------------------------

def create_user(

    username,

    password
):

    hashed = bcrypt.hashpw(

        password.encode(),

        bcrypt.gensalt()
    )

    try:

        cursor.execute(

            """

            INSERT INTO users (

                username,

                password

            )

            VALUES (?, ?)

            """,

            (

                username,

                hashed
            )
        )

        conn.commit()

        return True

    except:

        return False

# -----------------------------------
# LOGIN USER
# -----------------------------------

def login_user(

    username,

    password
):

    cursor.execute(

        """

        SELECT password

        FROM users

        WHERE username=?

        """,

        (username,)
    )

    data = cursor.fetchone()

    if data:

        stored_password = data[0]

        return bcrypt.checkpw(

            password.encode(),

            stored_password
        )

    return False
