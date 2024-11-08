from django.shortcuts import render, get_object_or_404, redirect
from .models import PollSet, PollOption
from .forms import PollCreationForm, VoteForm
from django.utils import timezone

def create_poll(request):
    if request.method == 'POST':
        form = PollCreationForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.save()

            # Collect all options from the request
            options = request.POST.getlist('options')
            for option_text in options:
                if option_text.strip():
                    PollOption.objects.create(poll=poll, text=option_text.strip())
            
            return redirect('view_poll', poll_id=poll.id)
    else:
        form = PollCreationForm()
    return render(request, 'polls/create_poll.html', {'form': form})

def view_poll(request, poll_id):
    poll = get_object_or_404(PollSet, id=poll_id)
    return render(request, 'polls/view_poll.html', {'poll': poll})

def poll_closed(request, poll_id):
    poll = get_object_or_404(PollSet, id=poll_id)
    winning_option = poll.options.order_by('-votes').first()
    return render(request, 'poll_closed', {'poll': poll,
                                                        'winner': winning_option,
                                                        'close_time': poll.closed_at})
# View for voting on a poll


from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

def vote_poll(request, poll_id):
    # Retrieve the poll
    poll = get_object_or_404(PollSet, id=poll_id)
    # Check and update poll status if the closing time has passed

    # If the poll is closed, render the closed poll page
    if poll.is_closed():
        poll.save()
        # Find the winning option
        winning_option = poll.options.order_by('-votes').first()
        return render(request, 'polls/poll_closed.html', {'poll': poll,
                                                        'winner': winning_option,
                                                        'close_time': poll.closed_at})

    # Handle form submission (POST request)
    if request.method == 'POST':
        form = VoteForm(poll, request.POST)
        if form.is_valid():
            # Get the selected option from the form
            selected_option = form.cleaned_data['option']
            selected_option.votes += 1
            selected_option.save()

            # Redirect to the results page after voting
            return redirect('poll_results', poll_id=poll.id)
    else:
        # Display the form for GET request
        form = VoteForm(poll)

        # Render the vote_poll template with the poll and form
        return render(request, 'polls/vote_poll.html', {'form': form, 'poll': poll})

def poll_results(request, poll_id):
    poll = get_object_or_404(PollSet, id=poll_id)
    total_votes = sum(option.votes for option in poll.options.all())
    results = [
        {
            'option': option.text,
            'votes': option.votes,
            'percentage': (option.votes / total_votes) * 100 if total_votes > 0 else 0
        }
        for option in poll.options.all()
    ]
    return render(request, 'polls/poll_results.html', {'poll': poll, 'results': results})


from django.shortcuts import render, get_object_or_404, redirect
from .models import PollSet, PollOption
from .forms import PollCreationForm, VoteForm

# View for displaying all polls
def main(request):
    polls = PollSet.objects.all()
    return render(request, 'polls/main.html', {'polls': polls})

# View for deleting a poll
def delete_poll(request, poll_id):
    poll = get_object_or_404(PollSet, id=poll_id)
    poll.delete()
    return redirect('main')

from datetime import datetime

def poll_status(poll):
    # Check if the poll is closed based on current time
    if poll.closed_at and poll.closed_at < datetime.now():
        poll.is_closed = True
        poll.save()
