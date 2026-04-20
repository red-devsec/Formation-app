from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Formation

main = Blueprint('main', __name__)


@main.route('/')
def index():
    total = Formation.query.count()
    categories = db.session.query(Formation.categorie, db.func.count(Formation.id))\
        .group_by(Formation.categorie).all()
    return render_template('index.html', total=total, categories=categories)


@main.route('/formations')
def formations():
    categorie = request.args.get('categorie', '')
    search    = request.args.get('search', '')

    query = Formation.query
    if categorie:
        query = query.filter_by(categorie=categorie)
    if search:
        query = query.filter(Formation.titre.ilike(f'%{search}%'))

    formations  = query.order_by(Formation.id).all()
    categories  = db.session.query(Formation.categorie).distinct().all()
    categories  = [c[0] for c in categories]
    return render_template('formations.html',
                           formations=formations,
                           categories=categories,
                           selected_cat=categorie,
                           search=search)


@main.route('/formations/add', methods=['GET', 'POST'])
def add_formation():
    if request.method == 'POST':
        f = Formation(
            titre       = request.form['titre'],
            description = request.form['description'],
            duree       = request.form['duree'],
            niveau      = request.form['niveau'],
            categorie   = request.form['categorie'],
        )
        db.session.add(f)
        db.session.commit()
        flash('Formation ajoutée avec succès !', 'success')
        return redirect(url_for('main.formations'))
    return render_template('add_formation.html')


@main.route('/formations/delete/<int:id>', methods=['POST'])
def delete_formation(id):
    f = Formation.query.get_or_404(id)
    db.session.delete(f)
    db.session.commit()
    flash(f'Formation "{f.titre}" supprimée.', 'info')
    return redirect(url_for('main.formations'))


# ── API JSON (pour tester la DB via curl / Postman) ──────────────────────────

@main.route('/api/formations')
def api_formations():
    formations = Formation.query.all()
    return jsonify([f.to_dict() for f in formations])


@main.route('/api/formations/<int:id>')
def api_formation(id):
    f = Formation.query.get_or_404(id)
    return jsonify(f.to_dict())


@main.route('/health')
def health():
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({'status': 'ok', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'database': str(e)}), 500
