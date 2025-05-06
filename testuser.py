from app import create_app, db
from app.models import User

def create_user(name, email, role, password):
    if not User.query.filter_by(email=email).first():
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        print(f"Usuario creado: {name} ({role})")
    else:
        print(f"Ya existe el usuario: {email}")

app = create_app()
app.app_context().push()  # Necesario para trabajar con la DB

# Crear usuarios de prueba
create_user("Carlos Espinoza", "cespinoza@atentus.com", "admin", "pass")
create_user("Javier Chandia", "jchandia@atentus.com", "leader", "1q2w3e4r5t")
#create_user("Fernando Lizana", "flizana@atentus.com", "leader", "leader123")
#create_user("Lardin Armas ", "leader2@test.com", "leader", "leader123")



#create_user("Martin Mondaca ", "collab@test.com", "participant", "collab123")

db.session.commit()
print("✅ Usuarios cargados correctamente.")
