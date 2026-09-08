"""
StudyHard - Interactive Learning Application
Main application module
"""

import json
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class Subject(Enum):
    """Supported subjects"""
    ENGLISH = "Английский"
    MATHEMATICS = "Математика"
    RUSSIAN = "Русский"
    CHEMISTRY = "Химия"
    BIOLOGY = "Биология"
    PHYSICS = "Физика"
    HISTORY = "История"
    LITERATURE = "Литература"


@dataclass
class Question:
    """Question data structure"""
    question_text: str
    correct_answer: str
    options: List[str]
    topic: str
    subject: str


@dataclass
class EssayFeedback:
    """Essay evaluation feedback"""
    grammar_score: int  # 0-10
    vocabulary_score: int  # 0-10
    structure_score: int  # 0-10
    goal_achievement_score: int  # 0-10
    total_score: int  # 0-10
    comments: str
    errors: List[str]


class StudyHard:
    """Main application class"""
    
    def __init__(self):
        self.current_subject: str = None
        self.current_topic: str = None
        self.explanation: str = None
        self.questions: List[Question] = []
        self.user_answers: Dict[int, str] = {}
        self.error_count: int = 0
        self.passed: bool = False
        
    def select_subject(self, subject: str) -> bool:
        """Select a subject for studying"""
        try:
            self.current_subject = Subject[subject.upper()].value
            return True
        except KeyError:
            return False
    
    def load_topic(self, topic: str) -> bool:
        """Load topic and generate explanation"""
        if not self.current_subject:
            return False
        
        self.current_topic = topic
        self.explanation = self._generate_explanation(topic, self.current_subject)
        self.questions = self._generate_questions(topic, self.current_subject)
        self.user_answers = {}
        self.error_count = 0
        self.passed = False
        
        return True
    
    def _generate_explanation(self, topic: str, subject: str) -> str:
        """Generate explanation for the topic"""
        # This would be connected to an AI service in production
        explanation = f"""
        Тема: {topic}
        Предмет: {subject}
        
        Подробное объяснение темы "{topic}" в области {subject}:
        
        1. Основные концепции
        2. Ключевые определения
        3. Примеры и приложения
        4. Практическое применение
        5. Связь с другими темами
        
        [Здесь будет детальное объяснение из AI]
        """
        return explanation
    
    def _generate_questions(self, topic: str, subject: str) -> List[Question]:
        """Generate 10 questions for the topic"""
        # This would be connected to an AI service in production
        questions = []
        for i in range(1, 11):
            question = Question(
                question_text=f"Вопрос {i}: {topic}",
                correct_answer="A",
                options=["A) Вариант 1", "B) Вариант 2", "C) Вариант 3", "D) Вариант 4"],
                topic=topic,
                subject=subject
            )
            questions.append(question)
        return questions
    
    def submit_answer(self, question_index: int, answer: str) -> bool:
        """Submit answer to a question"""
        if question_index >= len(self.questions):
            return False
        
        self.user_answers[question_index] = answer
        
        if answer != self.questions[question_index].correct_answer:
            self.error_count += 1
        
        return True
    
    def get_results(self) -> Dict:
        """Get quiz results"""
        if len(self.user_answers) < len(self.questions):
            return {"status": "incomplete", "message": "Не все вопросы ответены"}
        
        if self.error_count >= 2:
            return {
                "status": "failed",
                "error_count": self.error_count,
                "message": f"Вы допустили {self.error_count} ошибок. Вопросы не засчитаны. Получите новый набор вопросов.",
                "new_questions": self._generate_questions(self.current_topic, self.current_subject)
            }
        
        self.passed = True
        correct_answers = len(self.questions) - self.error_count
        percentage = (correct_answers / len(self.questions)) * 100
        
        return {
            "status": "passed",
            "correct_answers": correct_answers,
            "total_questions": len(self.questions),
            "percentage": percentage,
            "error_count": self.error_count,
            "message": f"Поздравляем! Вы ответили на {correct_answers} из {len(self.questions)} вопросов ({percentage:.1f}%)"
        }
    
    def evaluate_essay(self, essay_text: str, essay_topic: str = None) -> EssayFeedback:
        """Evaluate essay based on criteria"""
        feedback = EssayFeedback(
            grammar_score=0,
            vocabulary_score=0,
            structure_score=0,
            goal_achievement_score=0,
            total_score=0,
            comments="",
            errors=[]
        )
        
        # Grammar evaluation
        feedback.grammar_score = self._evaluate_grammar(essay_text)
        
        # Vocabulary evaluation (B1+ level)
        feedback.vocabulary_score = self._evaluate_vocabulary(essay_text)
        
        # Structure evaluation
        feedback.structure_score = self._evaluate_structure(essay_text)
        
        # Goal achievement evaluation
        feedback.goal_achievement_score = self._evaluate_goal_achievement(essay_text, essay_topic)
        
        # Calculate total score
        feedback.total_score = (
            feedback.grammar_score +
            feedback.vocabulary_score +
            feedback.structure_score +
            feedback.goal_achievement_score
        ) // 4
        
        feedback.comments = self._generate_essay_feedback(feedback)
        
        return feedback
    
    def _evaluate_grammar(self, essay_text: str) -> int:
        """Evaluate grammatical correctness (0-10)"""
        # Placeholder for grammar checking
        # In production, would use specialized library like LanguageTool
        score = 8  # Default score
        
        # Simple checks
        errors = []
        if essay_text.count('.') < 3:
            errors.append("Недостаточно предложений")
            score -= 2
        
        if len(essay_text) < 100:
            errors.append("Текст слишком короткий")
            score -= 2
        
        return max(0, score)
    
    def _evaluate_vocabulary(self, essay_text: str) -> int:
        """Evaluate vocabulary level (B1+) (0-10)"""
        # Placeholder for vocabulary checking
        score = 7  # Default score
        
        # Check for complex words and expressions
        complex_words = sum(1 for word in essay_text.split() if len(word) > 10)
        
        if complex_words < 5:
            score -= 3
        
        return max(0, min(10, score))
    
    def _evaluate_structure(self, essay_text: str) -> int:
        """Evaluate text structure (0-10)"""
        score = 7  # Default score
        
        # Check for paragraph structure
        paragraphs = essay_text.split('\n\n')
        if len(paragraphs) < 3:
            score -= 3
        
        # Check for introduction, body, conclusion
        text_lower = essay_text.lower()
        has_intro_words = any(word in text_lower for word in ['во-первых', 'прежде всего', 'introduction', 'вводная'])
        has_conclusion_words = any(word in text_lower for word in ['в заключение', 'таким образом', 'conclusion', 'итого'])
        
        if not has_intro_words:
            score -= 2
        if not has_conclusion_words:
            score -= 2
        
        return max(0, min(10, score))
    
    def _evaluate_goal_achievement(self, essay_text: str, topic: str = None) -> int:
        """Evaluate if essay achieves its goals (0-10)"""
        score = 7  # Default score
        
        # Check minimum length for goal achievement
        if len(essay_text) < 150:
            score -= 3
        
        # Check for main ideas
        if essay_text.count('главное') == 0 and essay_text.count('главная идея') == 0:
            score -= 2
        
        return max(0, min(10, score))
    
    def _generate_essay_feedback(self, feedback: EssayFeedback) -> str:
        """Generate detailed feedback comments"""
        comments = f"""
        Оценка эссе:
        
        1. Грамматика: {feedback.grammar_score}/10
        2. Вокабуляр (B1+): {feedback.vocabulary_score}/10
        3. Структура текста: {feedback.structure_score}/10
        4. Достижение целей: {feedback.goal_achievement_score}/10
        
        Итоговая оценка: {feedback.total_score}/10
        
        Рекомендации:
        - Проверьте грамматические конструкции
        - Используйте более сложный вокабуляр
        - Структурируйте текст с четкими абзацами
        - Убедитесь, что эссе достигает своей цели
        """
        return comments
    
    def get_available_subjects(self) -> List[str]:
        """Get list of available subjects"""
        return [subject.value for subject in Subject]
    
    def reset(self):
        """Reset application state"""
        self.current_subject = None
        self.current_topic = None
        self.explanation = None
        self.questions = []
        self.user_answers = {}
        self.error_count = 0
        self.passed = False


# Example usage
if __name__ == "__main__":
    app = StudyHard()
    
    # Print available subjects
    print("Доступные предметы:")
    for subject in app.get_available_subjects():
        print(f"  - {subject}")
    
    # Select a subject
    app.select_subject("english")
    print(f"\nВыбран предмет: {app.current_subject}")
    
    # Load a topic
    app.load_topic("Present Simple Tense")
    print(f"\nТема: {app.current_topic}")
    print(f"\nОбъяснение:\n{app.explanation}")
    
    print(f"\nВопросы для проверки знаний:")
    for i, q in enumerate(app.questions, 1):
        print(f"\n{i}. {q.question_text}")
        for opt in q.options:
            print(f"   {opt}")
