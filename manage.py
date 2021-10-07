from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run("192.168.50.51", debug=True)