from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from .models import BulkIssuance, IssueRequest, Transformation


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class IssueRequestForm(forms.ModelForm):
    class Meta:
        model = IssueRequest
        fields = ["asset", "quantity", "receiver"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "w-full rounded-lg bg-slate-800 border border-slate-700 px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500"
                }
            )


class TransformationForm(forms.ModelForm):
    class Meta:
        model = Transformation
        fields = [
            "raw_material",
            "finished_good_name",
            "finished_good_quantity",
            "consumed_quantity",
            "photo",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "w-full rounded-lg bg-slate-800 border border-slate-700 px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500"
                }
            )


class BulkIssuanceForm(forms.ModelForm):
    class Meta:
        model = BulkIssuance
        fields = ["asset", "class_name", "issued_quantity", "damaged_quantity", "wastage_notes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "w-full rounded-lg bg-slate-800 border border-slate-700 px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500"
                }
            )


class PermissionMatrixForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].widget.attrs.update(
            {
                "class": "mt-2 w-full rounded-lg bg-slate-800 border border-slate-700 px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500"
            }
        )
