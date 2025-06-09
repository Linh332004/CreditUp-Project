# file ahp.py - Improved Credit Scoring System

import numpy as np
import pandas as pd
import os
from typing import Dict, Any, Tuple
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==== Enhanced Normalization Functions ====

def normalize_gpa(gpa: float) -> float:
    """
    Normalize GPA with more granular scoring
    """
    gpa = max(0.0, min(float(gpa), 4.0))
    
    if gpa >= 3.8:
        return 9  
    elif gpa >= 3.5:
        return 8 
    elif gpa >= 3.0:
        return 7 
    elif gpa >= 2.7:
        return 5 
    elif gpa >= 2.3:
        return 3 
    elif gpa >= 2.0:
        return 2 
    else:
        return 1 

MAJOR_CATEGORIES = {
    "high_demand": {
        "majors": ["Computer Science", "Electrical Engineering", "Medicine", "Finance", "Data Science"],
        "job_prospect_score": 9,
        "salary_potential": 9,
        "market_stability": 8
    },
    "medium_high_demand": {
        "majors": ["Mechanical Engineering", "Civil Engineering", "Economics", "Accounting"],
        "job_prospect_score": 7,
        "salary_potential": 7,
        "market_stability": 7
    },
    "medium_demand": {
        "majors": ["Business Administration", "Marketing", "Law", "Psychology"],
        "job_prospect_score": 5,
        "salary_potential": 6,
        "market_stability": 5
    },
    "lower_demand": {
        "majors": ["Education", "Fine Arts", "History", "Philosophy", "Literature"],
        "job_prospect_score": 3,
        "salary_potential": 4,
        "market_stability": 4
    }
}

def normalize_major(major_name: str) -> float:
    """
    Enhanced major scoring based on market demand and prospects
    """
    major_name = str(major_name).strip()
    
    for category, info in MAJOR_CATEGORIES.items():
        if major_name in info["majors"]:
            score = (
                info["job_prospect_score"] * 0.5 +
                info["salary_potential"] * 0.3 +
                info["market_stability"] * 0.2
            )
            return score

    return 5.0

def calculate_savings_rate(savings: float, income: float) -> float:
    """
    Calculate savings rate with error handling
    """
    if income <= 0:
        return 0.0
    return max(0.0, min(1.0, savings / income))

def normalize_savings_rate(savings: float, income: float) -> float:
    """
    Enhanced savings rate normalization with Vietnamese context
    """
    rate = calculate_savings_rate(savings, income)
    
    if rate >= 0.30: 
        return 9
    elif rate >= 0.20: 
        return 8
    elif rate >= 0.15: 
        return 7
    elif rate >= 0.10: 
        return 5
    elif rate >= 0.05: 
        return 3
    elif rate > 0:   
        return 2
    else:        
        return 1

def calculate_spending_ratio(spending: float, income: float) -> float:
    """
    Calculate spending to income ratio
    """
    if income <= 0:
        return 1.0 
    return min(1.0, spending / income)

def normalize_spending_rate(spending: float, income: float) -> float:
    """
    Enhanced spending rate normalization (lower spending ratio = better score)
    """
    ratio = calculate_spending_ratio(spending, income)
    
    if ratio <= 0.50: 
        return 9
    elif ratio <= 0.60: 
        return 8
    elif ratio <= 0.70:
        return 7
    elif ratio <= 0.80: 
        return 5
    elif ratio <= 0.90:
        return 3
    elif ratio <= 0.95: 
        return 2
    else:           
        return 1

def normalize_discipline(score: float) -> float:
    """
    Linear normalization of discipline score (1-5 to 1-9)
    """
    score = max(1.0, min(5.0, float(score)))
    return 1 + (score - 1) * 2

