from sqlmodel import Session

from ai_template.models.database import Deployment, Model, Project
from ai_template.models.engine import engine


def seed_data():
    dummy_projects = [
        {"name": "AI Research", "description": "Machine learning research project"},
        {"name": "Web App", "description": "Full-stack web application"},
    ]

    dummy_models = [
        {
            "name": "GPT-2 Fine-tuned",
            "description": "Fine-tuned language model",
            "metrics": {"accuracy": 0.89, "loss": 0.11},
        },
        {
            "name": "Image Classifier",
            "description": "CNN for image classification",
            "metrics": {"accuracy": 0.95, "loss": 0.05},
        },
    ]

    dummy_deployments = [
        {"status": "deployed", "url": "https://api.example.com/v1"},
        {"status": "pending"},
    ]

    with Session(engine) as session:
        for p in dummy_projects:
            session.add(Project(**p))
        for m in dummy_models:
            session.add(Model(**m))
        for d in dummy_deployments:
            session.add(Deployment(**d))
        session.commit()


if __name__ == "__main__":
    seed_data()
