from random import shuffle
from collections import defaultdict

from flask import render_template, redirect, url_for, jsonify, request, session
from flask_login import logout_user, login_required, current_user

import app.constants as constants
from app.user import user

from .forms import SettingsForm


def render_details(title: str, data_dict: defaultdict(float)):
    labels = []
    data = []
    for key, value in data_dict.items():
        labels.append(key)
        data.append(value)

    colors = list(constants.AVAILIBLE_CHART_COLORS)
    shuffle(colors)
    return render_template('user/details.html', title=title, labels=labels, data=data,
                           colors=colors[:len(data)])


def get_runtime_settings():
    rsettings = current_user.settings
    if session.get('currency'):
        currency = session['currency']
    else:
        currency = rsettings.currency

    locale = rsettings.locale
    if session.get('date_range'):
        start_date = rsettings.start_date
        end_date = rsettings.end_date
    else:
        start_date = rsettings.start_date
        end_date = rsettings.end_date

    return currency, locale, start_date, end_date


# routes
@user.route('/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html')


@user.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm(obj=current_user.settings)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.update_settings(current_user.settings)
            current_user.save()
            return render_template('user/settings.html', form=form)

    return render_template('user/settings.html', form=form)


@user.route('/runtime_settings/apply_currency', methods=['POST'])
@login_required
def runtime_settings():
    session['currency'] = request.form['currency']
    response = {}
    return jsonify(response), 200


@user.route('/logout')
@login_required
def logout():
    session.pop('currency', None)
    logout_user()
    return redirect(url_for('home.start'))
