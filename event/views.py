from django.shortcuts import render, redirect
from .forms import FormForm, QuestionForm, OptionForm
from .models import Form, Question, Option

def save_form(request):
    if request.method == 'POST':
        # Save the form title and description
        form_data = FormForm(request.POST)

        if form_data.is_valid():
            form_instance = form_data.save()  # Save Form instance
            
            # Get the questions data
            questions = request.POST.getlist('questions[0][text]')  # This will need to change to match your structure
            question_types = request.POST.getlist('questions[0][question_type]')  # Same here

            for i in range(len(questions)):
                question_text = questions[i]
                question_type = question_types[i]
                
                # Create and save the Question instance
                question = Question.objects.create(
                    form=form_instance,
                    text=question_text,
                    question_type=question_type
                )
                
                # If the question type has options, save those too
                options = request.POST.getlist(f'options[{i}]')  # Adjust as needed to capture the specific options for each question
                for option_text in options:
                    Option.objects.create(
                        question=question,
                        text=option_text
                    )

            #return redirect('event:success')  # Redirect to a success page or wherever you want
    else:
        form_data = FormForm()

    return render(request, 'apps/event/event.html', {'form': form_data})  # Adjust the template name as needed
