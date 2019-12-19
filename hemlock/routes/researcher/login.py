"""Login"""

from hemlock.routes.researcher.utils import *

from functools import wraps
from werkzeug.security import check_password_hash

@bp.route('/login', methods=['GET','POST'])
def login():
    """Login view function"""
    if request.method == 'GET':
        session.clear()
    login_p = login_page()
    if request.method == 'POST':
        login_p._record_response()
        password = login_p.questions[0].response
        password = password or ''
        session_store('password', password)
        if login_p._validate():
            return login_successful()
    return render(login_p)

LOGIN_BTN = """
<button id="forward-button" name="direction" type="submit" class="w-100 btn btn-outline-primary" style="float: right;" value="forward">
    Login
</button>
"""

@researcher_page('login')
def login_page():
    """Create login page"""
    login_p = Page(back=False)
    Validate(login_p, check_password)
    Free(login_p, text=PASSWORD_PROMPT)
    login_p.forward_button = LOGIN_BTN
    return login_p

def check_password(login_page):
    """Check the input password against researcher password"""
    if not password_correct():
        return PASSWORD_INCORRECT

def login_successful():
    """Process successful login

    Clear login page and redirect to requested page.
    """
    login_p = login_page()
    login_p.clear_errors()
    login_p.clear_responses()
    db.session.commit()
    requested = request.args.get('requested') or 'status'
    return redirect(url_for('hemlock.{}'.format(requested)))

def researcher_login_required(func):
    """Decorator requiring researcher login"""
    @wraps(func)
    def login_requirement():
        if not password_correct():
            login_page().error = LOGIN_REQUIRED
            db.session.commit()
            return redirect(url_for('hemlock.login', requested=func.__name__))
        return func()
    return login_requirement

def password_correct():
    """Indicate that the session password is correct"""
    if 'password' not in session:
        return False
    return check_password_hash(current_app.password_hash, session['password'])

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hemlock.login'))