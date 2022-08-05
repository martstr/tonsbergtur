from django import template

register = template.Library()

@register.simple_tag
def responded_correctly(problem, user):
    return problem.user_has_correct_answer(user)

@register.simple_tag
def problems_completed(location, user):
    return location.get_completed_problem_count(user)

@register.simple_tag
def location_completed(location, user):
    return location.location_completed(user)

@register.simple_tag
def location_title(location, user):
    return location.location_found(user)

@register.simple_tag
def get_accepted_answer(problem, user):
    return problem.get_accepted_answer(user)