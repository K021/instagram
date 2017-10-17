from django import forms


# class PostForm(forms.Form):
#     photo = forms.ImageField()
#     title = forms.CharField(max_length=50)
#     text = forms.CharField(max_length=50)
#
#     def clean_text(self):
#         data = self.cleaned_data['text']
#         if data != data.upper():
#             raise forms.ValidationError('All letters must be uppercase')
#         return data


# class PostComment(forms.Form):
#     comment = forms.CharField(
#         widget=forms.CharField(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )

class PostForm(forms.Form):
    photo = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean_text(self):
        data = self.cleaned_data['text']
        if data != data.upper():
            raise forms.ValidationError('All text must uppercase!')
        return data


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
            }
        )
    )
