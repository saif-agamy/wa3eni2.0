from flask import Blueprint,render_template

school_b = Blueprint(
    "school",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/school/static"
)

@school_b.route("/school/")
def school():
    return render_template("school.html")

@school_b.route("/initiative/")
def initiative():
    return render_template("initiative.html")