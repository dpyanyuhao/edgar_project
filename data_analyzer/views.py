from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
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
    funds = FundInfo.objects.order_by('manager_name')
    context={'funds': funds}

    if request.method == "POST":
        selected_cik = int(request.POST.get('manager_dropdown'))
        positions = PositionInfo.objects.filter(cik=selected_cik)
        positions_with_security_info = positions.values('cusip__ticker', 'cusip__name', 'cusip__sector', 'value', 'shares', 'filing_period').order_by('filing_period')
        context.update({'positions': positions_with_security_info, 'selected_cik': selected_cik})

        unique_cusip_names = sorted(set([position['cusip__name'] for position in positions_with_security_info]))
        context.update({'unique_cusip_names': unique_cusip_names})

        import plotly.express as px
        import pandas as pd

        df = pd.DataFrame(positions_with_security_info)
        df = df.sort_values('cusip__name')
        fig = px.area(df, 
              x="filing_period", 
              y="value", 
              color="cusip__name"
              )
        
        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(hovermode="x")
        fig.update_layout(
            xaxis_title="Period",
            yaxis_title="Total Value",
            legend_title_text="Holdings"
        )
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all", label="All")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )

        
        fig.update_layout(
            updatemenus=[
                dict(
                    type='buttons',
                    showactive=False,
                    x=1.3,
                    y=-0.1,
                    buttons=[
                        dict(label='Show All',
                            method='restyle',
                            args=['visible', [True for trace in fig.data]]),
                        dict(label='Hide All',
                            method='restyle',
                            args=['visible', ['legendonly' for trace in fig.data]])
                    ]
                )
            ]
        )

        plot = fig.to_html(full_html=False, default_height=500, default_width=800)
        context.update({'plot': plot})

    return render(request, 'dropdown.html', context)


def landing(request):
    funds = FundInfo.objects.order_by('manager_name')
    context={'funds': funds}

    if request.method == "POST":
        selected_cik = int(request.POST.get('manager_dropdown'))
        positions = PositionInfo.objects.filter(cik=selected_cik)
        positions_with_security_info = positions.values('cusip__ticker', 'cusip__name', 'cusip__sector', 'value', 'shares', 'filing_period').order_by('filing_period')
        context.update({'positions': positions_with_security_info, 'selected_cik': selected_cik})

        unique_cusip_names = sorted(set([position['cusip__name'] for position in positions_with_security_info]))
        context.update({'unique_cusip_names': unique_cusip_names})

        import plotly.express as px
        import pandas as pd

        df = pd.DataFrame(positions_with_security_info)
        df = df.sort_values('cusip__name')
        fig = px.area(df, 
              x="filing_period", 
              y="value", 
              color="cusip__name"
              )
        
        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(hovermode="x")
        fig.update_layout(
            xaxis_title="Period",
            yaxis_title="Total Value",
            legend_title_text="Holdings"
        )
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all", label="All")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )

        
        fig.update_layout(
            updatemenus=[
                dict(
                    type='buttons',
                    showactive=False,
                    x=1.3,
                    y=-0.1,
                    buttons=[
                        dict(label='Show All',
                            method='restyle',
                            args=['visible', [True for trace in fig.data]]),
                        dict(label='Hide All',
                            method='restyle',
                            args=['visible', ['legendonly' for trace in fig.data]])
                    ]
                )
            ]
        )

        plot = fig.to_html(full_html=False, default_height=500, default_width=800)
        context.update({'plot': plot})

        # Place code for sector exposure here


    return render(request, 'landing.html', context)


def get_filtered_positions(request):
    cusip_name = request.GET.get('cusip_name')
    cik = int(request.GET.get('cik'))

    filtered_positions = PositionInfo.objects.filter(cik=cik, cusip__name=cusip_name)
    table_html = render_to_string('positions_table.html', {'positions': filtered_positions})

    return JsonResponse({'table': table_html})


def application_one(request):
    funds = FundInfo.objects.all().order_by('manager_name')
    return render(request, 'application_one.html', {'funds': funds})


def get_time_intervals(request):
    cik = int(request.GET.get('cik'))
    intervals = PositionInfo.objects.filter(cik=cik).values_list('filing_period', flat=True).distinct().order_by('filing_period')
    return JsonResponse({'intervals': list(intervals)})


def get_cik_and_time(request):
    from datetime import datetime
    # 1. Extract parameters from the request
    cik = int(request.GET.get('cik'))
    time = request.GET.get('time')

    # Convert the 'time' string to a datetime object
    time_as_date = datetime.strptime(time, '%Y-%m-%d').date()

    # 2. Retrieve data for the given cik and time
    current_positions = PositionInfo.objects.filter(cik=cik, filing_period=time_as_date)
    prev_quarter_date = PositionInfo.objects.filter(cik=cik, filing_period__lt=time).latest('filing_period').filing_period
    previous_positions = PositionInfo.objects.filter(cik=cik, filing_period=prev_quarter_date)

    # Convert previous_positions to a dictionary for easier lookup
    prev_data = {pos.cusip_id: pos for pos in previous_positions}

    results = []

    # 3. Calculate changes and 4. Prepare data
    for pos in current_positions:
        ticker = pos.cusip.ticker
        stock_name = pos.cusip.name
        value = pos.value
        shares = pos.shares
        prev_shares = prev_data.get(pos.cusip_id).shares if pos.cusip_id in prev_data else 0
        change_in_shares = shares - prev_shares
        percent_change = round((shares - prev_shares) / prev_shares * 100, 2) if prev_shares != 0 else 0
        percent_of_company = round((value / sum([p.value for p in current_positions])) * 100, 2)

        results.append({
            'stock_name': stock_name,
            'ticker': ticker,
            'value': value,
            'shares': shares,
            '% change in shares': percent_change,
            'absolute change in shares': change_in_shares,
            '% of company': percent_of_company
        })
    
    # Sorting results by '% of company' in descending order
    sorted_results = sorted(results, key=lambda x: x['% of company'], reverse=True)

    # 5. Send the data
    return JsonResponse({'data': sorted_results})

