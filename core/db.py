import mysql.connector
import hashlib
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "online_examination",
    "user": "root",
    "password": "root",
}


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"[DB Error] {e}")
        return None


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


# ── Auth


def validate_login(username: str, password: str) -> bool:
    con = get_connection()
    if not con:
        return False
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM signup WHERE username=%s AND password=%s",
            (username, hash_password(password)),
        )
        return cur.fetchone() is not None
    except Error as e:
        print(e)
        return False
    finally:
        con.close()


def validate_admin(username: str, password: str) -> bool:
    con = get_connection()
    if not con:
        return False
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, hash_password(password)),
        )
        return cur.fetchone() is not None
    except Error as e:
        print(e)
        return False
    finally:
        con.close()


# ── Signup


def username_exists(username: str) -> bool:
    con = get_connection()
    if not con:
        return False
    try:
        cur = con.cursor()
        cur.execute("SELECT username FROM signup WHERE username=%s", (username,))
        return cur.fetchone() is not None
    finally:
        con.close()


def email_exists(email: str) -> bool:
    con = get_connection()
    if not con:
        return False
    try:
        cur = con.cursor()
        cur.execute("SELECT email FROM signup WHERE email=%s", (email,))
        return cur.fetchone() is not None
    finally:
        con.close()


def insert_student(
    username: str, name: str, contact: str, email: str, password: str
) -> bool:
    con = get_connection()
    if not con:
        return False
    try:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO signup VALUES (%s,%s,%s,%s,%s)",
            (username, name, contact, email, hash_password(password)),
        )
        con.commit()
        return True
    except Error as e:
        print(e)
        return False
    finally:
        con.close()


# ── Exam Results


def save_result(
    username: str, subject: str, score: int, total: int, passed: bool
) -> bool:
    con = get_connection()
    if not con:
        return False
    try:
        cur = con.cursor()
        cur.execute(
            """INSERT INTO exam_results
            (username, subject, score, total, passed, attempt_date)
            VALUES (%s,%s,%s,%s,%s,NOW())""",
            (username, subject, score, total, passed),
        )
        con.commit()
        return True
    except Error as e:
        print(e)
        return False
    finally:
        con.close()


def get_student_history(username: str) -> list:
    con = get_connection()
    if not con:
        return []
    try:
        cur = con.cursor()
        cur.execute(
            """SELECT subject, score, total, passed, attempt_date
            FROM exam_results WHERE username=%s
            ORDER BY attempt_date DESC""",
            (username,),
        )
        return cur.fetchall()
    except Error as e:
        print(e)
        return []
    finally:
        con.close()


def get_subject_performance(username: str) -> list:
    con = get_connection()
    if not con:
        return []
    try:
        cur = con.cursor()
        cur.execute(
            """SELECT subject,
            COUNT(*) AS attempts,
            ROUND(AVG(score/total*100), 1) AS avg_percent,
            MAX(score) AS best_score,
            SUM(passed) AS pass_count
            FROM exam_results WHERE username=%s
            GROUP BY subject""",
            (username,),
        )
        return cur.fetchall()
    except Error as e:
        print(e)
        return []
    finally:
        con.close()


# ── Admin


def get_all_students() -> list:
    con = get_connection()
    if not con:
        return []
    try:
        cur = con.cursor()
        cur.execute("SELECT username, name, contact, email FROM signup ORDER BY name")
        return cur.fetchall()
    except Error as e:
        print(e)
        return []
    finally:
        con.close()


def delete_student(username: str) -> bool:
    con = get_connection()
    if not con:
        return False
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM exam_results WHERE username=%s", (username,))
        cur.execute("DELETE FROM signup WHERE username=%s", (username,))
        con.commit()
        return True
    except Error as e:
        print(e)
        return False
    finally:
        con.close()


def get_all_results() -> list:
    con = get_connection()
    if not con:
        return []
    try:
        cur = con.cursor()
        cur.execute(
            """SELECT r.username, s.name, r.subject,
            r.score, r.total, r.passed, r.attempt_date
            FROM exam_results r
            JOIN signup s ON r.username = s.username
            ORDER BY r.attempt_date DESC"""
        )
        return cur.fetchall()
    except Error as e:
        print(e)
        return []
    finally:
        con.close()


def get_dashboard_stats() -> dict:
    con = get_connection()
    if not con:
        return {}
    try:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM signup")
        total_students = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM exam_results")
        total_exams = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM exam_results WHERE passed=1")
        total_pass = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM exam_results WHERE passed=0")
        total_fail = cur.fetchone()[0]

        cur.execute(
            """SELECT subject, COUNT(*) as cnt
            FROM exam_results GROUP BY subject ORDER BY cnt DESC"""
        )
        subject_attempts = cur.fetchall()

        return {
            "total_students": total_students,
            "total_exams": total_exams,
            "total_pass": total_pass,
            "total_fail": total_fail,
            "subject_attempts": subject_attempts,
        }
    except Error as e:
        print(e)
        return {}
    finally:
        con.close()
