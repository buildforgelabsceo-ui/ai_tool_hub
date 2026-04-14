from flask import Blueprint, render_template, request, jsonify, abort
from ..models.tool import Tool
from ..models import db
from ..data.seed import CATEGORIES
import os
from flask import send_from_directory
main = Blueprint('main', __name__)
@main.route('/sitemap.xml')
def sitemap():
    static_path = os.path.join(os.getcwd(), 'aitoolhub', 'static')
    return send_from_directory(static_path, 'sitemap.xml')
@main.route('/')
def index():
    featured_tools = Tool.query.filter_by(featured=True).limit(6).all()
    all_tools_count = Tool.query.count()
    return render_template('index.html',
        featured_tools=featured_tools,
        categories=CATEGORIES,
        all_tools_count=all_tools_count
    )

@main.route('/tools')
def tools():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search = request.args.get('q', '')
    pricing = request.args.get('pricing', '')

    query = Tool.query

    if category:
        query = query.filter(Tool.category == category)
    if pricing:
        query = query.filter(Tool.pricing == pricing)
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            db.or_(
                Tool.name.ilike(search_term),
                Tool.description.ilike(search_term),
                Tool.tags.ilike(search_term),
                Tool.category.ilike(search_term)
            )
        )

    tools = query.order_by(Tool.featured.desc(), Tool.date_added.desc()).paginate(
        page=page, per_page=12, error_out=False
    )

    return render_template('tools.html',
        tools=tools,
        categories=CATEGORIES,
        current_category=category,
        current_search=search,
        current_pricing=pricing
    )

@main.route('/tools/<slug>')
def tool_detail(slug):
    tool = Tool.query.filter_by(slug=slug).first_or_404()
    related_tools = Tool.query.filter(
        Tool.category == tool.category,
        Tool.id != tool.id
    ).limit(4).all()
    return render_template('tool_detail.html', tool=tool, related_tools=related_tools, categories=CATEGORIES)

@main.route('/categories')
def categories():
    cats_with_counts = []
    for cat in CATEGORIES:
        count = Tool.query.filter_by(category=cat['name']).count()
        cats_with_counts.append({**cat, 'count': count})
    return render_template('categories.html', categories=cats_with_counts)

@main.route('/categories/<category_name>')
def category_detail(category_name):
    decoded = category_name.replace('-', ' ')
    # Find matching category
    matched_cat = None
    for cat in CATEGORIES:
        if cat['name'].lower().replace(' ', '-') == category_name.lower():
            matched_cat = cat
            decoded = cat['name']
            break

    tools = Tool.query.filter_by(category=decoded).order_by(Tool.featured.desc()).all()
    return render_template('tools.html',
        tools_list=tools,
        categories=CATEGORIES,
        current_category=decoded,
        current_search='',
        current_pricing='',
        page_title=f'{decoded}',
        matched_cat=matched_cat
    )

@main.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        from slugify import slugify
        name = request.form.get('name', '').strip()
        website_url = request.form.get('website_url', '').strip()
        description = request.form.get('description', '').strip()
        short_description = request.form.get('short_description', '').strip()
        category = request.form.get('category', '').strip()
#         logo_url = request.form.get('logo_url', '').strip()
        pricing = request.form.get('pricing', 'Freemium').strip()
        tags = request.form.get('tags', '').strip()

        errors = []
        if not name: errors.append('Tool name is required.')
        if not website_url: errors.append('Website URL is required.')
        if not description: errors.append('Description is required.')
        if not category: errors.append('Category is required.')

        if not errors:
            slug = slugify(name)
            # Make slug unique
            base_slug = slug
            counter = 1
            while Tool.query.filter_by(slug=slug).first():
                slug = f"{base_slug}-{counter}"
                counter += 1

            tool = Tool(
                name=name,
                slug=slug,
                description=description,
                short_description=short_description or description[:200],
                website_url=website_url,
                category=category,
#                 logo_url=logo_url,
                pricing=pricing,
                tags=tags,
                featured=False
            )
            db.session.add(tool)
            db.session.commit()
            return render_template('submit.html', categories=CATEGORIES, success=True, tool=tool)

        return render_template('submit.html', categories=CATEGORIES, errors=errors,
                               form_data=request.form)

    return render_template('submit.html', categories=CATEGORIES)

# API endpoints
@main.route('/api/search')
def api_search():
    q = request.args.get('q', '')
    if not q or len(q) < 2:
        return jsonify([])
    search_term = f'%{q}%'
    tools = Tool.query.filter(
        db.or_(
            Tool.name.ilike(search_term),
            Tool.category.ilike(search_term),
            Tool.tags.ilike(search_term)
        )
    ).limit(8).all()
    return jsonify([{
        'name': t.name,
        'slug': t.slug,
        'category': t.category,
#         'logo_url': t.logo_url,
        'short_description': t.short_description
    } for t in tools])

@main.errorhandler(404)
def not_found(e):
    return render_template('404.html', categories=CATEGORIES), 404
