from django import forms


class PostForm(forms.Form):
    photo = forms.ImageField()
    # text = forms.CharField(max_length=50)
    #
    # def clean_text(self):
    #     data = self.cleaned_data['text']
    #     if data != data.upper():
    #         raise forms.ValidationError('All letters must be uppercase')
    #     return data


# class PostComment(forms.Form):
#     comment = forms.CharField(
#         widget=forms.CharField(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
