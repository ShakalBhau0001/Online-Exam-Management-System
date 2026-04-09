import mysql.connector
import hashlib
from mysql.connector import Error

DB_CONFIG = {"host": "localhost", "port": 3306, "user": "root", "password": "root"}
DB_NAME = "online_examination"


def hp(p):
    return hashlib.md5(p.encode()).hexdigest()


def run():
    con = mysql.connector.connect(**DB_CONFIG)
    cur = con.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cur.execute(f"USE {DB_NAME}")
    print(f"✅ Database '{DB_NAME}' ready")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS signup (
            username VARCHAR(50)  PRIMARY KEY,
            name     VARCHAR(100) NOT NULL,
            contact  VARCHAR(15)  NOT NULL,
            email    VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(64)  NOT NULL
        )"""
    )
    print("✅ Table 'signup' ready")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS admin (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(64) NOT NULL
        )"""
    )
    print("✅ Table 'admin' ready")
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS exam_results (
            id           INT AUTO_INCREMENT PRIMARY KEY,
            username     VARCHAR(50)  NOT NULL,
            subject      VARCHAR(100) NOT NULL,
            score        INT NOT NULL,
            total        INT NOT NULL,
            passed       TINYINT(1) NOT NULL,
            attempt_date DATETIME NOT NULL,
            FOREIGN KEY (username) REFERENCES signup(username) ON DELETE CASCADE
        )"""
    )
    print("✅ Table 'exam_results' ready")

    # Sample students (3) - passwords will be hashed before insertion
    students = [
        ("rahul01", "Rahul Sharma", "9876543210", "rahul@gmail.com", "rahul123"),
        ("priya02", "Priya Patel", "9123456780", "priya@gmail.com", "priya456"),
        ("amit03", "Amit Verma", "9988776655", "amit@gmail.com", "amit789"),
    ]
    for u, n, c, e, p in students:
        cur.execute("DELETE FROM exam_results WHERE username=%s", (u,))
        cur.execute("DELETE FROM signup WHERE username=%s", (u,))
        cur.execute("INSERT INTO signup VALUES (%s,%s,%s,%s,%s)", (u, n, c, e, hp(p)))
        print(f"  ✅ Student inserted (hashed): {u}")

    # Default admin account
    cur.execute("DELETE FROM admin WHERE username='admin'")
    cur.execute("INSERT INTO admin VALUES (%s,%s)", ("admin", hp("admin123")))
    print("  ✅ Admin inserted → username: admin | password: admin123")
    con.commit()
    con.close()

    print("\n" + "─" * 45)
    print("🎉 Setup complete! Now run:")
    print("   python main.py")
    print("─" * 45)
    print("\nStudent logins:")
    print("  rahul01 / rahul123")
    print("  priya02 / priya456")
    print("  amit03  / amit789")
    print("\nAdmin login:")
    print("  admin   / admin123")


if __name__ == "__main__":
    try:
        run()
    except Error as e:
        print(f"❌ DB Error: {e}")
        print("👉 Please check your MySQL password in setup_db.py!")
