from Core.database import SessionLocal
from Core.security import hash_password
from Models.User import User

def create_admin():
    db = SessionLocal()

    # check đã có admin chưa
    admin = db.query(User).filter(User.role == "ADMIN").first()

    if admin:
        print("Admin already exists")
        return

    new_admin = User(
        username="admin",
        email="admin@gmail.com",
        password=hash_password("123456"),
        role="ADMIN"
    )

    db.add(new_admin)
    db.commit()
    db.close()

    print("Admin created!")

if __name__ == "__main__":
    create_admin()