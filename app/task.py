from huey.contrib.djhuey import task
from apps.votes.models import Vote
from apps.choices.models import Choice
from apps.polls.models import Poll
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Count
import json

User = get_user_model()

@task()
def submit_vote_task(user_id, poll_id, choice_id):
    try:
        print(f"⏳ Processing vote: user={user_id}, poll={poll_id}, choice={choice_id}")
        
        user = User.objects.get(id=user_id)
        poll = Poll.objects.get(id=poll_id)
        choice = Choice.objects.get(id=choice_id, poll=poll)

        # Check if user already voted
        if Vote.objects.filter(user=user, poll=poll).exists():
            print(f"⚠️ User {user_id} already voted in poll {poll_id}")
            return {
                'status': 'failed',
                'reason': 'already_voted',
                'poll_id': str(poll_id)
            }

        # Create the vote
        vote = Vote.objects.create(user=user, poll=poll, choice=choice)
        print(f"✅ Vote created with ID: {vote.id}")

        # Calculate updated stats for the poll
        total_votes = Vote.objects.filter(poll=poll).count()
        
        # Get choice data
        choices_data = []
        for c in poll.choices.all():
            vote_count = Vote.objects.filter(choice=c).count()
            percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
            choices_data.append({
                'id': str(c.id),
                'text': c.text,
                'vote_count': vote_count,
                'percentage': round(percentage, 2)
            })

        # Prepare update data
        update_data = {
            'poll_id': str(poll_id),
            'question': poll.question,
            'total_votes': total_votes,
            'choices': choices_data,
            'message': f"New vote in '{poll.question[:20]}...'",
        }
        
        # Get channel layer
        channel_layer = get_channel_layer()
        
        # Send detail update to specific poll group
        detail_message = {
            'type': 'poll_update',
            'data': {
                **update_data,
                'update_type': 'detail'
            }
        }
        print(f"📤 Sending detail update to poll_{poll_id} group: {json.dumps(detail_message)[:100]}...")
        async_to_sync(channel_layer.group_send)(f"poll_{poll_id}", detail_message)

        # Send index update to all polls group
        index_message = {
            'type': 'poll_update',
            'data': {
                **update_data,
                'update_type': 'index'
            }
        }
        print(f"📤 Sending index update to all_polls group: {json.dumps(index_message)[:100]}...")
        async_to_sync(channel_layer.group_send)("all_polls", index_message)

        print(f"✅ WebSocket messages sent successfully")
        return {
            'status': 'success',
            'poll_id': str(poll_id),
            'total_votes': total_votes
        }

    except Exception as e:
        print(f"❌ Error in submit_vote_task: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'status': 'error',
            'reason': str(e),
            'poll_id': str(poll_id) if poll_id else "unknown"
        }