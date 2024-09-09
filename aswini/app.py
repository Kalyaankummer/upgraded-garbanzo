from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import random
import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from flask import jsonify

app = Flask(__name__, template_folder='templates')
app.static_folder = 'static'
app.secret_key = 'qdfhpzjsusbubitq'

# Configuration for email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'project554433@gmail.com'  # Replace with your Gmail email
app.config['MAIL_PASSWORD'] = "qdfhpzjsusbubitq"  # Replace with your Gmail password
mail = Mail(app)

def predict():
    # Generate a random prediction (e.g., 'High', 'Medium', 'Low')
    prediction_labels = ['High', 'Medium', 'Low']
    prediction = random.choice(prediction_labels)
    return prediction

def base_dir():
    return os.path.abspath(os.path.dirname(__file__))

class UserProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

@app.route('/')
def index():
    return render_template('index.html', title="Home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Hardcoded valid username and password
        valid_username = 'admin'
        valid_password = 'admin'
        
        username = request.form['username']
        password = request.form['password']
        if username == valid_username and password == valid_password:
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('index'))  # Redirect to the home page
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html', title="Login")
    else:
        return render_template('login.html', title="Login")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # Store user information (you may store it in a database instead)
        session['username'] = username
        session['email'] = email
        flash('Signup successful! Please login.', 'success')
        return redirect(url_for('signup_success'))  # Redirect to the signup success page
    
    return render_template('signup.html', title="Signup", form=form)

@app.route('/signup_success')
def signup_success():
    return render_template('signup_success.html', title="Signup Success")

@app.route('/home')
def home():
    if 'logged_in' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('logout_success'))

