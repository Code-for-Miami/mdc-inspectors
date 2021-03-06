# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for, redirect, session, abort)
# from flask_login import login_user, login_required, logout_user

from inspectors.extensions import login_manager
from inspectors.registration.models import User
from inspectors.inspections.models import (
        Supervisor,
        Inspector,
        Inspection
        )
from inspectors.registration.forms import RegisterForm
from inspectors.utils import flash_errors
from inspectors.database import db

blueprint = Blueprint('registration', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = RegisterForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            flash("Great! You're now registered into our system.", 'success')
            new_user = User.create(permit_number=form.permit_number.data, email=form.email.data, phone_number=form.phone_number.data)
            redirect_url = request.args.get("next") or url_for("registration.complete", id=new_user.id)
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/users/<id>", methods=["GET", "POST"])
def complete(id):
    user = User.query.get(id)
    if user is None:
        abort(404)

    form = RegisterForm(request.form, obj=user)
    return render_template("public/settings.html", form=form)


@blueprint.route("/about/")
def about():
    return render_template("public/about.html")

