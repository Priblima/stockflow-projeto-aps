from app.core.security import hash_password
from app.database import Base, SessionLocal, engine
from app.models import Produto, User


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@stockflow.com").first()
        if admin is None:
            admin = User(
                nome="Administrador Demo",
                email="admin@stockflow.com",
                senha_hash=hash_password("admin123"),
                perfil="admin",
                ativo=True,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)

        produtos_demo = [
            {"nome": "Teclado Mecânico", "categoria": "Periféricos", "quantidade": 12, "peso": 0.85, "preco": 199.90},
            {"nome": "Mouse Sem Fio", "categoria": "Periféricos", "quantidade": 4, "peso": 0.20, "preco": 89.90},
            {"nome": "Monitor 24 polegadas", "categoria": "Monitores", "quantidade": 7, "peso": 3.80, "preco": 799.00},
        ]

        for item in produtos_demo:
            exists = db.query(Produto).filter(Produto.nome == item["nome"]).first()
            if exists is None:
                db.add(Produto(**item, criado_por_id=admin.id))

        db.commit()
        print("Seed executado com sucesso!")
        print("Usuário demo: admin@stockflow.com | Senha: admin123")
    finally:
        db.close()


if __name__ == "__main__":
    main()
