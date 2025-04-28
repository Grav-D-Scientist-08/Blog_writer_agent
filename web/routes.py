from flask import Flask, render_template, request, redirect, session, url_for
from auth_service.auth_service import sign_up, sign_in
from agents.topic_agent import get_trending_topics
from agents.blog_writer_agent import write_blog
from agents.blog_validator_agent import validate_blog
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Secret key from .env

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        interest = request.form['interest']
        msg = sign_up(name, email, password, interest)
        if "✅" in msg:
            return redirect(url_for('login'))
        return render_template('signup.html', error=msg)
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = sign_in(email, password)
        if user:
            session['user_id'] = user.id
            session['name'] = user.name
        
            session['interest'] = user.interest
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="❌ Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Fetch trending topics via the Topic Agent
    trending_topics = get_trending_topics()

    # Handle the topic selection and blog generation
    topic = None
    blog_content = None
    validation_msg = None

    if request.method == 'POST':
        topic = request.form.get('topic')

        if topic:
            # Generate blog using Blog Writer Agent
            blog_content = write_blog(topic)

            # Validate the generated blog using the Blog Validator Agent
            validation_msg = validate_blog(blog_content)

    return render_template('dashboard.html',
                           name=session['name'],
                           interest=session['interest'],
                           trending_topics=trending_topics,
                           selected_topic=topic,
                           blog_content=blog_content)
                        
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Test
if __name__ == "__main__":
    app.run(debug=True)