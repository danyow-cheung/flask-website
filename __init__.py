from flask import Flask
from flask import render_template
import os
from . import sqlitedb
from . import user    
from . import score

def create_app():
    FlaskScore = Flask(__name__,template_folder="templates",static_url_path="",static_folder="")

    FlaskScore.config.from_mapping(
            SECRET_KEY='FlaskScore',
            SQLITEDB=os.path.join(FlaskScore.instance_path,'FlaskScore.sqlite')
            )
    
    
    sqlitedb.init_app(FlaskScore)
   
    FlaskScore.register_blueprint(user.bp)

  
    FlaskScore.register_blueprint(score.bp)
    FlaskScore.add_url_rule('/',endpoint='index')

  	


    return FlaskScore
    
    
create_app()
