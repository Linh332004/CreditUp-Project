import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Academic Score System
gpa = ctrl.Antecedent(np.arange(0, 4.1, 0.1), 'gpa')
major_demand = ctrl.Antecedent(np.arange(0, 11, 1), 'major_demand')
academic_score = ctrl.Consequent(np.arange(0, 101, 1), 'academic_score')

# Membership functions for academic
gpa['low'] = fuzz.trimf(gpa.universe, [0, 0, 2.2])
gpa['medium'] = fuzz.trimf(gpa.universe, [2.0, 3.0, 3.6])
gpa['high'] = fuzz.trimf(gpa.universe, [3.3, 3.8, 4.0])

major_demand['low'] = fuzz.trimf(major_demand.universe, [0, 0, 5])
major_demand['medium'] = fuzz.trimf(major_demand.universe, [3, 6, 8])
major_demand['high'] = fuzz.trimf(major_demand.universe, [7, 9, 10])

academic_score['poor'] = fuzz.trimf(academic_score.universe, [0, 20, 40])
academic_score['average'] = fuzz.trimf(academic_score.universe, [35, 50, 65])
academic_score['good'] = fuzz.trimf(academic_score.universe, [60, 75, 85])
academic_score['excellent'] = fuzz.trimf(academic_score.universe, [80, 90, 100])

# Academic rules
academic_rules = [
    ctrl.Rule(gpa['high'] & major_demand['high'], academic_score['excellent']),
    ctrl.Rule(gpa['medium'] & major_demand['high'], academic_score['good']),
    ctrl.Rule(gpa['high'] & major_demand['medium'], academic_score['good']),
    ctrl.Rule(gpa['medium'] & major_demand['medium'], academic_score['average']),
    ctrl.Rule(gpa['low'] & major_demand['high'], academic_score['average']),
    ctrl.Rule(gpa['low'] | major_demand['low'], academic_score['poor'])
]

# Financial Score System
income = ctrl.Antecedent(np.arange(0, 30000001, 1000000), 'income')
spending = ctrl.Antecedent(np.arange(0, 30000001, 1000000), 'spending')
reserve = ctrl.Antecedent(np.arange(0, 2, 1), 'reserve')
in_debt = ctrl.Antecedent(np.arange(0, 2, 1), 'in_debt')
finance_score = ctrl.Consequent(np.arange(0, 101, 1), 'finance_score',defuzzify_method='centroid')

# Membership functions for financial
income['low'] = fuzz.trimf(income.universe, [0, 4000000, 8000000])
income['medium'] = fuzz.trimf(income.universe, [7000000, 12000000, 18000000])
income['high'] = fuzz.trimf(income.universe, [15000000, 22000000, 30000000])

spending['low'] = fuzz.trimf(spending.universe, [0, 4000000, 7000000])
spending['medium'] = fuzz.trimf(spending.universe, [6000000, 9000000, 13000000])
spending['high'] = fuzz.trimf(spending.universe, [12000000, 18000000, 25000000])

reserve['no'] = fuzz.trimf(reserve.universe, [0, 0, 1])
reserve['yes'] = fuzz.trimf(reserve.universe, [1, 1, 1])

in_debt['yes'] = fuzz.trimf(in_debt.universe, [1, 1, 1])
in_debt['no'] = fuzz.trimf(in_debt.universe, [0, 0, 1])

finance_score['low'] = fuzz.trimf(finance_score.universe, [0, 30, 50])
finance_score['medium'] = fuzz.trimf(finance_score.universe, [40, 60, 80])
finance_score['high'] = fuzz.trimf(finance_score.universe, [70, 85, 100])

# Financial rules
finance_rules = [
    ctrl.Rule(income['high'] & spending['low'] & reserve['yes'] & in_debt['no'], finance_score['high']),
    ctrl.Rule(income['high'] & spending['medium'] & reserve['yes'] & in_debt['no'], finance_score['high']),
    ctrl.Rule(income['medium'] & spending['medium'] & reserve['yes'] & in_debt['no'], finance_score['medium']),
    ctrl.Rule(income['low'] | spending['high'] | in_debt['yes'], finance_score['low']),
    ctrl.Rule(reserve['no'] & in_debt['yes'], finance_score['low']),
    ctrl.Rule(income['medium'] & reserve['yes'], finance_score['medium']),
    ctrl.Rule(spending['low'] & reserve['yes'], finance_score['high'])
]

# Personal Score System
discipline = ctrl.Antecedent(np.arange(1, 6, 1), 'discipline')
study_plan = ctrl.Antecedent(np.arange(0, 2, 1), 'study_plan')
break_rule = ctrl.Antecedent(np.arange(0, 2, 1), 'break_rule')
personal_score = ctrl.Consequent(np.arange(0, 101, 1), 'personal_score')

