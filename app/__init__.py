#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db import connect_db
from app.helpers.errors import register_error_handlers, not_found_error


# Create the app
app = Flask(__name__)

# Setup a session for messages, etc.
init_session(app)

# Handle 404 and 500 errors
register_error_handlers(app)


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
  with connect_db() as client:
        # Get all the things from the DB
        
        sql = "SELECT id, name, pirority FROM task ORDER BY name ASC"
        result = client.execute(sql)
        task = result.rows

        # And show them on the page
        return render_template("pages/home.jinja", task=task)

   


#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")


#-----------------------------------------------------------
# Tasks page route - Show all the things, and new thing form
#-----------------------------------------------------------
@app.get("/tasks/")
def show_all_things():
    with connect_db() as client:
        # Get all the things from the DB
        sql = "SELECT id, name, pirority FROM task ORDER BY name ASC"
        result = client.execute(sql)
        tasks = result.rows

        # And show them on the page
        return render_template("pages/tasks.jinja", tasks=tasks)


#-----------------------------------------------------------
# Thing page route - Show details of a single thing
#-----------------------------------------------------------
@app.get("/tasks/<int:id>")
def show_one_thing(id):
    with connect_db() as client:
        # Get the thing details from the DB
        sql = "SELECT id, name, pirority FROM task WHERE id=?"
        values = [id]
        result = client.execute(sql, values)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            thing = result.rows[0]
            return render_template("pages/thing.jinja", thing=thing)

        else:
            # No, so show error
            return not_found_error()


#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add_a_thing():
    # Get the data from the form
    name  = request.form.get("name")
    pirority = request.form.get("pirority")

    # Sanitise the inputs
    name = html.escape(name)
    pirority = html.escape(pirority)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO task (name, pirority) VALUES (?, ?)"
        values = [name, pirority ]
        client.execute(sql, values)

        # Go back to the home page
        flash(f"task'{name}' added", "success")
        return redirect("/tasks")


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_a_thing(id):
    with connect_db() as client:
        # Delete the thing from the DB
        sql = "DELETE FROM task WHERE id=?"
        values = [id]
        client.execute(sql, values)

        # Go back to the home page
        flash("Thing deleted", "warning")
        return redirect("/tasks")


