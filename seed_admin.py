from Core.database import SessionLocal
from Core.security import hash_password
from Models.User import User

def create_admin():
    db = SessionLocal()

    try:
        print("START SEED")

        admin = db.query(User).filter(User.username == "admin").first()

        if admin:
            print("Admin already exists")
            return

        new_admin = User(
            username="admin",
            email="admin@gmail.com",
            password=hash_password("123456"),  # 👈 dùng hàm của bạn
            role="ADMIN"
        )

        db.add(new_admin)
        db.commit()

        print("Admin created!")

    except Exception as e:
        db.rollback()
        print("ERROR:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()