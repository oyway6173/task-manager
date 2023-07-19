from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Project, Issue, Comments, Board, Status
from .forms import MyUserCreationForm, IssueCreationForm, IssueUpdateForm
from django.db.models import Q 
from django.http import HttpResponse

# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)  

        if user:
            login(request, user)
            return redirect('home')    
        else:
            return render(request, 'base/login_register.html', {
                'page': 'login',
                'message': 'Invalid credentials'
            })

    return render(request, 'base/login_register.html', {'page': 'login'})


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'base/login_register.html', {
                'page': 'register',
                'form': MyUserCreationForm(),
                'message': 'An error occurred during registration'
            })

    return render(request, 'base/login_register.html', {
        'page': 'register',
        'form': form    
    })


@login_required(login_url='/login')
def logoutPage(request):
    logout(request)
    return redirect('home')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    projects = Project.objects.all()

    all_issues = Issue.objects.all().count

    if q:
        issues = Issue.objects.filter(
            Q(project__id__iexact=q) 
            # Q(board__project__id__icontains=q) |
            # Q(name__icontains=q) |
            # Q(description__icontains=q)
        )
        issue_comments = Comments.objects.filter(
            Q(issue__project__id__iexact=q)
        )
    else: 
        issues = Issue.objects.all()
        issue_comments = Comments.objects.all()

    context = {
        'projects': projects,
        'all_issues': all_issues,
        'issues': issues,
        'issue_comments': issue_comments
    }
    return render(request, 'base/home.html', context)


@login_required(login_url='/login')
def issue(request, pk):

    issue = Issue.objects.get(id=pk)

    issue_comments = issue.comments_set.all()

    participants = issue.participants.all().exclude(
        Q(id__exact=issue.reporter.id) |
        Q(id__exact=issue.assignee.id)
    )

    if request.method == 'POST':
        comment = Comments.objects.create(
            user=request.user,
            issue=issue,
            body=request.POST.get('body')
        )
        issue.participants.add(request.user)
        return redirect('issue', pk=issue.id)

    context = {
        'issue': issue,
        'issue_comments': issue_comments,
        'participants': participants
    }
    return render(request, 'base/issue.html', context)


@login_required(login_url='/login')
def createIssue(request):

    form = IssueCreationForm()
    boards = Board.objects.all()
    projects = Project.objects.all()

    if request.method == 'POST':
        project_id = request.POST.get('project')
        project, created = Project.objects.get_or_create(name=project_id)
        board_label = request.POST.get('board')
        board, board_created = Board.objects.get_or_create(label=board_label, project=project, defaults={'name': board_label[1:].capitalize().replace('_', ' '), 'owner': request.user})
        if board_created:
            for i in range(1,4):
                status = Status.objects.get(description='default', step=i)
                status.board.add(board)
            status = Status.objects.get(description='default', step=1)
        else:
            status = Status.objects.get(board=board, step=1)

        Issue.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            board=board,
            status=status,
            reporter=request.user,
            assignee=User.objects.get(id=request.POST.get('assignee')) if request.POST.get('assignee') != '' else None,
            project=project
        )
        return redirect('home')
    
    context = {
        'form': form,
        'boards': boards,
        'projects': projects
    }
    return render(request, 'base/issue_form.html', context)


@login_required(login_url='/login')
def updateIssue(request, pk):
    issue = Issue.objects.get(id=pk)
    form = IssueUpdateForm(instance=issue)
    statuses = Status.objects.filter(board__id__iexact = issue.board.id)

    print(statuses)

    if request.user != issue.reporter and request.user != issue.assignee:
        return HttpResponse("Don't touch здесь!")
    
    if request.method == 'POST':
        issue.name = request.POST.get('name')
        issue.description = request.POST.get('description')
        issue.status = statuses.get(id=request.POST.get('status'))
        issue.assignee = User.objects.get(id=request.POST.get('assignee'))
        issue.save()
        return redirect('issue', pk=issue.id)
    
    context = {
        'issue': issue,
        'form': form,
        'statuses': statuses
    }
    return render(request, 'base/issue_update_form.html', context)
    

@login_required(login_url='/login')
def deleteIssue(request, pk):
    issue = Issue.objects.get(id=pk)

    if request.user != issue.reporter:
        return HttpResponse("Don't touch здесь!")
    
    if request.method == 'POST':
        issue.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': issue})


@login_required(login_url='/login')
def deleteComment(request, pk):
    comment = Comments.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse("Don't touch здесь!")
    
    if request.method == 'POST':
        comment.delete()
        return redirect('issue', pk=comment.issue.id)

    return render(request, 'base/delete.html', {'obj': comment})


def board(request, pk):

    board = Board.objects.get(id=pk)
    project = board.project
    project_boards = Board.objects.filter(project=project)
    statuses = Status.objects.filter(board=board)
    issues = Issue.objects.filter(project=project, board=board)

    context = {
        'board': board, 
        'project': project,
        'project_boards': project_boards, 
        'statuses': statuses,
        'issues': issues
    }
    return render(request, 'base/project-board.html', context)


def issues(request, pk):

    project = Project.objects.get(id=pk)
    project_boards = Board.objects.filter(project=project)
    issues = Issue.objects.filter(project=project)

    context = {
        'project': project,
        'issues': issues,
        'project_boards': project_boards
    }

    return render(request, 'base/project-board.html', context)


def boards(request):

    boards = Board.objects.all()

    context = {
        'boards': boards
    }
    return render(request, 'base/boards.html', context)