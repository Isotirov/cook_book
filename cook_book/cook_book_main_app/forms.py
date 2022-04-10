from django import forms

from cook_book.cook_book_main_app.models import CookedMeal, MealImage, Comment


class MainAppFormsMixin:
    fields = {}

    def add_class_create_recipe_form(self):
        for _, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += ' u-border-3 u-border-grey-30 u-input u-input-rectangle u-radius-10'


class CreateRecipeForm(forms.ModelForm, MainAppFormsMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_class_create_recipe_form()

    class Meta:
        model = CookedMeal
        exclude = ['user', 'initial_images']
        labels = {
            'type': 'Категория',
            'title': 'Име на рецептата',
            'ingredients': 'Продукти (по един на ред) / Пример: месце - 1 кг',
            'cooking_time': 'Време за приготвяне (минути)',
            'description': 'Описание / Начин на приготвяне',
        }

    bot_catcher = forms.CharField(
        required=False,
        widget=forms.HiddenInput)

    def clean_bot_catcher(self):
        value = self.cleaned_data['bot_catcher']
        if len(value) > 0:
            raise forms.ValidationError("Gotcha BOT")
        return value


class DeleteRecipeForm(forms.ModelForm):
    class Meta:
        model = CookedMeal
        fields = []


class CreateMealImage(forms.ModelForm):
    class Meta:
        model = MealImage
        fields = '__all__'


class EditRecipeForm(forms.ModelForm):

    class Meta:
        model = CookedMeal
        exclude = ['type', 'user']


# class DeleteRecipeForm(forms.ModelForm):
#     class Meta:
#         model = CookedMeal
#         exclude = ['type', 'user']
#
#     def save(self, commit=True):
#         self.instance.delete()
#         return self.instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'recipe']
        labels = {
            'comment': 'Напиши коментар',
        }
        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-radius-17 u-white',
                },
            ),
        }

    bot_catcher = forms.CharField(
        required=False,
        widget=forms.HiddenInput)

    def clean_bot_catcher(self):
        value = self.cleaned_data['bot_catcher']
        if len(value) > 0:
            raise forms.ValidationError("Gotcha BOT")
        return value
