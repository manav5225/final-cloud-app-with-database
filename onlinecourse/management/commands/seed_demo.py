from django.core.management.base import BaseCommand
from onlinecourse.models import Course, Lesson, Question, Choice

class Command(BaseCommand):
    help = "Create a demo course with lessons, questions and choices."

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            name="Python Fundamentals",
            defaults={"description": "Learn Python basics and programming fundamentals."},
        )
        lesson, _ = Lesson.objects.get_or_create(
            course=course, order=1,
            defaults={"title": "Python Basics", "content": "Variables, data types and control flow."},
        )
        q1, _ = Question.objects.get_or_create(
            lesson=lesson, text="Which keyword defines a function in Python?",
            defaults={"points": 1},
        )
        Choice.objects.get_or_create(question=q1, text="def", defaults={"is_correct": True})
        Choice.objects.get_or_create(question=q1, text="func", defaults={"is_correct": False})
        Choice.objects.get_or_create(question=q1, text="function", defaults={"is_correct": False})

        q2, _ = Question.objects.get_or_create(
            lesson=lesson, text="Which type stores True or False?",
            defaults={"points": 1},
        )
        Choice.objects.get_or_create(question=q2, text="bool", defaults={"is_correct": True})
        Choice.objects.get_or_create(question=q2, text="string", defaults={"is_correct": False})
        Choice.objects.get_or_create(question=q2, text="list", defaults={"is_correct": False})

        self.stdout.write(self.style.SUCCESS("Demo course created successfully."))
