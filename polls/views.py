from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# Flaw 1: Broken authentication
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
    """ Flaw 1 fix: 
    from django.shortcuts import render, get_object_or_404
    from django.http import HttpResponse, HttpResponseRedirect
    from django.urls import reverse
    from .models import Question, Choice
    from django.contrib.auth.decorators import login_required

    @login_required
    def vote(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    """

# Flaw 2: SQL Injection
def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        questions = Question.objects.raw("SELECT * FROM polls_question WHERE question_text LIKE '%" + q + "%'")
        return render(request, 'polls/search_results.html', {'questions': questions})
    else:
        return HttpResponse('No search query provided.')

# Flaw 2 fix: 
# def search(request):
#     if 'q' in request.GET:
#         q = request.GET['q']
#         questions = Question.objects.filter(question_text__icontains=q)
#         return render(request, 'polls/search_results.html', {'questions': questions})
#     else:
#         return HttpResponse('No search query provided.')

@login_required
def create_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        pub_date = request.POST.get('pub_date')
        # create a new question
        question = Question.objects.create(question_text=question_text, pub_date=pub_date)
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        return render(request, 'polls/create_question.html')
    



def registrationsuccess(request):
    return render(request, 'polls/registrationsuccess.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Flaw 3: Sensitive data exposure. Note: backend.py required to complete the flaw
        user = User(username=username, password=password)  
        user.save()
        
        return render(request, 'polls/registrationsuccess.html')
    else:
        return render(request, 'polls/register.html')

    """
Flaw 3 fix:
Note: backend.py should also be removed

    from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        hashed_password = make_password(password)  # Hash the password
        
        user = User(username=username, password=hashed_password)  
        user.save()
        
        return render(request, 'polls/registrationsuccess.html')
    else:
        return render(request, 'polls/register.html')
"""


# Flaw 4: Cross-Site Scripting (XSS)
    
from django.utils.safestring import mark_safe  # Flaw 4: Importing mark_safe to create flaw 4. 
#Part of fix: in secure application this import should be removed.

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # Disabling escaping by marking the question_text as safe
    question_text = mark_safe(question.question_text)
    return render(request, 'polls/detail.html', {'question': question_text})

#Flaw 4 fix
"""
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
  
    question_text = question.question_text
    return render(request, 'polls/detail.html', {'question': question_text})
"""

# Flaw 5: Security Misconfiguration
def debug_info(request):
    debug_info = {}
    # Adding username and IP address to debug_info
    debug_info['username'] = request.user.username
    debug_info['ip_address'] = request.META.get('REMOTE_ADDR', None)
    return render(request, 'polls/debug.html', {'debug_info': debug_info})

"""Flaw 5 fix:
To fix security misconfiguration, I need to restrict access to sensitive debug 
 information. This involves implementing proper access controls, 
 such as role-based access control (RBAC) or permission checks, 
 to ensure that debug information is only accessible to authorized users 
 with appropriate permissions. IN settings.py, I also should disable debug mode, which prevents exposing
sensitive information


"""
