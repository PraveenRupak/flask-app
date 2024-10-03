from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get form data from the request
            username = request.form['username']
            password = request.form['password']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']

            # Log form data to help with debugging
            app.logger.info(f"Received registration data: {username}, {email}")

            # Connect to the SQLite database (ensure path is correct)
            conn = sqlite3.connect('/home/ubuntu/mydatabase.db')
            c = conn.cursor()

            # Insert user data into the database
            c.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)",
                      (username, password, firstname, lastname, email))
            conn.commit()
            conn.close()

            # Log successful registration
            app.logger.info(f"User {username} registered successfully")

            # Return welcome message with user details
            return f"""
                <h1>Welcome {username}!</h1>
                <p>First Name: {firstname}</p>
                <p>Last Name: {lastname}</p>
                <p>Email: {email}</p>
            """

        except Exception as e:
            app.logger.error(f"Error during registration: {str(e)}")
            return f"An error occurred: {str(e)}"

    # If the request method is GET, just render the registration form
    return render_template('register.html')

# Main route for testing
@app.route('/')
def index():
    return "Welcome to the Flask App!"

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

