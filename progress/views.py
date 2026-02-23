from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import QuizAttempt, AttemptAnswer
from django.utils import timezone
from datetime import timedelta

@login_required
def progress_view(request):
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-attempted_at')

    total_attempts = attempts.count()
    avg_score = 0
    if total_attempts > 0:
        avg_score = round(sum(a.percentage() for a in attempts) / total_attempts)

    # Calculate streak
    streak = 0
    today = timezone.now().date()
    check_date = today
    while True:
        if QuizAttempt.objects.filter(
            user=request.user,
            attempted_at__date=check_date
        ).exists():
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    return render(request, 'progress/progress.html', {
        'attempts': attempts,
        'total_attempts': total_attempts,
        'avg_score': avg_score,
        'streak': streak,
    })