def normalize_smartphone_usage(hours: float) -> float:
    """
    Enhanced smartphone usage normalization
    """
    hours = max(0.0, float(hours))
    
    if hours <= 2:  
        return 9
    elif hours <= 3: 
        return 8
    elif hours <= 4:   
        return 7
    elif hours <= 5:  
        return 5
    elif hours <= 7:  
        return 3
    elif hours <= 9:  
        return 2
    else:         
        return 1

def normalize_news_frequency(freq: float) -> float:
    """
    News reading frequency normalization (times per week)
    """
    freq = max(0.0, float(freq))
    
    if freq >= 5:     
        return 9
    elif freq >= 3:   
        return 8
    elif freq >= 2:   
        return 7
    elif freq >= 1:   
        return 5
    else:           
        return 3

def normalize_binary_criteria(answer: Any, positive_score: float = 9, negative_score: float = 3) -> float:
    """
    Enhanced binary criteria normalization with better type handling
    """
    if isinstance(answer, str):
        answer_lower = answer.strip().lower()
        return positive_score if answer_lower in ['yes', 'true', '1', 'có'] else negative_score
    elif isinstance(answer, bool):
        return positive_score if answer else negative_score
    elif isinstance(answer, (int, float)):
        return positive_score if answer > 0 else negative_score
    else:
        return negative_score

def calculate_debt_to_income_ratio(debt_amount: float, income: float) -> float:
    """
    Calculate debt-to-income ratio
    """
    if income <= 0:
        return float('inf') if debt_amount > 0 else 0
    return debt_amount / income

def normalize_debt_situation(existing_debt: str, debt_amount: float, income: float) -> float:
    """
    Enhanced debt situation normalization considering amount and ratio
    """
    has_debt = normalize_binary_criteria(existing_debt, 0, 1) == 0 
    
    if not has_debt:
        return 9 
    
    debt_ratio = calculate_debt_to_income_ratio(debt_amount, income)
    
    if debt_ratio <= 0.1:     
        return 7
    elif debt_ratio <= 0.2:  
        return 5
    elif debt_ratio <= 0.3:   
        return 3
    elif debt_ratio <= 0.5:
        return 2
    else:
        return 1

# ==== Enhanced Weight System ====

ENHANCED_WEIGHTS = {
    'GPA': 0.08,                   
    'Major': 0.12,                 
    'Savings Rate': 0.25,          
    'Spending Rate': 0.20,
    'Debt Situation': 0.15,        
    'Discipline': 0.10,       
    'Emergency Fund': 0.05,    
    'Smartphone Time': 0.02,      
    'Read News': 0.02,           
    'Schedule': 0.005,           
    'Violations': 0.005,           
    'Apps': 0.005,               
    'Course': 0.005               
}

