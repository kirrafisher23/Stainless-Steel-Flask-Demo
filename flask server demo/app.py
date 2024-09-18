from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",    # Your actual MySQL username
    password="password",  # Your actual MySQL password
    database="stainless_steel_pipe"  # Your schema/database name
)

@app.route('/')
def index():
    cursor = db.cursor()

    # Query unique values for each attribute
    cursor.execute("SELECT DISTINCT din_num FROM tp304 UNION SELECT DISTINCT din_num FROM tp304l UNION SELECT DISTINCT din_num FROM tp316 UNION SELECT DISTINCT din_num FROM tp316l")
    din_numbers = cursor.fetchall()

    cursor.execute("SELECT DISTINCT nominal_pipe_size FROM tp304 UNION SELECT DISTINCT nominal_pipe_size FROM tp304l UNION SELECT DISTINCT nominal_pipe_size FROM tp316 UNION SELECT DISTINCT nominal_pipe_size FROM tp316l")
    nominal_pipe_sizes = cursor.fetchall()

    cursor.execute("SELECT DISTINCT mm_size FROM tp304 UNION SELECT DISTINCT mm_size FROM tp304l UNION SELECT DISTINCT mm_size FROM tp316 UNION SELECT DISTINCT mm_size FROM tp316l")
    mm_sizes = cursor.fetchall()

    cursor.execute("SELECT DISTINCT schedule_number FROM tp304 UNION SELECT DISTINCT schedule_number FROM tp304l UNION SELECT DISTINCT schedule_number FROM tp316 UNION SELECT DISTINCT schedule_number FROM tp316l")
    schedule_numbers = cursor.fetchall()

    cursor.execute("SELECT DISTINCT wall_thickness_mm FROM tp304 UNION SELECT DISTINCT wall_thickness_mm FROM tp304l UNION SELECT DISTINCT wall_thickness_mm FROM tp316 UNION SELECT DISTINCT wall_thickness_mm FROM tp316l")
    wall_thicknesses = cursor.fetchall()

    cursor.execute("SELECT DISTINCT design_strength FROM tp304 UNION SELECT DISTINCT design_strength FROM tp304l UNION SELECT DISTINCT design_strength FROM tp316 UNION SELECT DISTINCT design_strength FROM tp316l")
    design_strengths = cursor.fetchall()

    cursor.execute("SELECT DISTINCT mpa FROM tp304 UNION SELECT DISTINCT mpa FROM tp304l UNION SELECT DISTINCT mpa FROM tp316 UNION SELECT DISTINCT mpa FROM tp316l")
    mpa_values = cursor.fetchall()

    cursor.execute("SELECT DISTINCT psi FROM tp304 UNION SELECT DISTINCT psi FROM tp304l UNION SELECT DISTINCT psi FROM tp316 UNION SELECT DISTINCT psi FROM tp316l")
    psi_values = cursor.fetchall()

    # Pass the fetched data to the HTML template
    return render_template('index.html', 
                           din_numbers=din_numbers,
                           nominal_pipe_sizes=nominal_pipe_sizes,
                           mm_sizes=mm_sizes,
                           schedule_numbers=schedule_numbers,
                           wall_thicknesses=wall_thicknesses,
                           design_strengths=design_strengths,
                           mpa_values=mpa_values,
                           psi_values=psi_values)

@app.route('/query', methods=['POST'])
def query():
    # Get form data
    pipe_grade = request.form.get('pipe_grade')
    din_num = request.form.get('din_num', 'N/A')
    nominal_pipe_size = request.form.get('nominal_pipe_size', 'N/A')
    mm_size = request.form.get('mm_size', 'N/A')
    schedule_number = request.form.get('schedule_number', 'N/A')
    wall_thickness_mm = request.form.get('wall_thickness_mm', 'N/A')
    design_strength = request.form.get('design_strength', 'N/A')
    mpa = request.form.get('mpa', 'N/A')
    psi = request.form.get('psi', 'N/A')

    # Start building the dynamic query
    query = f"SELECT * FROM {pipe_grade} WHERE 1=1"

    # Only add conditions for fields that are not 'N/A' or empty
    if din_num and din_num != 'N/A':
        query += f" AND din_num = {din_num}"
    if nominal_pipe_size and nominal_pipe_size != 'N/A':
        query += f" AND nominal_pipe_size = {nominal_pipe_size}"
    if mm_size and mm_size != 'N/A':
        query += f" AND mm_size = {mm_size}"
    if schedule_number and schedule_number != 'N/A':
        query += f" AND schedule_number = '{schedule_number}'"
    if wall_thickness_mm and wall_thickness_mm != 'N/A':
        query += f" AND wall_thickness_mm = {wall_thickness_mm}"
    if design_strength and design_strength != 'N/A':
        query += f" AND design_strength = {design_strength}"
    if mpa and mpa != 'N/A':
        query += f" AND mpa = {mpa}"
    if psi and psi != 'N/A':
        query += f" AND psi = {psi}"

    # Debugging the final query output (optional, but useful for debugging)
    print("Final Query:", query)

    # Execute the query
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    # Error checking if no results are found
    if not result:
        return render_template('index.html', error="No results found for your search. Please try again with valid input.")

    # Pass the result to the results template
    return render_template('results.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
