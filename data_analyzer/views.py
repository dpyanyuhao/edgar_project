from django.shortcuts import render
from .models import FundInfo, PositionInfo, SecurityInfo

# Create your views here.
def index(request):
    return render(request, 'index.html')

def graph(request):
    funds = FundInfo.objects.all()
    context={'funds': funds}
    return render(request, 'graph.html', context)


def test_alt(request):
    positions = PositionInfo.objects.count()
    context={'count': positions}
    return render(request, 'test_graph.html', context)


def dropdown(request):
    funds = FundInfo.objects.all().order_by('manager_name')
    context={'funds': funds}

    if request.method == "POST":
        selected_cik = int(request.POST.get('manager_dropdown'))
        positions = PositionInfo.objects.filter(cik=selected_cik)
        positions_with_security_info = positions.values('cusip__ticker', 'cusip__name', 'value', 'shares', 'filing_period').order_by('filing_period')
        context.update({'positions': positions_with_security_info, 'selected_cik': selected_cik})

    return render(request, 'dropdown.html', context)