def validate_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean user data
    """
    validated_data = {}

    numeric_fields = {
        'gpa': 0.0,
        'income': 0.0,
        'spending': 0.0,
        'savings': 0.0,
        'self_discipline': 3.0,
        'smartphone': 5.0,
        'news': 1.0,
        'debt_amount': 0.0
    }
    
    for field, default in numeric_fields.items():
        try:
            validated_data[field] = float(user_data.get(field, default))
        except (ValueError, TypeError):
            validated_data[field] = default
            logger.warning(f"Invalid value for {field}, using default: {default}")

    string_fields = ['major', 'emergency_fund', 'existing_debt', 'study_schedule', 
                    'academic_warnings', 'finance_apps', 'finance_course']
    
    for field in string_fields:
        validated_data[field] = str(user_data.get(field, '')).strip()

    if validated_data['savings'] == 0.0:
        calculated_savings = max(0.0, validated_data['income'] - validated_data['spending'])
        validated_data['savings'] = calculated_savings
    
    return validated_data

def normalize_inputs(user_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Enhanced input normalization with validation
    """
    clean_data = validate_user_data(user_data)
    
    normalized_scores = {}
    
    try:
        normalized_scores['GPA'] = normalize_gpa(clean_data['gpa'])
        normalized_scores['Major'] = normalize_major(clean_data['major'])

        normalized_scores['Savings Rate'] = normalize_savings_rate(
            clean_data['savings'], clean_data['income']
        )
        normalized_scores['Spending Rate'] = normalize_spending_rate(
            clean_data['spending'], clean_data['income']
        )
        normalized_scores['Debt Situation'] = normalize_debt_situation(
            clean_data['existing_debt'], clean_data['debt_amount'], clean_data['income']
        )

        normalized_scores['Discipline'] = normalize_discipline(clean_data['self_discipline'])
        normalized_scores['Emergency Fund'] = normalize_binary_criteria(clean_data['emergency_fund'])

        normalized_scores['Smartphone Time'] = normalize_smartphone_usage(clean_data['smartphone'])
        normalized_scores['Read News'] = normalize_news_frequency(clean_data['news'])

        normalized_scores['Schedule'] = normalize_binary_criteria(clean_data['study_schedule'])
        normalized_scores['Violations'] = normalize_binary_criteria(
            clean_data['academic_warnings'], 3, 9  # Invert: violations are bad
        )
        normalized_scores['Apps'] = normalize_binary_criteria(clean_data['finance_apps'])
        normalized_scores['Course'] = normalize_binary_criteria(clean_data['finance_course'])
        
        logger.info(f"Normalization completed. Scores: {normalized_scores}")
        return normalized_scores
        
    except Exception as e:
        logger.error(f"Error in normalize_inputs: {str(e)}")
        raise

def calculate_ahp_score(normalized_scores: Dict[str, float], weights: Dict[str, float]) -> float:
    """
    Enhanced AHP score calculation with validation
    """
    if not normalized_scores or not weights:
        raise ValueError("Empty normalized scores or weights")
    
    score = 0.0
    total_weight = 0.0
    
    for criterion, weight in weights.items():
        if criterion in normalized_scores:
            score += normalized_scores[criterion] * weight
            total_weight += weight
        else:
            logger.warning(f"Missing criterion in normalized scores: {criterion}")

    if total_weight > 0:
        final_score = (score / total_weight) * (100/9)
    else:
        final_score = 0.0
    
    logger.info(f"AHP Score calculated: {final_score:.2f} (total weight: {total_weight:.3f})")
    return min(100.0, max(0.0, final_score))

def get_credit_rating(score: float) -> Tuple[str, str]:
    """
    Enhanced credit rating with descriptions
    """
    if score >= 85:
        return "Excellent", "Exceptional creditworthiness with minimal risk"
    elif score >= 75:
        return "Very Good", "Strong creditworthiness with low risk"
    elif score >= 65:
        return "Good", "Satisfactory creditworthiness with moderate risk"
    elif score >= 50:
        return "Fair", "Acceptable creditworthiness with some risk"
    elif score >= 35:
        return "Poor", "Below average creditworthiness with high risk"
    else:
        return "Very Poor", "Poor creditworthiness with very high risk"

def generate_improvement_recommendations(normalized_scores: Dict[str, float]) -> Dict[str, list]:
    """
    Generate specific improvement recommendations based on scores
    """
    recommendations = {
        "high_priority": [],
        "medium_priority": [],
        "low_priority": []
    }

    if normalized_scores.get('Savings Rate', 9) < 4:
        recommendations["high_priority"].append(
            "Critical: Increase your savings rate. Aim to save at least 10-15% of your income."
        )
    
    if normalized_scores.get('Spending Rate', 9) < 4:
        recommendations["high_priority"].append(
            "Critical: Reduce your spending. Create a detailed budget and eliminate unnecessary expenses."
        )
    
    if normalized_scores.get('Debt Situation', 9) < 4:
        recommendations["high_priority"].append(
            "Critical: Address your debt situation. Create a debt repayment plan."
        )

    if 4 <= normalized_scores.get('GPA', 9) < 7:
        recommendations["medium_priority"].append(
            "Improve your GPA through better study habits and academic support."
        )
    
    if 4 <= normalized_scores.get('Discipline', 9) < 7:
        recommendations["medium_priority"].append(
            "Work on self-discipline through goal setting and habit formation."
        )
    
    if normalized_scores.get('Emergency Fund', 9) < 7:
        recommendations["medium_priority"].append(
            "Build an emergency fund covering 3-6 months of expenses."
        )

    if normalized_scores.get('Smartphone Time', 9) < 6:
        recommendations["low_priority"].append(
            "Reduce smartphone usage to improve focus and productivity."
        )
    
    if normalized_scores.get('Read News', 9) < 6:
        recommendations["low_priority"].append(
            "Stay informed about financial news and market trends."
        )
    
    return recommendations