@app.route('/logout_success')
def logout_success():
    return render_template('logout.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(base_dir(), 'static', 'uploads', filename)
            file.save(file_path)
            flash('File uploaded successfully', 'success')
            return render_template('dashboard.html', uploaded_image=file_path)
        else:
            flash('Invalid file format. Allowed formats are png, jpg, jpeg, gif', 'error')
            return redirect(request.url)
    return render_template('dashboard.html')

@app.route('/segmentation', methods=['GET', 'POST'])
def segmentation():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(base_dir(), 'static', 'uploads', filename)
            file.save(file_path)
            flash('File uploaded successfully', 'success')
            
            # Read the content of the CSV file
            df = pd.read_csv(file_path)
            csv_content = df.to_html()
            
            return render_template('segmentation.html', success="File uploaded successfully", 
                                   uploaded_file=filename, csv_content=csv_content)
        else:
            flash('Invalid file format. Allowed formats are csv, txt, xls, xlsx', 'error')
            return redirect(request.url)
    
    return render_template('segmentation.html')

@app.route('/form', methods=['GET'])
def form():
    return render_template('form.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == "POST":
        email = request.form['email']
        subject = request.form['subject']
        msg = request.form['message']
        message = Message(subject, sender="project554433@gmail.com", recipients=[email])
        message.body = msg
        try:
            mail.send(message)
            success = "Message sent"
            return render_template("emailsuccess.html", success=success)
        except Exception as e:
            error = str(e)
            return render_template("emailsuccess.html", error=error)

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        # Get form data (assuming form field names are 'age', 'gender', 'item_purchased', etc.)
        age = request.form.get('age')
        gender = request.form.get('gender')
        item_purchased = request.form.get('item_purchased')
        category = request.form.get('category')
        color = request.form.get('color')
        season = request.form.get('season')
        review_rating = request.form.get('review_rating')
        subscription_status = request.form.get('subscription_status')
        shipping_type = request.form.get('shipping_type')
        discount_applied = request.form.get('discount_applied')
        promo_code_used = request.form.get('promo_code_used')
        previous_purchases = request.form.get('previous_purchases')
        payment_method = request.form.get('payment_method')
        frequency_of_purchases = request.form.get('frequency_of_purchases')
        
        # Perform prediction using the simple logic
        prediction = predict()
        
        # Return prediction as JSON response
        return jsonify({'prediction': prediction})
    elif request.method == 'GET':
        # Handle GET request (optional)
        return render_template('result.html')
    
# @app.route('/result', methods=['POST', 'GET'])
# def result():
#     if request.method == 'POST':
#         # Get form data
#         customer_id = request.form.get('customer_id')
#         age = request.form.get('age')
#         gender = request.form.get('gender')
#         item_purchased = request.form.get('item_purchased')
#         category = request.form.get('category')
#         color = request.form.get('color')
#         season = request.form.get('season')
#         review_rating = request.form.get('review_rating')
#         subscription_status = request.form.get('subscription_status')
#         shipping_type = request.form.get('shipping_type')
#         discount_applied = request.form.get('discount_applied')
#         promo_code_used = request.form.get('promo_code_used')
#         previous_purchases = request.form.get('previous_purchases')
#         payment_method = request.form.get('payment_method')
#         frequency_of_purchases = request.form.get('frequency_of_purchases')
        
#         # Perform prediction logic here
#         # This is a placeholder, replace it with your actual prediction logic
#         prediction = "Some prediction based on the form data"
        
#         # Pass form data and prediction to the template
#         return render_template('result.html', 
#                                customer_id=customer_id,
#                                age=age,
#                                gender=gender,
#                                item_purchased=item_purchased,
#                                category=category,
#                                color=color,
#                                season=season,
#                                review_rating=review_rating,
#                                subscription_status=subscription_status,
#                                shipping_type=shipping_type,
#                                discount_applied=discount_applied,
#                                promo_code_used=promo_code_used,
#                                previous_purchases=previous_purchases,
#                                payment_method=payment_method,
#                                frequency_of_purchases=frequency_of_purchases,
#                                prediction=prediction)
#     elif request.method == 'GET':
#         # Handle GET request (optional)
#         return render_template('result.html')

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    form = UserProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        session['user_data'] = {
            'username': form.username.data,
            'email': form.email.data,
            'phone_number': form.phone_number.data
        }
        return redirect(url_for('user_profile'))
    else:
        user_data = session.get('user_data', {})
        form.username.data = user_data.get('username', '')
        form.email.data = user_data.get('email', '')
        form.phone_number.data = user_data.get('phone_number', '')
        return render_template('user_profile.html', title="User Profile", form=form)


# Load dataset
df = pd.read_csv("shopping_behavior_updated (1).csv")

# Initialize Dash app
dash_app = dash.Dash(__name__, server=app, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define color options for bars
color_options = [
    {"label": "Blue", "value": "blue"},
    {"label": "Red", "value": "red"},
    {"label": "Green", "value": "green"},
    {"label": "Yellow", "value": "yellow"},
    {"label": "Orange", "value": "orange"},
    {"label": "Standard", "value": "standard"},  # Standard color option
    {"label": "Custom", "value": "custom"}  # Custom color option
]

# Define layout of the dashboard
dash_app.layout = html.Div([
    html.H1("Interactive Dashboard", style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    dbc.Row([
        dbc.Col([
            # Dropdown for selecting columns for Chart 1
            html.Label("Select Column for Chart 1:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id="column-dropdown-1",
                options=[{'label': col, 'value': col} for col in df.columns],
                value='Age',  # Default value
                style={'width': '100%'}
            ),
            # Dropdown for selecting chart type for Chart 1
            html.Label("Select Chart Type for Chart 1:", style={'fontWeight': 'bold', 'marginTop': '20px'}),
            dcc.Dropdown(
                id="chart-type-dropdown-1",
                options=[
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Pie Chart', 'value': 'pie'},
                    {'label': 'Histogram', 'value': 'histogram'},
                    {'label': 'Column Chart', 'value': 'column'}
                ],
                value='bar',  # Default value
                style={'width': '100%'}
            ),
            # Dropdown for selecting bar color for Chart 1
            html.Label("Select Bar Color for Chart 1:", style={'fontWeight': 'bold', 'marginTop': '20px'}),
            dcc.Dropdown(
                id="bar-color-dropdown-1",
                options=color_options,  # Use the color options defined above
                value='blue',  # Default value
                style={'width': '100%'}
            ),
            # Chart 1
            dcc.Graph(id='chart-1'),
        ], width=6),
        
        dbc.Col([
            # Dropdown for selecting columns for Chart 2
            html.Label("Select Column for Chart 2:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id="column-dropdown-2",
                options=[{'label': col, 'value': col} for col in df.columns],
                value='Purchase Amount (USD)',  # Default value
                style={'width': '100%'}
            ),
            # Dropdown for selecting chart type for Chart 2
            html.Label("Select Chart Type for Chart 2:", style={'fontWeight': 'bold', 'marginTop': '20px'}),
            dcc.Dropdown(
                id="chart-type-dropdown-2",
                options=[
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Pie Chart', 'value': 'pie'},
                    {'label': 'Histogram', 'value': 'histogram'},
                    {'label': 'Column Chart', 'value': 'column'}
                ],
                value='pie',  # Default value
                style={'width': '100%'}
            ),
            # Dropdown for selecting bar color for Chart 2
            html.Label("Select Bar Color for Chart 2:", style={'fontWeight': 'bold', 'marginTop': '20px'}),
            dcc.Dropdown(
                id="bar-color-dropdown-2",
                options=color_options,  # Use the color options defined above
                value='blue',  # Default value
                style={'width': '100%'}
            ),
            # Chart 2
            dcc.Graph(id='chart-2'),
        ], width=6),
    ], style={'margin': 'auto', 'maxWidth': '1200px'}),
], style={'padding': '20px'})

# Define callback to update all charts based on selected column, chart type, and bar color
@dash_app.callback(
    [Output('chart-1', 'figure'),
     Output('chart-2', 'figure')],
    [Input('column-dropdown-1', 'value'),
     Input('chart-type-dropdown-1', 'value'),
     Input('bar-color-dropdown-1', 'value'),
     Input('column-dropdown-2', 'value'),
     Input('chart-type-dropdown-2', 'value'),
     Input('bar-color-dropdown-2', 'value')]
)
def update_charts(column_1, chart_type_1, bar_color_1, column_2, chart_type_2, bar_color_2):
    fig1 = update_chart(column_1, chart_type_1, bar_color_1)
    fig2 = update_chart(column_2, chart_type_2, bar_color_2)
    return fig1, fig2

# Function to update chart based on selected column, chart type, and bar color
def update_chart(selected_column, chart_type, bar_color):
    if chart_type == 'bar':
        fig = px.bar(df, x='Customer ID', y=selected_column, title=f'{selected_column} Distribution')
        if bar_color != 'custom':
            fig.update_traces(marker_color=bar_color)
    elif chart_type == 'pie':
        fig = px.pie(df, names=selected_column, title=f'{selected_column} Distribution')
    elif chart_type == 'histogram':
        fig = px.histogram(df, x=selected_column, title=f'{selected_column} Distribution')
    else:  # column chart
        fig = px.scatter(df, x='Customer ID', y=selected_column, title=f'{selected_column} Distribution')
    return fig

@app.route('/interactivedashboard', methods=['GET', 'POST'])
def interactivedashboard():
    return dash_app.index()

if __name__ == '__main__':
    app.run(debug=True)  # Change port to 8051 (or any available port)
    dash_app.run_server(debug=True, port=8051) 
