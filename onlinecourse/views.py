
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Submission


def course_list(request):
    courses = Course.objects.all()
    return render(request, "course_list.html", {"courses": courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "course_details_bootstrap.html", {"course": course})


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method != "POST":
        return redirect("course_details", course_id=course.id)

    selected_ids = [
    value for key, value in request.POST.items()
    if key.startswith("question_")
]
    questions = []
    for lesson in course.lessons.all():
        questions.extend(
            list(lesson.questions.prefetch_related("choices").all())
        )

    total_score = 0
    possible_score = 0

    for question in questions:
        possible_score += question.points
        total_score += question.is_get_score(selected_ids)

    submission = Submission.objects.create(
        user=request.user if request.user.is_authenticated else None,
        course=course,
        score=total_score,
        total_points=possible_score,
    )

    return redirect(
        "show_exam_result",
        course_id=course.id,
        submission_id=submission.id,
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission, pk=submission_id, course=course
    )

    selected_ids = request.GET.getlist("selected")
    questions = []
    for lesson in course.lessons.all():
        questions.extend(
            list(lesson.questions.prefetch_related("choices").all())
        )

    # Reconstruct result details from the submission score while retaining
    # question-by-question answer information for the result page.
    result_items = []
    for question in questions:
        correct_choices = list(question.choices.filter(is_correct=True))
        result_items.append({
            "question": question,
            "correct_choices": correct_choices,
        })

    grade = (
        round((submission.score / submission.total_points) * 100)
        if submission.total_points
        else 0
    )
    possible = submission.total_points

    return render(
        request,
        "exam_result_bootstrap.html",
        {
            "course": course,
            "selected_ids": selected_ids,
            "grade": grade,
            "possible": possible,
            "submission": submission,
            "result_items": result_items,
        },
    )
