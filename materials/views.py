from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import StudyMaterial, ChatMessage
from .ai_helper import extract_text_from_pdf, generate_mcq_questions, generate_flashcards, chat_with_material
from quiz.models import Question, Flashcard
from progress.models import QuizAttempt
import json

def landing(request):
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    search = request.GET.get('search', '')
    subject_filter = request.GET.get('subject', '')

    materials = StudyMaterial.objects.filter(user=request.user).order_by('-uploaded_at')

    if search:
        materials = materials.filter(title__icontains=search) | materials.filter(subject__icontains=search)
        materials = materials.distinct()

    if subject_filter:
        materials = materials.filter(subject__icontains=subject_filter)

    # Get all unique subjects for filter tabs
    all_materials = StudyMaterial.objects.filter(user=request.user)
    subjects = list(all_materials.values_list('subject', flat=True).distinct())

    # Group materials by subject
    from collections import defaultdict
    grouped = defaultdict(list)
    for m in materials:
        grouped[m.subject].append(m)

    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-attempted_at')[:5]

    return render(request, 'dashboard.html', {
        'materials': materials,
        'attempts': attempts,
        'subjects': subjects,
        'grouped': dict(grouped),
        'search': search,
        'subject_filter': subject_filter,
    })

@login_required
def upload_material(request):
    if request.method == 'POST':
        title = request.POST['title']
        subject = request.POST['subject']
        file = request.FILES['file']

        material = StudyMaterial.objects.create(
            user=request.user,
            title=title,
            subject=subject,
            file=file
        )

        try:
            text = extract_text_from_pdf(material.file.path)
            material.extracted_text = text
            material.save()
            messages.success(request, 'Material uploaded! You can now generate questions and flashcards.')
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')

        return redirect('material_detail', pk=material.pk)

    return render(request, 'materials/upload.html')

@login_required
def generate_content(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    if request.method == 'POST':
        num_questions = int(request.POST.get('num_questions', 10))
        num_flashcards = int(request.POST.get('num_flashcards', 10))

        try:
            # Delete old questions and flashcards
            Question.objects.filter(material=material).delete()
            Flashcard.objects.filter(material=material).delete()

            questions = generate_mcq_questions(material.extracted_text, num_questions)
            for q in questions:
                Question.objects.create(
                    material=material,
                    question_text=q['question'],
                    option_a=q['option_a'],
                    option_b=q['option_b'],
                    option_c=q['option_c'],
                    option_d=q['option_d'],
                    correct_answer=q['correct_answer'],
                    explanation=q.get('explanation', ''),
                    difficulty=q.get('difficulty', 'medium'),
                    question_type='mcq'
                )

            flashcards = generate_flashcards(material.extracted_text, num_flashcards)
            for f in flashcards:
                Flashcard.objects.create(
                    material=material,
                    front=f['front'],
                    back=f['back']
                )

            return JsonResponse({'success': True, 'questions': len(questions), 'flashcards': len(flashcards)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'error': 'Invalid request'})

@login_required
def material_detail(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    questions = Question.objects.filter(material=material)
    flashcards = Flashcard.objects.filter(material=material)
    attempts = QuizAttempt.objects.filter(user=request.user, material=material).order_by('-attempted_at')
    chat_history = ChatMessage.objects.filter(material=material, user=request.user)
    return render(request, 'materials/detail.html', {
        'material': material,
        'questions': questions,
        'flashcards': flashcards,
        'attempts': attempts,
        'chat_history': chat_history,
    })

@login_required
def delete_material(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    material.delete()
    messages.success(request, 'Material deleted.')
    return redirect('dashboard')

@login_required
def chat_view(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        # Load history from DB
        history = list(ChatMessage.objects.filter(
            material=material, user=request.user
        ).values('role', 'content'))

        # Save user message
        ChatMessage.objects.create(
            material=material,
            user=request.user,
            role='user',
            content=user_message
        )

        response = chat_with_material(material.extracted_text, user_message, history)

        # Save assistant response
        ChatMessage.objects.create(
            material=material,
            user=request.user,
            role='assistant',
            content=response
        )

        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'})