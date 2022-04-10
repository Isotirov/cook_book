from django import forms

from cook_book.cook_book_profiles.models import CookBookUserProfile


class ProfileFormsMixin:
    fields = {}

    def add_class_update_profile_form(self):
        for _, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' u-border-3 u-border-grey-30 u-input u-input-rectangle u-radius-10'


class UpdateProfileForm(forms.ModelForm, ProfileFormsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_class_update_profile_form()

    class Meta:
        model = CookBookUserProfile
        exclude = ['joined', 'user', 'is_complete']
        labels = {
            'image': 'Профилна снимка - оставете празно, за да остане сегашната снимка',
            'first_name': 'Име',
            'last_name': 'Фамилия',
        }
        widgets = {
            'image': forms.FileInput(
                attrs={
                    'onchange': "readURL(this);",
                },
            ),
        }
