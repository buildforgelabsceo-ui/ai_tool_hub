from flask import Flask
from .models import db
from .config import config

def create_app(config_name='default'):
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .routes.main import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        _seed_if_empty()

    return app

def _seed_if_empty():
    from .models.tool import Tool
    if Tool.query.count() == 0:
        from .data.seed import SEED_TOOLS
        for t in SEED_TOOLS:
            tool = Tool(**t)
            db.session.add(tool)
        db.session.commit()
        print(f"Seeded {len(SEED_TOOLS)} tools.")