def process_user_data_comprehensive(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Comprehensive user data processing with enhanced analytics
    """
    try:
        normalized_scores = normalize_inputs(user_data)

        ahp_score = calculate_ahp_score(normalized_scores, ENHANCED_WEIGHTS)

        rating, description = get_credit_rating(ahp_score)

        recommendations = generate_improvement_recommendations(normalized_scores)

        component_scores = {
            'academic': (normalized_scores['GPA'] + normalized_scores['Major']) / 2,
            'financial': (normalized_scores['Savings Rate'] + normalized_scores['Spending Rate'] + 
                         normalized_scores['Debt Situation']) / 3,
            'personal': (normalized_scores['Discipline'] + normalized_scores['Emergency Fund']) / 2,
            'digital': (normalized_scores['Smartphone Time'] + normalized_scores['Read News']) / 2
        }
        
        return {
            'final_score': ahp_score,
            'rating': rating,
            'rating_description': description,
            'normalized_scores': normalized_scores,
            'component_scores': component_scores,
            'recommendations': recommendations,
            'weights_used': ENHANCED_WEIGHTS
        }
        
    except Exception as e:
        logger.error(f"Error in comprehensive processing: {str(e)}")
        raise

global_weights = ENHANCED_WEIGHTS

def process_user_data_from_csv(csv_path: str) -> list:
    """
    Enhanced CSV processing with better error handling
    """
    try:
        if not os.path.exists(csv_path):
            logger.error(f"CSV file not found: {csv_path}")
            return []
        
        df = pd.read_csv(csv_path)
        results = []
        
        for index, row in df.iterrows():
            try:
                user_data = row.to_dict()
                result = process_user_data_comprehensive(user_data)
                result['row_index'] = index
                result['timestamp'] = user_data.get('submission_time', '')
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error processing row {index}: {str(e)}")
                continue
        
        logger.info(f"Successfully processed {len(results)} records from CSV")
        return results
        
    except Exception as e:
        logger.error(f"Error processing CSV file: {str(e)}")
        return []

def test_enhanced_system():
    """
    Test the enhanced credit scoring system
    """
    test_data = {
        'gpa': 3.5,
        'major': 'Computer Science',
        'income': 15000000,
        'spending': 10000000,
        'savings': 5000000,
        'self_discipline': 4,
        'smartphone': 3,
        'news': 3,
        'emergency_fund': 'yes',
        'existing_debt': 'no',
        'debt_amount': 0,
        'study_schedule': 'yes',
        'academic_warnings': 'no',
        'finance_apps': 'yes',
        'finance_course': 'yes'
    }
    
    print("Testing Enhanced Credit Scoring System")
    print("=" * 50)
    
    result = process_user_data_comprehensive(test_data)
    
    print(f"Final Score: {result['final_score']:.2f}")
    print(f"Rating: {result['rating']} - {result['rating_description']}")
    print("\nComponent Scores:")
    for component, score in result['component_scores'].items():
        print(f"  {component.title()}: {score:.2f}")
    
    print("\nRecommendations:")
    for priority, recs in result['recommendations'].items():
        if recs:
            print(f"  {priority.replace('_', ' ').title()}:")
            for rec in recs:
                print(f"    - {rec}")

if __name__ == "__main__":
    test_enhanced_system()