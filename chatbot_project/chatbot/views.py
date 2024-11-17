from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .chatbot_logic import ChatbotLogic
from django.conf import settings
import os

# Initialize ChatbotLogic
chatbot_logic = ChatbotLogic(
    dataset_path=os.path.join(settings.BASE_DIR, 'chatbot', 'dataset.json'),
    unanswered_path=os.path.join(settings.BASE_DIR, 'chatbot', 'unanswered_questions.json')
)

def home(request):
    """Render the homepage for the chatbot"""
    return render(request, 'index.html')

@csrf_exempt
def chatbot(request):
    """Handle chat messages from the user"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()

            # Use chatbot logic to find a response
            response = chatbot_logic.find_best_response(question)

            if response:
                return JsonResponse({'response': response}, status=200)
            else:
                chatbot_logic.add_unanswered(question)
                return JsonResponse({
                    'response': "I'm sorry, I don't have an answer for that yet. It has been saved for review."
                }, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Error processing the request: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_unanswered_questions(request):
    """Fetch unanswered questions for users to review."""
    try:
        unanswered = chatbot_logic._load_json(chatbot_logic.unanswered_path)
        if not unanswered:
            return JsonResponse([], safe=False)  # Return an empty list if no questions
        return JsonResponse(unanswered, safe=False)
    except Exception as e:
        return JsonResponse({'error': f'Error fetching unanswered questions: {str(e)}'}, status=500)

@csrf_exempt
def submit_answers(request):
    """Handle submitted answers for unanswered questions"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            answers = data.get('answers', [])

            # Save answers to the dataset and remove from unanswered
            for answer in answers:
                question = answer.get('question')
                response = answer.get('response')
                if question and response:
                    chatbot_logic.save_answer(question, response)

            return JsonResponse({'message': 'Answers saved successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Error saving answers: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
