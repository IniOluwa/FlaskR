# Import Dependencies
import functools
from Flask import Blueprint, flash, g, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


# Create Blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register Route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Check Method
    if request.method == 'POST':
        # Get Values
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        # Handle
        if not username:
            error = 'Username is Required.'
            
        elif not password:
            error = 'Password is Required.'
            
        # Create User
        if error is None:
            try:
                db.execute("INSERT INTO user (username, password) VALUES (?, ?)",
                            (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f'{username} is already a registered user.'
        else:
            return redirect(url_for('auth.login'))
            
        # Show Error
        flash(error)
        
    # Return Page Otherwise
    return render_template('auth/register.html')

# Login Route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Check Method
    if request.method == 'POST':
        # Get Values
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        
        # Check User
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            
        # Login User
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
            
        # Show Error
        flash(error)
        
    # Return Page Otherwise
    return render_template('auth/login')

# Before Request
@bp.before_app_request
def load_logged_in_user():
    # Get User
    user_id = session['user_id']
    
    # Check User
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

# Logout Route
@bp.route('/logout')
def logout():
    # Clear Session
    session.clear()
    
    # Return to Index
    return redirect(url_for('index'))
    
# Login Required Decorator Function
def login_required():
    # Wrap View
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # Check & Handle User Availability
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        # Return View
        return view(**kwargs)
    
    # Return Wrapped View Function
    return wrapped_view
