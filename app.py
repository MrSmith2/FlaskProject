from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    specs_short = db.Column(db.String(300), nullable=False)
    specs = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/products')
def products():
    articles = Article.query.order_by(Article.price.desc()).all()
    return render_template('products.html', articles=articles)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        text = request.form['text']
        specs = request.form['specs']
        specs_short = request.form['specs_short']
        article = Article(title=title, price=price, text=text, specs=specs, specs_short=specs_short)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении товара произошла ошибка"
    else:
        return render_template('create.html')


@app.route('/products/<int:article_id>')
def article_get(article_id):
    article = Article.query.get(article_id)
    return render_template('article_detailed.html', article=article)


@app.route('/products/<int:article_id>/delete')
def article_delete(article_id):
    article = Article.query.get_or_404(article_id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/products')
    except:
        return 'При удалении товара произошла ошибка'


@app.route('/products/<int:article_id>/edit', methods=['POST', 'GET'])
def article_edit(article_id):
    article = Article.query.get(article_id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.price = request.form['price']
        article.text = request.form['text']
        article.specs = request.form['specs']
        article.specs_short = request.form['specs_short']

        try:
            db.session.commit()
            return redirect('/products')
        except:
            return "При обновлении информации о товаре произошла ошибка"
    else:
        return render_template('article_edit.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)
