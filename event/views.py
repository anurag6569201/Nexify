from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse , Http404
from .models import Form, Question, Response, Answer
from .forms import FormCreateForm, QuestionCreateForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Form, Question, Response, Answer
from django.forms import modelformset_factory
from collections import defaultdict


def add_questions(request, form_id):
    form = get_object_or_404(Form, id=form_id)

    if request.method == 'POST':        
        # Determine the number of questions dynamically based on the question_text keys in the POST data
        num_questions = len([key for key in request.POST if key.startswith("question_text_")])
        
        # Loop through each question
        for i in range(num_questions):
            question_text = request.POST.get(f'question_text_{i}')
            question_type = request.POST.get(f'question_type_{i}')
            
            if question_text and question_type:
                # Create the question instance
                question = Question.objects.create(
                    form=form,
                    text=question_text,
                    question_type=question_type
                )

                # If the question type is Multiple Choice or Dropdown, handle the choices
                if question_type in ['MC', 'DD']:
                    # Retrieve and process choices
                    choices = request.POST.getlist(f'choice_{i}[]')  # Get list of choices
                    question.choices = ','.join(choices)  # Store as a comma-separated string
                    question.save()  # Save the updated question with choices


        # After saving all questions, redirect to the form detail page
        return redirect('event:form_detail', form_id=form.id)

    return render(request, 'apps/event/add_questionss.html', {'form': form})

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



def view_forms(request):
    # Assuming the Form model has a 'form_type' attribute
    # Group forms by their 'form_type' attribute
    form_types = Form.objects.values('form_type').distinct()  # Get distinct form types
    
    grouped_forms = {}  # Dictionary to hold grouped forms
    
    for form_type in form_types:
        forms = Form.objects.filter(form_type=form_type['form_type'])
        grouped_forms[form_type['form_type']] = forms  # Group forms by type
    
    # Passing the grouped forms to the template
    context = {
        'grouped_forms': grouped_forms
    }
    return render(request, 'forms/view_forms.html', context)


def form_list(request):
    """View to list all forms."""
    forms = Form.objects.all()
    return render(request, 'forms/form_list.html', {'forms': forms})


def create_form(request):
    if request.method == 'POST':
        form = FormCreateForm(request.POST ,request.FILES)
        if form.is_valid():
            new_form = form.save()
            # Redirect to add_question view with the newly created form's ID
            return redirect('event:add_questions', form_id=new_form.id)
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
  # Handle file upload for images
            if question.question_type == 'IMG':
                answer_file = request.FILES.get(f'question_{question.id}')
                if answer_file:
                    Answer.objects.create(response=response, question=question, answer_image=answer_file)
            else:
                # Handle text-based answers
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
            return redirect('event:view_forms')  # Redirect to the form list after deletion
    except Form.DoesNotExist:
        raise Http404("Form not found")
