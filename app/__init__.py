from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'postgresql://admin:admin123@db:5432/formations_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        from app.models import Formation
        if Formation.query.count() == 0:
            seed_data()

    return app


def seed_data():
    from app.models import Formation
    formations = [
        Formation(
            titre="Développement Web Full Stack",
            description="Maîtrisez HTML, CSS, JavaScript, React et Node.js pour créer des applications web modernes.",
            duree="6 mois",
            niveau="Débutant → Intermédiaire",
            categorie="Développement Web"
        ),
        Formation(
            titre="DevOps & Cloud Computing",
            description="Docker, Kubernetes, CI/CD, AWS et Azure. Automatisez et scalez vos infrastructures.",
            duree="4 mois",
            niveau="Intermédiaire",
            categorie="Infrastructure"
        ),
        Formation(
            titre="Intelligence Artificielle & Machine Learning",
            description="Python, TensorFlow, PyTorch. Construisez des modèles prédictifs et des réseaux de neurones.",
            duree="5 mois",
            niveau="Intermédiaire → Avancé",
            categorie="Data & IA"
        ),
        Formation(
            titre="Cybersécurité & Ethical Hacking",
            description="Pentest, analyse de vulnérabilités, cryptographie. Sécurisez les systèmes d'information.",
            duree="4 mois",
            niveau="Intermédiaire",
            categorie="Sécurité"
        ),
        Formation(
            titre="Data Engineering avec Python",
            description="Pandas, SQL, Spark, Airflow. Construisez des pipelines de données robustes et scalables.",
            duree="3 mois",
            niveau="Intermédiaire",
            categorie="Data & IA"
        ),
        Formation(
            titre="Développement Mobile Android & iOS",
            description="React Native et Flutter pour créer des applications mobiles cross-platform performantes.",
            duree="4 mois",
            niveau="Débutant → Intermédiaire",
            categorie="Développement Mobile"
        ),
    ]
    db.session.bulk_save_objects(formations)
    db.session.commit()
