from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse , Http404
from .models import Form, Question, Response, Answer
from .forms import FormCreateForm, QuestionCreateForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Form, Question, Response, Answer
from django.forms import modelformset_factory


def add_questions(request, form_id):
    form = get_object_or_404(Form, id=form_id)

    if request.method == 'POST':
        # Loop through all the question fields by index (instead of using getlist)
        question_texts = [request.POST.get(f'question_text_{i}') for i in range(len(request.POST) // 2)]
        question_types = [request.POST.get(f'question_type_{i}') for i in range(len(request.POST) // 2)]

        # Loop through each question and create it
        for i in range(len(question_texts)):
            if question_texts[i] and question_types[i]:
                question = Question.objects.create(
                    form=form,
                    text=question_texts[i],
                    question_type=question_types[i]
                )

                # Handle choices for MC and DD types (Multiple Choice and Dropdown)
                if question_types[i] in ['MC', 'DD']:
                    choices = request.POST.getlist(f'choice_{i}')  # Get the choices for this question
                    question.choices = ','.join(choices)  # Store choices as comma-separated string
                    question.save()

        return redirect('form_detail', form_id=form.id)  # Redirect to form detail after saving questions

    return render(request, 'forms/add_questions.html', {'form': form})


# Other views...

def view_all_questions(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    questions = form.questions.all()  # Get all the questions related to the form
    return render(request, 'forms/view_all_questions.html', {'form': form, 'questions': questions})


def form_responses(request, form_id):
    """View to list all submissions of a specific form."""
    form = get_object_or_404(Form, id=form_id)
    responses = form.responses.all()  # Retrieve all responses for this form
    return render(request, 'forms/form_responses.html', {'form': form, 'responses': responses})


def form_list(request):
    """View to list all forms."""
    forms = Form.objects.all()
    return render(request, 'forms/form_list.html', {'forms': forms})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Form, Question, Response, Answer
from .forms import FormCreateForm, QuestionCreateForm

def create_form(request):
    if request.method == 'POST':
        form = FormCreateForm(request.POST)
        if form.is_valid():
            new_form = form.save()
            # Redirect to add_question view with the newly created form's ID
            return redirect('add_questions', form_id=new_form.id)
    else:
        form = FormCreateForm()
    return render(request, 'forms/create_form.html', {'form': form})


def form_detail(request, form_id):
    """View to display and submit a form."""
    form = get_object_or_404(Form, id=form_id)
    questions = form.questions.all()

    # Prepare split choices for multiple choice and dropdown questions
    for question in questions:
        if question.question_type in ['MC', 'DD']:  # MC for multiple choice, DD for dropdown
            question.split_choices = question.choices.split(',') if question.choices else []

    if request.method == 'POST':
        # Save the response as a new instance for each submission
        response = Response(form=form)
        response.save()

        # Process each question's answer
        for question in questions:
            answer_text = request.POST.get(f'question_{question.id}')
            if answer_text:
                Answer.objects.create(response=response, question=question, answer_text=answer_text)

        # Redirect to the same form to allow multiple submissions
        return redirect('form_detail', form_id=form.id)

    return render(request, 'forms/form_detail.html', {'form': form, 'questions': questions})

def delete_form(request, form_id):
    try:
        form = Form.objects.get(id=form_id)
        if request.method == 'POST':
            form.delete()
            return redirect('form_list')  # Redirect to the form list after deletion
    except Form.DoesNotExist:
        raise Http404("Form not found")