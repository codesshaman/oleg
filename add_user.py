# add_user.py
import sqlite3

# Подключаемся к базе
conn = sqlite3.connect('hypnovirus.db')
cursor = conn.cursor()

# Новый пользователь
username = 'hacker'
password_hash = '$argon2id$v=19$m=102400,t=2,p=8$uHDCKbwF1PKZFmYks1iJ7g$CPB3khp+jwvckLFRmIg6DUL4ybAeM1TGRGEVX0UBSLU'

# Вставляем
try:
    cursor.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )
    print(f"[+] Пользователь '{username}' успешно добавлен.")
except sqlite3.IntegrityError:
    print(f"[-] Пользователь '{username}' уже существует.")
except Exception as e:
    print(f"[-] Ошибка: {e}")

# Сохраняем и закрываем
conn.commit()
conn.close()
