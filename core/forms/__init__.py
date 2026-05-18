from .auth_forms import (
    CustomAllauthLoginForm,
    CustomPasswordChangeForm,
    CustomSignupForm,
    LoginForm,
)
from .avatar_forms import AvatarBuilderForm
from .class_forms import (
    ClassForm,
    ClassGroupEditForm,
    CreateStudentForm,
    StudentSignupForm,
)
from .forum_forms import ForumPostForm, ForumReplyForm
from .profile_forms import ProfileForm
from .resource_forms import TeachingResourceForm

__all__ = [
    "AvatarBuilderForm",
    "ClassForm",
    "ClassGroupEditForm",
    "CreateStudentForm",
    "CustomAllauthLoginForm",
    "CustomPasswordChangeForm",
    "CustomSignupForm",
    "ForumPostForm",
    "ForumReplyForm",
    "LoginForm",
    "ProfileForm",
    "StudentSignupForm",
    "TeachingResourceForm",
]