# Membership functions for personal

discipline['low'] = fuzz.trimf(discipline.universe, [1, 1, 2])
discipline['medium'] = fuzz.trimf(discipline.universe, [2.2, 3.2, 4.2])
discipline['high'] = fuzz.trimf(discipline.universe, [3.8, 4.5, 5])

study_plan['no'] = fuzz.trimf(study_plan.universe, [0, 0, 1])
study_plan['yes'] = fuzz.trimf(study_plan.universe, [1, 1, 1])

break_rule['yes'] = fuzz.trimf(break_rule.universe, [1, 1, 1])
break_rule['no'] = fuzz.trimf(break_rule.universe, [0, 0, 1])

personal_score['low'] = fuzz.trimf(personal_score.universe, [0, 30, 50])
personal_score['medium'] = fuzz.trimf(personal_score.universe, [40, 60, 80])
personal_score['high'] = fuzz.trimf(personal_score.universe, [70, 85, 100])

# Personal rules
personal_rules = [
    ctrl.Rule(break_rule['yes'], personal_score['low']),
    ctrl.Rule(break_rule['no'] & discipline['high'] & study_plan['yes'], personal_score['high']),
    ctrl.Rule(break_rule['no'] & discipline['medium'] & study_plan['yes'], personal_score['medium']),
    ctrl.Rule(break_rule['no'] & discipline['high'], personal_score['high']),
    ctrl.Rule(break_rule['no'] & discipline['medium'], personal_score['medium']),
    ctrl.Rule(discipline['low'], personal_score['low'])
]

# Online Score System
smartphone_time = ctrl.Antecedent(np.arange(0, 13, 1), 'smartphone_time')
read_news = ctrl.Antecedent(np.arange(0, 8, 1), 'read_news')
use_finance_app = ctrl.Antecedent(np.arange(0, 2, 1), 'use_finance_app')
study_finance = ctrl.Antecedent(np.arange(0, 2, 1), 'study_finance')
online_score = ctrl.Consequent(np.arange(0, 101, 1), 'online_score')

# Membership functions for online
smartphone_time['low'] = fuzz.trimf(smartphone_time.universe, [0, 1, 3])
smartphone_time['medium'] = fuzz.trimf(smartphone_time.universe, [2, 4, 6])
smartphone_time['high'] = fuzz.trimf(smartphone_time.universe, [5, 8, 12])

read_news['low'] = fuzz.trimf(read_news.universe, [0, 0, 2])
read_news['medium'] = fuzz.trimf(read_news.universe, [1, 3, 5])
read_news['high'] = fuzz.trimf(read_news.universe, [4, 6, 7])

use_finance_app['no'] = fuzz.trimf(use_finance_app.universe, [0, 0, 1])
use_finance_app['yes'] = fuzz.trimf(use_finance_app.universe, [1, 1, 1])

study_finance['no'] = fuzz.trimf(study_finance.universe, [0, 0, 1])
study_finance['yes'] = fuzz.trimf(study_finance.universe, [1, 1, 1])

online_score['low'] = fuzz.trimf(online_score.universe, [0, 30, 50])
online_score['medium'] = fuzz.trimf(online_score.universe, [40, 60, 80])
online_score['high'] = fuzz.trimf(online_score.universe, [70, 85, 100])

# Online rules
online_rules = [
    ctrl.Rule(smartphone_time['low'] & read_news['high'] & use_finance_app['yes'] & study_finance['yes'], online_score['high']),
    ctrl.Rule(smartphone_time['medium'] & read_news['medium'], online_score['medium']),
    ctrl.Rule(smartphone_time['high'] | read_news['low'], online_score['low']),
    ctrl.Rule(use_finance_app['no'] & study_finance['no'], online_score['low']),
    ctrl.Rule(read_news['medium'] & study_finance['yes'], online_score['medium']),
    ctrl.Rule(smartphone_time['low'] & study_finance['yes'], online_score['high'])
]

# Create control systems
academic_ctrl = ctrl.ControlSystem(academic_rules)
finance_ctrl = ctrl.ControlSystem(finance_rules)
personal_ctrl = ctrl.ControlSystem(personal_rules)
online_ctrl = ctrl.ControlSystem(online_rules)

