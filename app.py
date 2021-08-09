from website import create_app
from flask import Flask

with connection.cursor() as cursor:
    cursor.execute('SELECT COUNT(*) FROM users')
    result = cursor.fetchone()
print(result)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
