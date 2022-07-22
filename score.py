from flask import(Blueprint,flash,g,redirect,render_template,request,url_for)
from werkzeug.exceptions import abort
from .sqlitedb import connect_db
from .user import login_required
import numpy as np
from wtforms import Form as form

bp = Blueprint('score',__name__)

@bp.route('/')
def index():
    db = connect_db()
    scores =db.execute('SELECT * FROM score ORDER BY id  DESC').fetchall()
    return render_template('index.html',scores=scores)

@bp.route('/create',methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        score = request.form['score']
        error = None

        if not score:
            error = "成绩不能为空"
            
        if error is not None:
            flash(error)

        else:
            db = connect_db()
            db.execute(
                'INSERT INTO score(score) VALUES(?)',[score]
            )
            db.commit()
            return redirect(url_for('score.index'))
            
    return render_template('create.html',form=form)
            
@bp.route('/analyse')
@login_required
def analyse():
    db=connect_db()
    scores = db.execute(
        'SELECT score FROM score'
    ).fetchall()
    allScore = np.array(scores)
    g.scoreCnt = len(allScore)
    g.maxScore=np.max(allScore)
    g.minScore=np.min(allScore)
    g.averageScore=np.around(np.mean(allScore),2)
    g.excellentCnt = len(list(filter(lambda i:i>=90,allScore)))
    g.failCnt = len(list(filter(lambda i:i<=59,allScore)))
    return render_template("analyse.html")
    
 
