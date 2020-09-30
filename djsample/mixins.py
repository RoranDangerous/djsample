from django.http import Http404

class IsTeacherMixin(object):
    def has_permissions(self):
        return self.request.user.is_teacher

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404('You do not have permission.')
        return super(IsTeacherMixin, self).dispatch(
            request, *args, **kwargs)