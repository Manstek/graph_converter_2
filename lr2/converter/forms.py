from django import forms


class IncidenceMatrixForm(forms.Form):
    matrix = forms.CharField(
        widget=forms.Textarea,
        help_text="Введите матрицу инцидентности, строки разделены новыми строками.")
