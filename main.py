from flask import Flask, Blueprint, jsonify, render_template,request
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from topics import mockMethods, getTrendingCategories, mockEvents, parseEventsResponse, queryEvents, queryCategory, parseArticlesResponse
from flask_appconfig import AppConfig
from flask_bootstrap import Bootstrap
from nav import nav
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from wtforms import Form, BooleanField, StringField, validators, SelectField

class AttributesForm(Form):
    concept = StringField('Concept')
    category = StringField('Category')
    keywords = StringField('keywords')
    count = StringField('count')
    sorting = SelectField('sort by', choices=[('socialScore', 'Social score'), ('sourceAlexaCountryRank', 'Social Alexa Country Rank'),('date', 'Cosine similarity'),('sourceImportanceRank', 'Source importance rank'),('sourceAlexaGlobalRank', 'Source Alexa global rank')])

app = Flask(__name__)
AppConfig(app)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
nav.init_app(app)

# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
nav.register_element('frontend_top', Navbar(
    View('Home', '.topics'),
    Subgroup(
        'Docs',
        Link('Flask-Bootstrap', 'http://pythonhosted.org/Flask-Bootstrap'),
        Link('Flask-AppConfig', 'https://github.com/mbr/flask-appconfig'),
        Link('Flask-Debug', 'https://github.com/mbr/flask-debug'),
        Separator(),
        Text('Bootstrap'),
        Link('Getting started', 'http://getbootstrap.com/getting-started/'),
        Link('CSS', 'http://getbootstrap.com/css/'),
        Link('Components', 'http://getbootstrap.com/components/'),
        Link('Javascript', 'http://getbootstrap.com/javascript/'),
        Link('Customize', 'http://getbootstrap.com/customize/'), ),
    Text('Using Flask-Bootstrap {}'.format(FLASK_BOOTSTRAP_VERSION)), ))

#app.register_blueprint(frontend)

@app.route("/", methods=['GET', 'POST'])
def topics():
	form = AttributesForm(request.form)
	if request.method=='POST':
		concept = form.concept.data
		category = form.category.data
		keywords = form.keywords.data
		sort_by = form.sorting.data
		count = form.count.data
		response = parseEventsResponse(queryEvents(concept=concept, category=category, keywords=keywords.split(','), sortBy=sort_by))
		response_articles = parseArticlesResponse(queryCategory(concept=concept,category=category,keywords=keywords.split(','), sortBy=sort_by))
		return render_template('index.html', form=form,articles=response_articles, events=response)
	return render_template('index.html', form=form,articles=[], events=[])

@app.route("/trending")
def trending():
	result = getTrendingCategories()
	return render_template('trends.html', trends=result)

if __name__ == "__main__":
    app.run()