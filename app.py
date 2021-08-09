from website import create_app
from flask import Flask

app = create_app()

select * from users where user_name = '$user' and password = '$pass'

if __name__ == '__main__':
    app.run(debug=True)
