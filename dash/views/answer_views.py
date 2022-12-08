from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..models import Answer, Question
from ..forms import AnswerForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages



def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    form = AnswerForm(request.POST)
    if form.is_valid():
        answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now(), author=request.user)
        answer.save()
    return redirect('{}#answer_{}'.format(resolve_url('dash:detail', question_id=question.id), answer.id))

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('dash:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(resolve_url('dash:detail', question_id=answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'dash/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('dash:detail', question_id=answer.question.id)


@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(resolve_url('dash:detail', question_id=answer.question.id), answer.id))
