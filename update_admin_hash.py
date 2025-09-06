# update_admin_hash.py
import sqlite3

# Подключаемся к базе данных
db_file = 'hypnovirus.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Ваш хэш
new_hash = '$argon2id$v=19$m=102400,t=2,p=8$uHDCKbwF1PKZFmYks1iJ7g$CPB3khp+jwvckLFRmIg6DUL4ybAeM1TGRGEVX0UBSLU'

# Обновляем хэш у пользователя admin
try:
    cursor.execute(
        "UPDATE users SET password_hash = ? WHERE username = 'admin'",
        (new_hash,)
    )
    if cursor.rowcount > 0:
        print("[+] Хэш пользователя 'admin' успешно обновлён.")
    else:
        print("[-] Пользователь 'admin' не найден.")
except Exception as e:
    print(f"[-] Ошибка при обновлении: {e}")

# Проверим результат
cursor.execute("SELECT id, username, password_hash FROM users WHERE username = 'admin';")
rows = cursor.fetchall()

print("\n[+] Текущие данные admin:")
for row in rows:
    print(f"ID: {row[0]}, Username: {row[1]}")
    print(f"Hash: {row[2]}")

# Сохраняем изменения и закрываем
conn.commit()
conn.close()
