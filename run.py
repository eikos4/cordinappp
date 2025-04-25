from app import create_app

app = create_app()


# Opcional: comandos de línea para interactuar con la base de datos
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    app.run(debug=True)
