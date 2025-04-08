from django.views.generic import DetailView, ListView
from django.shortcuts import redirect
from django.contrib import messages
from apps.polls.models import Poll
from apps.choices.models import Choice
from apps.votes.models import Vote
from app.task import submit_vote_task

class DashboardView(ListView):
    model = Poll
    template_name = 'dashboard/index.html'
    context_object_name = 'polls'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for poll in context['polls']:
            poll.total_votes = Vote.objects.filter(poll=poll).count()
        return context

class VoteDetailView(DetailView):
    model = Poll
    template_name = 'dashboard/vote_detail.html'
    context_object_name = 'poll'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll = self.object
        choices = poll.choices.all()
        total_votes = Vote.objects.filter(poll=poll).count()

        choice_votes = []
        for choice in choices:
            vote_count = Vote.objects.filter(choice=choice).count()
            vote_percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            choice_votes.append({
                'id': choice.id,
                'text': choice.text,
                'vote_count': vote_count,
                'percentage': vote_percentage,
            })

        context['choices'] = choice_votes
        context['total_votes'] = total_votes
        context['has_voted'] = Vote.objects.filter(user=self.request.user, poll=poll).exists()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        selected_choice_id = request.POST.get('choice')

        if not selected_choice_id:
            messages.error(request, "Please select an option to vote.")
            return self.render_to_response(self.get_context_data())

        try:
            choice = Choice.objects.get(id=selected_choice_id, poll=self.object)

            existing_vote = Vote.objects.filter(user=request.user, poll=self.object).first()
            if existing_vote:
                messages.error(request, "You have already voted in this poll.")
                return self.render_to_response(self.get_context_data())

            submit_vote_task(user_id=request.user.id, poll_id=self.object.id, choice_id=choice.id)

            messages.success(request, "Your vote is being processed!")
            return redirect("dashboard")

        except Choice.DoesNotExist:
            messages.error(request, "Invalid choice selected.")
            return self.render_to_response(self.get_context_data())