from django import template
from accounts.models import StudentProfile, ClientProfile

register = template.Library()

@register.simple_tag
def get_profile_image(user):
    try:
        if hasattr(user, 'studentprofile') and user.studentprofile.profile_image:
            return user.studentprofile.profile_image.url
        elif hasattr(user, 'clientprofile') and user.clientprofile.profile_image:
            return user.clientprofile.profile_image.url
    except:
        pass
    return None
