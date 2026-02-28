from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import StudyMaterial, ChatMessage, MaterialFile
from .ai_helper import extract_text_from_pdf, generate_mcq_questions, generate_flashcards, chat_with_material
from quiz.models import Question, Flashcard
from progress.models import QuizAttempt
from collections import defaultdict
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

    all_materials = StudyMaterial.objects.filter(user=request.user)
    subjects = list(all_materials.values_list('subject', flat=True).distinct())

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
        files = request.FILES.getlist('files')

        if not files:
            messages.error(request, 'Please upload at least one file!')
            return redirect('upload')

        # Validate ALL files BEFORE creating material
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg', '.tiff', '.ico', '.heic')
        for uploaded_file in files:
            if uploaded_file.size > 15 * 1024 * 1024:
                messages.error(request, f'{uploaded_file.name} exceeds the 15MB size limit!')
                return redirect('upload')
            if uploaded_file.name.lower().endswith(image_extensions):
                messages.error(request, f'{uploaded_file.name} is an image file and is not supported!')
                return redirect('upload')

        # Only create material if all files pass validation
        material = StudyMaterial.objects.create(
            user=request.user,
            title=title,
            subject=subject,
        )

        # Process each file
        combined_text = ""
        successful = 0
        for uploaded_file in files:
            try:
                mat_file = MaterialFile.objects.create(
                    material=material,
                    file=uploaded_file,
                    filename=uploaded_file.name
                )
                text = extract_text_from_pdf(mat_file.file.path)
                combined_text += "\n\n--- " + uploaded_file.name + " ---\n\n" + text
                successful += 1
            except Exception as e:
                messages.error(request, 'Error reading ' + uploaded_file.name + ': ' + str(e))

        if successful == 0:
            material.delete()
            messages.error(request, 'No files could be processed. Material was not created.')
            return redirect('upload')

        material.extracted_text = combined_text
        material.save()
        messages.success(request, f'{successful} file(s) uploaded successfully!')
        return redirect('material_detail', pk=material.pk)

    return render(request, 'materials/upload.html')

@login_required
def add_file(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        if not files:
            return JsonResponse({'success': False, 'error': 'No files uploaded'})

        added = []
        for f in files:
            try:
                mat_file = MaterialFile.objects.create(
                    material=material,
                    file=f,
                    filename=f.name
                )
                text = extract_text_from_pdf(mat_file.file.path)
                # Append new text to existing
                material.extracted_text += f"\n\n--- {f.name} ---\n\n" + text
                material.save()
                added.append(f.name)
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})

        return JsonResponse({'success': True, 'added': added, 'count': len(added)})
    return JsonResponse({'error': 'Invalid request'})

@login_required
def delete_file(request, pk, file_id):
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    mat_file = get_object_or_404(MaterialFile, pk=file_id, material=material)
    mat_file.delete()

    # Rebuild extracted text from remaining files
    combined_text = ""
    for f in material.files.all():
        try:
            text = extract_text_from_pdf(f.file.path)
            combined_text += f"\n\n--- {f.filename} ---\n\n" + text
        except:
            pass
    material.extracted_text = combined_text
    material.save()

    return JsonResponse({'success': True})

@login_required
def generate_content(request, pk):
    material = get_object_or_404(StudyMaterial, pk=pk, user=request.user)
    if request.method == 'POST':
        num_questions = int(request.POST.get('num_questions', 10))
        num_flashcards = int(request.POST.get('num_flashcards', 10))
        selected_files = request.POST.getlist('selected_files')
        # selected_files = list of file IDs user selected

        try:
            # Build text from selected files only
            if selected_files:
                text = ""
                for file_id in selected_files:
                    try:
                        mat_file = MaterialFile.objects.get(pk=file_id, material=material)
                        file_text = extract_text_from_pdf(mat_file.file.path)
                        text += f"\n\n--- {mat_file.filename} ---\n\n" + file_text
                    except:
                        pass
            else:
                text = material.extracted_text
            # If no files selected use all text

            Question.objects.filter(material=material).delete()
            Flashcard.objects.filter(material=material).delete()

            questions = generate_mcq_questions(text, num_questions)
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

            flashcards = generate_flashcards(text, num_flashcards)
            for f in flashcards:
                Flashcard.objects.create(
                    material=material,
                    front=f['front'],
                    back=f['back']
                )

            return JsonResponse({
                'success': True,
                'questions': len(questions),
                'flashcards': len(flashcards)
            })
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
    mat_files = material.files.all()
    return render(request, 'materials/detail.html', {
        'material': material,
        'questions': questions,
        'flashcards': flashcards,
        'attempts': attempts,
        'chat_history': chat_history,
        'mat_files': mat_files,
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
        selected_files = data.get('selected_files', [])

        # Build text from selected files
        if selected_files:
            text = ""
            for file_id in selected_files:
                try:
                    mat_file = MaterialFile.objects.get(pk=file_id, material=material)
                    file_text = extract_text_from_pdf(mat_file.file.path)
                    text += f"\n\n--- {mat_file.filename} ---\n\n" + file_text
                except:
                    pass
        else:
            text = material.extracted_text

        history = list(ChatMessage.objects.filter(
            material=material, user=request.user
        ).values('role', 'content'))

        ChatMessage.objects.create(
            material=material,
            user=request.user,
            role='user',
            content=user_message
        )

        response = chat_with_material(text, user_message, history)

        ChatMessage.objects.create(
            material=material,
            user=request.user,
            role='assistant',
            content=response
        )

        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'})