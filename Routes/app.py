from flask import Flask, request
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from Routes import Path
from Models.Function import Function
import os
import sys
import socketio
import eventlet


app = Flask(__name__)  # Flask app instance initiated
wsgi_app = app.wsgi_app

api = Api(app)  # Flask restful wraps Flask app around it.
app.debug=False
app.config['SECRET_KEY']='abc'
api.prefix='/api/v1'
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Cryptocurrency Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)

if __name__=='__main__':
    Path.initalize_routes(api)
    Path.initalize_swagger(docs)
    #Function.schedule()

    sio = socketio.Server()
    app = socketio.WSGIApp(sio, wsgi_app)
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app).run()


