from app.api import app

app = app.create_app()

if __name__ == '__main__':
    app.run(debug=False)