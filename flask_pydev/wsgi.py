import Login
from Login import app


if __name__ == '__main__':
    import logging
    import logging.handlers
    handler = logging.handlers.RotatingFileHandler(
        'logs/error.log',
        backupCount=20,
        maxBytes=1024 * 1024)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    logging.getLogger('werkzeug').addHandler(handler)
    app.logger.setLevel(logging.WARNING) 
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0',port=5000, threaded=True)
