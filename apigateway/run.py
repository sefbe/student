from app import create_app
from app.routes import app_bp

app = create_app()
##app.register_blueprint(app_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

