from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def question_user_like(context, question):
    user = context.request.user
    if not user.id:
        return 0
    q = question.likes.filter(author=user).first()
    if not q:
        return 0
    return q.value


@register.simple_tag(takes_context=True)
def question_user_answer(context, question):
    user = context.request.user
    if not user.id:
        return 0
    q = question.answers.filter(author=user).first()
    if not q:
        return 0
    print(q.value)
    return q.value