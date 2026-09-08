"""
Web interface for StudyHard application
Built with Flask
"""

from flask import Flask, render_template, request, jsonify, session
import os
import json
from studyhard import StudyHard, Subject

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Store study instances per user
study_sessions = {}


def get_or_create_study(user_id: str) -> StudyHard:
    """Get or create a study session for user"""
    if user_id not in study_sessions:
        study_sessions[user_id] = StudyHard()
    return study_sessions[user_id]


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Get available subjects"""
    study = StudyHard()
    return jsonify({
        'subjects': study.get_available_subjects()
    })


@app.route('/api/select-subject', methods=['POST'])
def select_subject():
    """Select a subject"""
    data = request.json
    subject = data.get('subject')
    user_id = session.get('user_id', 'default')
    
    study = get_or_create_study(user_id)
    success = study.select_subject(subject)
    
    if success:
        session['subject'] = subject
        return jsonify({
            'success': True,
            'message': f'Предмет "{study.current_subject}" выбран'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Неверное название предмета'
        }), 400


@app.route('/api/load-topic', methods=['POST'])
def load_topic():
    """Load a topic and get explanation"""
    data = request.json
    topic = data.get('topic')
    user_id = session.get('user_id', 'default')
    
    study = get_or_create_study(user_id)
    success = study.load_topic(topic)
    
    if success:
        return jsonify({
            'success': True,
            'topic': study.current_topic,
            'explanation': study.explanation,
            'total_questions': len(study.questions)
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Ошибка при загрузке темы'
        }), 400


@app.route('/api/questions', methods=['GET'])
def get_questions():
    """Get all questions"""
    user_id = session.get('user_id', 'default')
    study = get_or_create_study(user_id)
    
    questions = []
    for i, q in enumerate(study.questions):
        questions.append({
            'id': i,
            'text': q.question_text,
            'options': q.options
        })
    
    return jsonify({'questions': questions})


@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    """Submit answer to a question"""
    data = request.json
    question_id = data.get('question_id')
    answer = data.get('answer')
    user_id = session.get('user_id', 'default')
    
    study = get_or_create_study(user_id)
    success = study.submit_answer(question_id, answer)
    
    if success:
        return jsonify({
            'success': True,
            'message': 'Ответ зарегистрирован'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Ошибка при регистрации ответа'
        }), 400


@app.route('/api/results', methods=['GET'])
def get_results():
    """Get quiz results"""
    user_id = session.get('user_id', 'default')
    study = get_or_create_study(user_id)
    
    results = study.get_results()
    
    if results['status'] == 'failed':
        # Return new questions if failed
        study.questions = results['new_questions']
        study.user_answers = {}
        study.error_count = 0
    
    return jsonify(results)


@app.route('/api/evaluate-essay', methods=['POST'])
def evaluate_essay():
    """Evaluate an essay"""
    data = request.json
    essay_text = data.get('essay')
    essay_topic = data.get('topic')
    user_id = session.get('user_id', 'default')
    
    study = get_or_create_study(user_id)
    feedback = study.evaluate_essay(essay_text, essay_topic)
    
    return jsonify({
        'success': True,
        'grammar_score': feedback.grammar_score,
        'vocabulary_score': feedback.vocabulary_score,
        'structure_score': feedback.structure_score,
        'goal_achievement_score': feedback.goal_achievement_score,
        'total_score': feedback.total_score,
        'comments': feedback.comments,
        'errors': feedback.errors
    })


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset study session"""
    user_id = session.get('user_id', 'default')
    
    if user_id in study_sessions:
        study_sessions[user_id].reset()
    
    return jsonify({'success': True, 'message': 'Сессия сброшена'})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
