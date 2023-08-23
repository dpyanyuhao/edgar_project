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
    funds = FundInfo.objects.order_by('manager_name')
    context={'funds': funds}

    if request.method == "POST":
        selected_cik = int(request.POST.get('manager_dropdown'))
        positions = PositionInfo.objects.filter(cik=selected_cik)
        positions_with_security_info = positions.values('cusip__ticker', 'cusip__name', 'cusip__sector', 'value', 'shares', 'filing_period').order_by('filing_period')
        context.update({'positions': positions_with_security_info, 'selected_cik': selected_cik})

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

        # Find the 'cusip__name' with the greatest total value
        max_cusip = df.groupby('cusip__name')['value'].sum().idxmax()

        # Loop through traces (lines) of the figure and set visibility
        # for trace in fig.data:
        #     if trace.name != max_cusip:
        #         trace.visible = 'legendonly'

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

        import plotly.express as px
        import pandas as pd

        df = pd.DataFrame(positions_with_security_info)
        df['filing_period'] = pd.to_datetime(df['filing_period'], format='%d-%b-%Y')
        # print(df['filing_period'].unique())

        fig = px.area(df, 
              x="filing_period", 
              y="value", 
              color="cusip__name"
              )
        
        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(hovermode="x")

        # Find the 'cusip__name' with the greatest total value
        max_cusip = df.groupby('cusip__name')['value'].sum().idxmax()

        # Loop through traces (lines) of the figure and set visibility
        for trace in fig.data:
            if trace.name != max_cusip:
                trace.visible = 'legendonly'

        plot = fig.to_html(full_html=False, default_height=500, default_width=800)
        context.update({'plot': plot})

     return render(request, 'landing.html', context)