def process_fuzzy_scores(user_data):
    """Process user data and return fuzzy logic scores."""
    try:
        academic_sim = ctrl.ControlSystemSimulation(academic_ctrl)
        try:
            academic_sim.input['gpa'] = float(user_data.get('gpa', 0))
            academic_sim.input['major_demand'] = float(user_data.get('major_demand', 0))
            academic_sim.compute()
            score_academic = academic_sim.output.get('academic_score', 60)
        except Exception as e:
            print("[ERROR] Academic fuzzy compute failed:", e)
            raise

        finance_sim = ctrl.ControlSystemSimulation(finance_ctrl)
        try:
            finance_sim.input['income'] = float(user_data.get('income', 0))
            finance_sim.input['spending'] = float(user_data.get('spending', 0))
            finance_sim.input['reserve'] = 1 if user_data.get('reserve', 'no').lower() == 'yes' else 0
            finance_sim.input['in_debt'] = 1 if user_data.get('existing_debt', 'no').lower() == 'yes' else 0
            finance_sim.compute()
            score_finance = finance_sim.output.get('finance_score', 60)
        except Exception as e:
            print("[ERROR] Finance fuzzy compute failed:", e)
            raise

        personal_sim = ctrl.ControlSystemSimulation(personal_ctrl)
        try:
            personal_sim.input['discipline'] = float(user_data.get('self_discipline', 0))
            personal_sim.input['study_plan'] = 1 if user_data.get('study_schedule', 'no').lower() == 'yes' else 0
            personal_sim.input['break_rule'] = 1 if user_data.get('academic_warnings', 'no').lower() == 'yes' else 0
            personal_sim.compute()
            score_personal = personal_sim.output.get('personal_score', 60)
        except Exception as e:
            print("[ERROR] Personal fuzzy compute failed:", e)
            raise

        online_sim = ctrl.ControlSystemSimulation(online_ctrl)
        try:
            online_sim.input['smartphone_time'] = float(user_data.get('smartphone', 0))
            online_sim.input['read_news'] = float(user_data.get('news', 0))
            online_sim.input['use_finance_app'] = 1 if user_data.get('finance_apps', 'no').lower() == 'yes' else 0
            online_sim.input['study_finance'] = 1 if user_data.get('finance_course', 'no').lower() == 'yes' else 0
            online_sim.compute()
            score_online = online_sim.output.get('online_score', 60)
        except Exception as e:
            print("[ERROR] Online fuzzy compute failed:", e)
            raise

        return {
            'academic': score_academic,
            'finance': score_finance,
            'personal': score_personal,
            'online': score_online
        }
    except Exception as e:
        print(f"Error in process_fuzzy_scores: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


def calculate_final_score(fuzzy_scores, ahp_score):
    """Calculate final score combining fuzzy logic and AHP results."""
    try:
        # Use AHP score as the base and adjust with fuzzy logic components
        final_score = (
            fuzzy_scores['academic'] * 0.1601 +
            fuzzy_scores['finance'] * 0.4673 +
            fuzzy_scores['personal'] * 0.2772 +
            fuzzy_scores['online'] * 0.0954
        )

        # Combine with AHP score (weighted average)
        return (final_score * 0.6 + ahp_score * 0.4)
    except Exception as e:
        print(f"Error in calculate_final_score: {str(e)}")
        raise


def credit_rate(final_score):
    """Convert numerical score to credit rating."""
    if final_score < 40:
        return 'Bad'
    elif final_score < 60:
        return 'Medium'
    elif final_score < 80:
        return 'Good'
    else:
        return 'Excellent'


def improvement_suggestions(academic_score, finance_score, personal_score, online_score):
    """
    Generate comprehensive improvement suggestions based on category scores.
    Returns a structured dictionary for better template rendering.

    Args:
        academic_score: Score for academic performance (0-100)
        finance_score: Score for financial management (0-100)
        personal_score: Score for personal discipline (0-100)
        online_score: Score for online behavior (0-100)

    Returns:
        dict: Dictionary containing categorized suggestions
    """
    suggestions = {
        'categories': []
    }

    # Academic suggestions
    if academic_score < 80:
        academic_suggestions = {
            'title': 'Academic Performance',
            'suggestions': [
                'Improve your GPA by focusing on your studies and seeking help when needed',
                'Consider choosing a more in-demand major or developing additional skills',
                'Attend all classes and participate actively in discussions',
                'Form study groups with classmates to enhance learning',
                'Meet with academic advisors regularly to track progress'
            ]
        }
        
        if academic_score < 60:
            academic_suggestions['suggestions'].extend([
                'Consider taking additional courses or workshops to strengthen weak areas',
                'Look for tutoring services or academic support programs',
                'Review and improve your study techniques and time management'
            ])
        
        suggestions['categories'].append(academic_suggestions)

    # Financial suggestions
    if finance_score < 80:
        finance_suggestions = {
            'title': 'Financial Management',
            'suggestions': [
                'Create a detailed budget and stick to it to better manage your spending',
                'Build an emergency fund by saving a portion of your income regularly',
                'Track all your expenses to identify areas where you can save',
                'Set up automatic savings transfers to ensure consistent saving'
            ]
        }
        
        if finance_score < 60:
            finance_suggestions['suggestions'].extend([
                'Consider taking a personal finance course to improve your financial literacy',
                'Review and reduce unnecessary subscriptions and expenses',
                'Create a debt repayment plan if you have any existing debts',
                'Look for ways to increase your income through part-time work or skills development'
            ])
        
        suggestions['categories'].append(finance_suggestions)

    # Personal suggestions
    if personal_score < 80:
        personal_suggestions = {
            'title': 'Personal Development',
            'suggestions': [
                'Improve your attendance and punctuality in classes',
                'Develop better study habits and create a consistent study schedule',
                'Set clear goals and track your progress regularly',
                'Practice time management techniques to balance study and personal life'
            ]
        }
        
        if personal_score < 60:
            personal_suggestions['suggestions'].extend([
                'Work on your self-discipline and time management skills',
                'Create a daily routine and stick to it',
                'Find a study buddy or accountability partner',
                'Take breaks and practice stress management techniques'
            ])
        
        suggestions['categories'].append(personal_suggestions)

    # Online suggestions
    if online_score < 80:
        online_suggestions = {
            'title': 'Digital Behavior',
            'suggestions': [
                'Reduce your smartphone usage and focus on more productive activities',
                'Stay informed about financial news and market trends',
                'Use productivity apps to manage your time and tasks',
                'Set specific times for checking social media and emails'
            ]
        }
        
        if online_score < 60:
            online_suggestions['suggestions'].extend([
                'Consider using financial management apps to track your expenses',
                'Take an online course about personal finance and investment',
                'Install website blockers during study hours',
                'Follow reputable financial education channels and resources'
            ])
        
        suggestions['categories'].append(online_suggestions)

    # If all scores are good, provide positive reinforcement
    if all(score >= 80 for score in [academic_score, finance_score, personal_score, online_score]):
        excellent_suggestions = {
            'title': 'Excellent Performance!',
            'suggestions': [
                'Keep maintaining your good habits and continue to improve',
                'Consider mentoring others who might need help',
                'Set new goals to further enhance your skills',
                'Share your successful strategies with peers'
            ]
        }
        suggestions['categories'].append(excellent_suggestions)

    return suggestions


def test_credit_score_calculation():
    """Test the credit score calculation with mock data."""
    print("Starting credit score calculation test...")

    # Mock user data
    mock_data = {
        # Academic
        'gpa': 3.5,
        'major_demand': 8,

        # Financial
        'income': 15_000_000,
        'spending': 7_000_000,
        'reserve': 'yes',
        'existing_debt': 'no',

        # Personal
        'self_discipline': 4,
        'study_schedule': 'yes',
        'academic_warnings': 'no',

        # Online
        'smartphone': 4,
        'news': 4,
        'finance_apps': 'yes',
        'finance_course': 'yes'
    }

    try:
        print("\nProcessing fuzzy scores...")
        # Process fuzzy scores
        fuzzy_scores = process_fuzzy_scores(mock_data)
        print("\nFuzzy Scores:")
        print(f"Academic: {fuzzy_scores['academic']:.2f}")
        print(f"Finance: {fuzzy_scores['finance']:.2f}")
        print(f"Personal: {fuzzy_scores['personal']:.2f}")
        print(f"Online: {fuzzy_scores['online']:.2f}")

        print("\nCalculating final score...")
        # Calculate final score (using a mock AHP score of 75)
        final_score = calculate_final_score(fuzzy_scores, 75)
        print(f"Final Score: {final_score:.2f}")

        # Get credit rating
        rating = credit_rate(final_score)
        print(f"Credit Rating: {rating}")

        # Get improvement suggestions
        suggestions = improvement_suggestions(
            fuzzy_scores['academic'], fuzzy_scores['finance'], fuzzy_scores['personal'], fuzzy_scores['online'])
        print("\nImprovement Suggestions:")
        for category in suggestions['categories']:
            print(f"\n{category['title']}:")
            for suggestion in category['suggestions']:
                print(f"- {suggestion}")

    except Exception as e:
        print(f"Error during testing: {str(e)}")
        import traceback
        print("\nDetailed error:")
        print(traceback.format_exc())


if __name__ == "__main__":
    print("Running credit score test...")
    test_credit_score_calculation()
    print("\nTest completed.")