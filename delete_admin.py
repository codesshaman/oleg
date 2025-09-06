# delete_admin.py
import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('hypnovirus.db')
cursor = conn.cursor()

# Удаляем пользователя с username = 'admin'
try:
    cursor.execute("DELETE FROM users WHERE username = 'admin'")
    print("Пользователь 'admin' удалён.")
except Exception as e:
    print(f"Ошибка: {e}")

# Сохраняем изменения
conn.commit()

# Проверим, кто остался
cursor.execute("SELECT * FROM users;")
print("Оставшиеся пользователи:")
for row in cursor.fetchall():
    print(row)

# Закрываем соединение
conn.close()