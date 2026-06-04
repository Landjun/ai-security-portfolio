"""
demo.py —— SQL 注入(SQLi)本地靶场:不安全 vs 安全 对比。

原理:把用户输入直接拼进 SQL 语句,攻击者就能改变语句结构,绕过登录、窃取数据。
本演示用内存 sqlite3,完全本地、无害,仅用于理解原理与防御。

运行:  python demo.py
"""

import sqlite3


def make_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users(username TEXT, password TEXT, role TEXT)")
    conn.executemany("INSERT INTO users VALUES(?,?,?)", [
        ("admin", "S3cret!", "admin"),
        ("alice", "alice123", "user"),
    ])
    conn.commit()
    return conn


def login_vulnerable(conn, username, password):
    """不安全:把输入直接拼进 SQL(字符串拼接)。"""
    sql = f"SELECT role FROM users WHERE username='{username}' AND password='{password}'"
    print(f"    实际执行的SQL: {sql}")
    row = conn.execute(sql).fetchone()
    return row[0] if row else None


def login_secure(conn, username, password):
    """安全:参数化查询,输入只当数据、不当代码。"""
    sql = "SELECT role FROM users WHERE username=? AND password=?"
    row = conn.execute(sql, (username, password)).fetchone()
    return row[0] if row else None


def line():
    print("-" * 60)


if __name__ == "__main__":
    conn = make_db()
    # 经典注入载荷:用 ' OR '1'='1 让 WHERE 永真;-- 注释掉后面的密码校验
    attack_user = "admin' --"
    attack_pwd = "随便填"

    print("=" * 60)
    print("SQL 注入演示")
    print("=" * 60)

    print("正常登录(alice / alice123):")
    print("  结果:", login_secure(conn, "alice", "alice123"))

    line()
    print("[不安全版] 攻击者用户名输入: admin' --  (密码乱填)")
    role = login_vulnerable(conn, attack_user, attack_pwd)
    print(f"  登录结果: {role}   <- 注入成功!无需密码就以 admin 登录")

    line()
    print("[安全版] 同样的注入载荷,改用参数化查询:")
    role = login_secure(conn, attack_user, attack_pwd)
    print(f"  登录结果: {role}   <- 注入失败(输入被当作普通数据)")

    line()
    print("\n结论:字符串拼接 SQL = 把输入当代码执行;参数化查询把输入只当数据,从根本上免疫注入。")
