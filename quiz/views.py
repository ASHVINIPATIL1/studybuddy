from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Flashcard
from materials.models import StudyMaterial
from progress.models import QuizAttempt, AttemptAnswer

@login_required
def take_quiz(request, material_id):
    material = get_object_or_404(StudyMaterial, pk=material_id, user=request.user)
    difficulty = request.GET.get('difficulty', 'all')
    questions = Question.objects.filter(material=material, question_type='mcq')
    if difficulty != 'all':
        questions = questions.filter(difficulty=difficulty)

    easy_count = Question.objects.filter(material=material, difficulty='easy').count()
    medium_count = Question.objects.filter(material=material, difficulty='medium').count()
    hard_count = Question.objects.filter(material=material, difficulty='hard').count()

    return render(request, 'quiz/take_quiz.html', {
        'material': material,
        'questions': questions,
        'difficulty': difficulty,
        'easy_count': easy_count,
        'medium_count': medium_count,
        'hard_count': hard_count,
    })

@login_required
def submit_quiz(request, material_id):
    material = get_object_or_404(StudyMaterial, pk=material_id, user=request.user)
    difficulty = request.POST.get('difficulty', 'all')
    questions = Question.objects.filter(material=material, question_type='mcq')
    if difficulty != 'all':
        questions = questions.filter(difficulty=difficulty)

    score = 0
    attempt = QuizAttempt.objects.create(
        user=request.user,
        material=material,
        total_questions=questions.count()
    )

    results = []
    wrong_ids = []
    for question in questions:
        user_answer = request.POST.get(f'question_{question.id}', '')
        is_correct = user_answer.lower() == question.correct_answer.lower()
        if is_correct:
            score += 1
        else:
            wrong_ids.append(question.id)
        AttemptAnswer.objects.create(
            attempt=attempt,
            question=question,
            user_answer=user_answer,
            is_correct=is_correct
        )
        results.append({
            'question': question,
            'user_answer': user_answer,
            'is_correct': is_correct,
        })

    attempt.score = score
    attempt.save()

    return render(request, 'quiz/results.html', {
        'attempt': attempt,
        'results': results,
        'material': material,
        'wrong_ids': ','.join(str(i) for i in wrong_ids),
    })

@login_required
def retry_wrong(request, material_id):
    material = get_object_or_404(StudyMaterial, pk=material_id, user=request.user)
    wrong_ids = request.GET.get('ids', '')
    if wrong_ids:
        id_list = [int(i) for i in wrong_ids.split(',') if i]
        questions = Question.objects.filter(id__in=id_list)
    else:
        questions = Question.objects.none()

    return render(request, 'quiz/take_quiz.html', {
        'material': material,
        'questions': questions,
        'difficulty': 'retry',
        'easy_count': 0,
        'medium_count': 0,
        'hard_count': 0,
    })

@login_required
def flashcards_view(request, material_id):
    material = get_object_or_404(StudyMaterial, pk=material_id, user=request.user)
    flashcards = Flashcard.objects.filter(material=material)
    return render(request, 'quiz/flashcards.html', {
        'material': material,
        'flashcards': flashcards
    })