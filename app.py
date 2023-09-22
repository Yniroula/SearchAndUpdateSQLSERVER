import secrets
from flask import Flask, redirect, request, render_template, flash, url_for
from config import cursor, conn, email_search_query, name_search_query, userid_search_query, update_query

app = Flask(__name__)
app.secret_key = secrets.token_hex(32) # Replace this with your actual secret key to run flash messages


@app.route('/')
def index():
    return render_template('index.html', user=None)

@app.route('/search', methods=['POST'])
def search():
    search_by = request.form['search_by']
    search_term = request.form['search_term']

    # Check if user_email is not empty and search
    if  search_by == "email":
        search_term = search_term.lower().strip()
        email_search_term = '%' + search_term + '%'
        cursor.execute(email_search_query, (email_search_term,))
        

    # Check if name is not empty and search
    elif  search_by == "name":
        search_term = search_term.strip()
        name_search_term  = '%' + search_term + '%'
        cursor.execute(name_search_query, (name_search_term,))
    
    results = cursor.fetchall()
    conn.commit()

    if len(results) > 0:
        # There are results, show the table
        return render_template("index.html", results=results)   
    else:
        # No results, show no results message
        return render_template("index.html", message="No results found.")
    

@app.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    if request.method == 'GET':
        # Fetch the record based on the user
        cursor.execute(userid_search_query, (user_id,))
        user = cursor.fetchone()

        if user:
            # Render the update template with the record details
            return render_template('update.html', user=user)
        else:
            # Handle the case when the record is not found
            flash('User not found.', 'error')
            return redirect('/')
    elif request.method == 'POST':
        try:
            # Handle the form submission for updating the record
            user_id = request.form['user_id']
            account_status = request.form['users_status']
            account_locked = request.form['account_locked']
            no_of_attempt = 0

            # Update the record in the database
            cursor.execute(update_query, (account_status, account_locked, no_of_attempt, user_id))
            conn.commit()

            # Flash update successful message and redirect back to the search page
            flash('Update successful.', 'success')
            return redirect(url_for('update', user_id=user_id))
        
        except Exception as e:
            # Flash exception message and redirect back to the search page
            flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('update', user_id=user_id))
        
    
if __name__ == '__main__':
    app.run(debug=True)