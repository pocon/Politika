from django.forms import ModelForm
from bills.models import *

class BillEditForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('title', 'summary', 'detailed')
