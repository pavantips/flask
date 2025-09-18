from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# Create Flask app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hr_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Float)
    hire_date = db.Column(db.Date, default=date.today)
    
    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return '''
    <h1>HR Employee Management System</h1>
    <p><a href="/add-employee">Add New Employee</a></p>
    <p><a href="/employees">View All Employees</a></p>
    '''

@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee = Employee(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            department=request.form['department'],
            position=request.form['position'],
            salary=float(request.form['salary'])
        )
        db.session.add(employee)
        db.session.commit()
        return redirect(url_for('view_employees'))
    
    return '''
    <h2>Add New Employee</h2>
    <form method="POST">
        First Name: <input type="text" name="first_name" required><br><br>
        Last Name: <input type="text" name="last_name" required><br><br>
        Email: <input type="email" name="email" required><br><br>
        Department: <input type="text" name="department" required><br><br>
        Position: <input type="text" name="position" required><br><br>
        Salary: <input type="number" name="salary" step="0.01" required><br><br>
        <input type="submit" value="Add Employee">
    </form>
    <p><a href="/">Back to Home</a></p>
    '''
@app.route('/employees')
def view_employees():
    employees = Employee.query.all()
    output = '<h2>All Employees</h2>'
    
    if employees:
        output += '<table border="1" style="border-collapse: collapse; width: 100%;">'
        output += '<tr><th>ID</th><th>Name</th><th>Email</th><th>Department</th><th>Position</th><th>Salary</th><th>Hire Date</th></tr>'
        
        for employee in employees:
            output += f'''
            <tr>
                <td>{employee.id}</td>
                <td>{employee.first_name} {employee.last_name}</td>
                <td>{employee.email}</td>
                <td>{employee.department}</td>
                <td>{employee.position}</td>
                <td>${employee.salary:,.2f}</td>
                <td>{employee.hire_date}</td>
            </tr>
            '''
        output += '</table>'
    else:
        output += '<p>No employees found.</p>'
    
    output += '<p><a href="/">Back to Home</a></p>'
    output += '<p><a href="/add-employee">Add New Employee</a></p>'
    
    return output
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Different port so both apps can run