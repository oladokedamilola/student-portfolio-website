from accounts.models import ClientProfile, StudentProfile

def unread_notifications_count(request):
    if request.user.is_authenticated:
        if request.user.role == "CLIENT":
            try:
                profile = ClientProfile.objects.get(user=request.user)
                count = profile.notifications.filter(is_read=False).count()
            except ClientProfile.DoesNotExist:
                count = 0
        elif request.user.role == "STUDENT":
            try:
                profile = StudentProfile.objects.get(user=request.user)
                count = profile.notifications.filter(is_read=False).count()
            except StudentProfile.DoesNotExist:
                count = 0
        else:
            count = 0
        return {'notifications_unread_count': count}
    return {}
