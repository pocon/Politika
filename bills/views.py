from bills.models import *
from bills.forms import *
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


def BillPage(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    return render_to_response('bills/page.html', {'bill': bill}, context_instance=RequestContext(request))

def BillDetailed(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    
    return render_to_response('bills/detailed.html', {'bill': bill}, context_instance=RequestContext(request))

def BillHistory(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    history = Edit.objects.filter(object_type="Bill").filter(object_id=bill_id)

    return render_to_response('bills/detailed.html', {'bill': bill}, context_instance=RequestContext(request))

@login_required
def BillEdit(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    if request.method == 'POST':
        form = BillEditForm(request.POST)
        if form.is_valid():
            bill.edit(editor=request.user, title=form.cleaned_data['title'], summary=form.cleaned_data['summary'], detailed=form.cleaned_data['detailed'])
            return redirect(bill)

    else:
        form = BillEditForm(bill)
        return render_to_response('bills/edit.html', {'bill': bill, 'form': form}, context_instance=RequestContext(request))

