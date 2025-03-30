# seed_users.py (script opcional)
from app import app
from project.models import db, User

with app.app_context():
    # Crear 6 usuarios
    names = ["j.chandia", "l.armas", "f.lizana", "c.espinosa", "n.arango", "j.fideney"]
    for name in names:
        user = User(username=name, email=f"{name.lower()}@example.com", password="12345")
        db.session.add(user)
    db.session.commit()
    print("Usuarios creados.")








flask shell
from project.models import db, User
user = User(username='atstatus', email='jchandia@atentus.com')
user.set_password('at2025status')
db.session.add(user)
db.session.commit()




users = User.query.all()
for user in users:
    user.set_password('at2025status')
    db.session.add(user)
db.session.commit()


new_user = User(username='jchandia', email='jchandia@atentus.com')
new_user.set_password('password123')
db.session.add(new_user)
db.session.commit()
print(f"Usuario '{new_user.username}' creado.")



new_user = User(username='L.ARMAS', email='larmas@atentus.com')
new_user.set_password('password123')
db.session.add(new_user)
db.session.commit()
print(f"Usuario '{new_user.username}' creado.")


new_user = User(username='N.ARANGO', email='narango@atentus.com')
new_user.set_password('password123')
db.session.add(new_user)
db.session.commit()
print(f"Usuario '{new_user.username}' creado.")

new_user = User(username='j.fideney', email='jfideney@atentus.com')
new_user.set_password('password123')
db.session.add(new_user)
db.session.commit()
print(f"Usuario '{new_user.username}' creado.")


new_user = User(username='C.ESPINOSA', email='cespinoza@atentus.com')
new_user.set_password('password123')
db.session.add(new_user)
db.session.commit()
print(f"Usuario '{new_user.username}' creado.")


new_user = User(username='f.lizana', email='flizanaa@atentus.com')
new_user.set_password('password123')
db.session.add(new_user)
db.session.commit()
print(f"Usuario '{new_user.username}' creado.")