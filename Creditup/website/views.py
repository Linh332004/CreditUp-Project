from flask import Blueprint, render_template, request, redirect, flash, url_for
import os
import csv
from flask_login import login_required, current_user
from datetime import datetime
from .modules.ahp import normalize_inputs, calculate_ahp_score, global_weights
from .modules.fuzzyscoring import credit_rate, improvement_suggestions, process_fuzzy_scores, calculate_final_score

views = Blueprint('views', __name__)

# Mapping form data to expected field names
FIELD_MAPPING = {
    'saving': 'savings',
    'reserve_fund': 'emergency_fund',
    'debt': 'existing_debt',
    'debt_amount': 'debt_amount',
    'discipline': 'self_discipline',
    'schedule': 'study_schedule', 
    'violation': 'academic_warnings',
    'finance_app': 'finance_apps',
    'news_freq': 'news',
    'finance_course': 'finance_course'
}

# Major mapping to standardized format
MAJOR_MAPPING = {
    'computer_science': 'Computer Science',
    'engineering': 'Electrical Engineering',
    'data_science': 'Computer Science',
    'accounting': 'Accounting',
    'finance': 'Finance',
    'marketing': 'Marketing',
    'law': 'Law',
    'education': 'Education',
    'economics': 'Economics',
    'psychology': 'Psychology',
    'medicine': 'Medicine'
}

def convert_emergency_fund_to_binary(value):
    """Convert emergency fund source to yes/no"""
    return 'yes' if value and value != 'none' else 'no'

def convert_debt_to_binary(value):
    """Convert debt type to yes/no"""
    return 'yes' if value and value != 'none' else 'no'

@views.route('/')
@login_required
def root():
    return redirect(url_for('views.input_page'))

@views.route('/input', methods=['GET'])
@login_required
def input_page():
    return render_template("input_form.html", user=current_user)

@views.route('/result', methods=['POST'])
@login_required
def result():
    print(f"Processing form submission for user: {current_user.email}")
    
    if not current_user.is_authenticated or not current_user.is_active:
        flash('Please log in to submit the form.', category='error')
        return redirect(url_for('auth.login'))

    try:
        # Get form data
        form_data = request.form.to_dict()
        print(f"Original form data: {form_data}")
        
        # Convert and map form data
        processed_data = {}
        
        # Direct mappings
        for form_key, expected_key in FIELD_MAPPING.items():
            if form_key in form_data:
                processed_data[expected_key] = form_data[form_key]
        
        # Handle fields that don't need mapping
        direct_fields = ['gpa', 'major', 'income', 'spending', 'smartphone', 'app_type', 'finance_app_name']
        for field in direct_fields:
            if field in form_data:
                processed_data[field] = form_data[field]
        
        # Convert major to standardized format
        if 'major' in processed_data:
            processed_data['major'] = MAJOR_MAPPING.get(processed_data['major'], processed_data['major'])
        
        # Handle special conversions
        if 'reserve_fund' in form_data:
            processed_data['emergency_fund'] = convert_emergency_fund_to_binary(form_data['reserve_fund'])
        
        if 'debt' in form_data:
            processed_data['existing_debt'] = convert_debt_to_binary(form_data['debt'])
        
        # Convert numeric fields
        numeric_fields = ['gpa', 'income', 'spending', 'savings', 'self_discipline', 'smartphone', 'news']
        for field in numeric_fields:
            if field in processed_data:
                try:
                    processed_data[field] = float(processed_data[field])
                except (ValueError, TypeError):
                    processed_data[field] = 0.0
        
        # Calculate savings if not provided
        if 'savings' not in processed_data:
            income = processed_data.get('income', 0)
            spending = processed_data.get('spending', 0)
            processed_data['savings'] = max(0, income - spending)
        
        # Add user info and timestamp
        processed_data['user_email'] = current_user.email
        processed_data['user_name'] = current_user.first_name
        processed_data['submission_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"Processed data: {processed_data}")
        
        # Create user directory if it doesn't exist
        current_dir = os.path.dirname(os.path.abspath(__file__))
        user_dir = os.path.join(current_dir, 'user_data')
        os.makedirs(user_dir, exist_ok=True)
        
        # Create user-specific CSV file
        user_email_safe = current_user.email.replace('@', '_at_').replace('.', '_dot_')
        csv_path = os.path.join(user_dir, f'{user_email_safe}_data.csv')
        
        # Write to CSV
        file_exists = os.path.isfile(csv_path)
        with open(csv_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=processed_data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(processed_data)
        
        # Calculate scores
        print("Calculating AHP scores...")
        
        # Normalize inputs for AHP
        normalized_scores = normalize_inputs(processed_data)
        print(f"Normalized scores: {normalized_scores}")
        
        # Calculate AHP score
        ahp_score = calculate_ahp_score(normalized_scores, global_weights)
        print(f"AHP Score: {ahp_score}")
        
        # Calculate fuzzy scores
        print("Calculating fuzzy scores...")
        
        # Prepare data for fuzzy scoring (add required fields if missing)
        fuzzy_data = processed_data.copy()
        
        # Add default values for missing fuzzy fields
        if 'major_demand' not in fuzzy_data:
            # Map major to demand level (0-10 scale)
            major_demand_map = {
                'Computer Science': 9,
                'Electrical Engineering': 8,
                'Finance': 7,
                'Accounting': 6,
                'Economics': 7,
                'Medicine': 9,
                'Law': 6,
                'Marketing': 5,
                'Psychology': 4,
                'Education': 4
            }
            fuzzy_data['major_demand'] = major_demand_map.get(fuzzy_data.get('major', ''), 5)
        
        if 'attendance' not in fuzzy_data:
            fuzzy_data['attendance'] = 85  # Default attendance
        
        if 'reserve' not in fuzzy_data:
            fuzzy_data['reserve'] = fuzzy_data.get('emergency_fund', 'no')
        
        fuzzy_scores = process_fuzzy_scores(fuzzy_data)
        print(f"Fuzzy scores: {fuzzy_scores}")
        
        # Calculate final combined score
        final_score = calculate_final_score(fuzzy_scores, ahp_score)
        print(f"Final combined score: {final_score}")
        
        # Get credit rating and suggestions
        credit_rating = credit_rate(final_score)
        suggestions = improvement_suggestions(
            fuzzy_scores['academic'],
            fuzzy_scores['finance'], 
            fuzzy_scores['personal'],
            fuzzy_scores['online']
        )
        
        print(f"Credit rating: {credit_rating}")
        print(f"Rendering result template...")
        
        # Render result template
        return render_template('result.html',
                             user=current_user,
                             score=round(final_score, 2),
                             rating=credit_rating,
                             academic_score=round(fuzzy_scores['academic'], 2),
                             financial_score=round(fuzzy_scores['finance'], 2),
                             personal_score=round(fuzzy_scores['personal'], 2),
                             online_score=round(fuzzy_scores['online'], 2),
                             suggestions=suggestions)
        
    except Exception as e:
        print(f"Error in result processing: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        flash(f'Error processing your data: {str(e)}', category='error')
        return redirect(url_for('views.input_page'))