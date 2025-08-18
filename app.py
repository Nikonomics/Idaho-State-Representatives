#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from dotenv import load_dotenv
from scraper import IdahoLegislatureScraper
from analyzer import RepresentativeAnalyzer
from models import Representative, Chamber
from zip_mapping import get_districts_by_zip, is_idaho_zip
from sample_data import get_sample_data

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize tools
scraper = IdahoLegislatureScraper()
api_key = os.getenv('OPENAI_API_KEY')
analyzer = RepresentativeAnalyzer(api_key=api_key)

# Cache for legislative data
legislative_data = None

def get_legislative_data():
    global legislative_data
    if legislative_data is None:
        try:
            legislative_data = scraper.get_all_data()
            # Check if scraping returned valid data
            valid_data = (legislative_data['senators'] and 
                         len(legislative_data['senators']) > 10 and
                         isinstance(legislative_data['senators'][0], Representative))
            
            if not valid_data:
                print("Using sample data for testing (scraper data insufficient)")
                legislative_data = get_sample_data()
        except Exception as e:
            print(f"Error loading data, using sample data: {e}")
            legislative_data = get_sample_data()
    return legislative_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/zip/<zip_code>')
def zip_lookup(zip_code):
    """Handle ZIP code lookup with multi-district support"""
    if not is_idaho_zip(zip_code):
        return render_template('zip_error.html', zip_code=zip_code)
    
    districts = get_districts_by_zip(zip_code)
    
    if len(districts) == 1:
        # Single district - redirect to district page
        return redirect(url_for('district_lookup', district_num=districts[0], zip_code=zip_code))
    elif len(districts) > 1:
        # Multiple districts - show selection page
        return render_template('district_selection.html', zip_code=zip_code, districts=districts)
    else:
        return render_template('zip_error.html', zip_code=zip_code)

@app.route('/district/<int:district_num>')
def district_lookup(district_num):
    zip_code = request.args.get('zip_code')
    data = get_legislative_data()
    
    district_reps = {
        'senate': None,
        'house': []
    }
    
    # Find Senate representative
    for senator in data['senators']:
        if senator.district == district_num:
            district_reps['senate'] = senator
            break
    
    # Find House representatives
    for rep in data['representatives']:
        if rep.district == district_num:
            district_reps['house'].append(rep)
    
    return render_template('district.html', district=district_num, reps=district_reps, zip_code=zip_code)

@app.route('/problem', methods=['GET', 'POST'])
def problem_analysis():
    if request.method == 'POST':
        problem_description = request.form.get('problem_description')
        if problem_description:
            data = get_legislative_data()
            all_reps = data['senators'] + data['representatives']
            analysis = analyzer.analyze_problem(problem_description, all_reps)
            return render_template('problem_results.html', analysis=analysis)
    
    return render_template('problem.html')

@app.route('/analyze', methods=['GET', 'POST'])
def representative_analysis():
    if request.method == 'POST':
        rep_name = request.form.get('representative_name')
        if rep_name:
            data = get_legislative_data()
            all_reps = data['senators'] + data['representatives']
            
            # Find the representative
            target_rep = None
            for rep in all_reps:
                if rep_name.lower() in rep.name.lower():
                    target_rep = rep
                    break
            
            if target_rep:
                analysis = analyzer.analyze_representative(target_rep)
                return render_template('rep_analysis.html', analysis=analysis)
            else:
                return render_template('analyze.html', error=f"Representative '{rep_name}' not found.")
    
    return render_template('analyze.html')

@app.route('/committees')
def committees():
    data = get_legislative_data()
    return render_template('committees.html', committees=data['committees'])

@app.route('/api/representatives')
def api_representatives():
    data = get_legislative_data()
    all_reps = data['senators'] + data['representatives']
    return jsonify([{
        'name': rep.name,
        'district': rep.district,
        'chamber': rep.chamber.value,
        'party': rep.party.value
    } for rep in all_reps])

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    data = get_legislative_data()
    all_reps = data['senators'] + data['representatives']
    
    matches = []
    for rep in all_reps:
        if query in rep.name.lower():
            matches.append({
                'name': rep.name,
                'district': rep.district,
                'chamber': rep.chamber.value,
                'party': rep.party.value
            })
    
    return jsonify(matches[:10])  # Limit to 10 results

if __name__ == '__main__':
    app.run(debug=True, port=5000)