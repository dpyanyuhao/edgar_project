from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import FundInfo, PositionInfo, SecurityInfo
import plotly.express as px
import pandas as pd

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


def get_position_change_table(request):
    from datetime import datetime
    # 1. Extract parameters from the request
    cik = int(request.GET.get('cik'))
    start_time = request.GET.get('start time')
    end_time = request.GET.get('end time')

    # Convert the 'time' string to a datetime object
    start_date = datetime.strptime(start_time, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_time, '%Y-%m-%d').date()

    # 2. Retrieve data for the given cik and time
    current_positions = PositionInfo.objects.filter(cik=cik, filing_period=start_date)
    previous_positions = PositionInfo.objects.filter(cik=cik, filing_period=end_date)

    # Convert both previous_positions and current_positions to dictionaries for easier lookup
    prev_data = {pos.cusip_id: pos for pos in previous_positions}
    current_data = {pos.cusip_id: pos for pos in current_positions}

    results = []

    # 3. Calculate changes and 4. Prepare data
    for pos in current_positions:
        ticker = pos.cusip.ticker
        stock_name = pos.cusip.name
        value = pos.value
        shares = pos.shares
        prev_shares = prev_data.get(pos.cusip_id).shares if pos.cusip_id in prev_data else 0
        change_in_shares = shares - prev_shares
        percent_change = round((shares - prev_shares) / prev_shares * 100, 2) if prev_shares != 0 else "NEW"
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
    
    for pos in previous_positions:
        if pos.cusip_id not in current_data:
            ticker = pos.cusip.ticker
            stock_name = pos.cusip.name
            prev_shares = pos.shares

            # These positions were sold, so their current value, shares, and % of company are 0
            results.append({
                'stock_name': stock_name,
                'ticker': ticker,
                'value': 0,
                'shares': 0,
                '% change in shares': -100,  # Because it was sold
                'absolute change in shares': -prev_shares,  # Negative of previous shares
                '% of company': 0
            })
    
    # Sorting results by '% of company' in descending order
    sorted_results = sorted(results, key=lambda x: x['% of company'], reverse=True)

    # 5. Send the data
    return JsonResponse({'data': sorted_results})


def get_fund_holdings_plot(request):
    cik = int(request.GET.get('cik'))
    positions = PositionInfo.objects.filter(cik=cik)
    positions_with_security_info = positions.values('cusip__ticker', 'cusip__name', 'cusip__sector', 'value', 'shares', 'filing_period').order_by('filing_period')

    df = pd.DataFrame(positions_with_security_info)
    df = df.sort_values('cusip__name')
    fig = px.area(df, x="filing_period", y="value", color="cusip__name")
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
    return JsonResponse({"plot": plot})


def get_sector_exposure_plot(request):
    cik = int(request.GET.get('cik'))
    positions = PositionInfo.objects.filter(cik=cik)
    positions_with_security_info = positions.values('cusip__ticker', 'cusip__name', 'cusip__sector', 'value', 'shares', 'filing_period').order_by('filing_period')

    # Convert the queryset to a DataFrame
    df = pd.DataFrame(positions_with_security_info)

    # Aggregate value by cusip__sector and filing_period
    aggregated = df.groupby(['cusip__sector', 'filing_period'])['value'].sum().reset_index()

    # Compute the total value for each filing_period
    total_per_period = aggregated.groupby('filing_period')['value'].sum().reset_index()
    total_per_period = total_per_period.rename(columns={'value': 'total_value'})

    # Merge the aggregated and total_per_period DataFrames to compute percentages
    merged = pd.merge(aggregated, total_per_period, on='filing_period')
    merged['percentage'] = (merged['value'] / merged['total_value']) * 100
    merged['percentage_text'] = merged['percentage'].apply(lambda x: f"{x:.2f}%")
    # Sort the merged dataframe based on the 'cusip__sector' column
    merged = merged.sort_values(by='cusip__sector')

    fig = px.bar(merged, 
                 y="filing_period", 
                 x="percentage", 
                 color="cusip__sector", 
                 orientation="h",
                 title="Sector Exposure by Filing Period",
                 hover_data={"cusip__sector": True,
                             "percentage": False,
                             "percentage_text": True,
                             "filing_period": True},
                 labels={'cusip__sector': 'Sector',
                         'percentage_text': 'Weight',
                         'filing_period': 'Period'}
              )
    
    fig.update_layout(
        xaxis_title="% of holdings",
        yaxis_title="Filing Period",
        legend_title_text="Sector"
        )
    
    # Set the stacking mode
    fig.update_layout(barmode='stack')
    plot = fig.to_html(full_html=False, default_height=500, default_width=800)
    return JsonResponse({"plot": plot})

def get_dollar_notional_plot(request):
    cusip = request.GET.get('cusip')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    positions = PositionInfo.objects.filter(
        cusip=cusip,
        filing_period__range =[start_time, end_time]
    ).order_by('filing_period')
   
   # Create a DataFrame for easier calculations
    df = pd.DataFrame.from_queryset(positions)

    # Compute total value and total shares at each filing_period
    data_points = df.groupby('filing_period').agg({'value': 'sum', 'shares': 'sum'}).reset_index()

    # Compute the $ notional bought/sold
    data_points['price'] = data_points['value']/data_points['shares']
    data_points['delta_shares'] = data_points['shares'].diff().fillna(0)
    data_points['notional'] = data_points['delta_shares'] * data_points['price']

    # Plot using Plotly Express
    fig = px.line(data_points, x='filing_period', y='notional', title="$ Notional Bought/Sold over Period")
    plot_html = fig.to_html()

    return JsonResponse({'plot_html': plot_html})




