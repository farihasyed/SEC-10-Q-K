from flask import Flask, url_for, render_template, redirect, request
import os
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from forms import Index
from tables import DataTable, main_table
from elements import Filing
import io
import base64

KEY = os.environ['API_KEY']
URL_ROOT = 'https://financialmodelingprep.com/api/v3/'
RESOURCE = 'financial-statement-full-as-reported/'
API_KEY = '?apikey=' + KEY
MILLIONS = 1000000

# example url https://financialmodelingprep.com/api/v3/financial-statement-full-as-reported/STOCK?apikey=KEY

INCOME_DATA_POINTS = {'Period Ending': 'date',
                      'Total Revenue': 'salesrevenuenet',
                      'Cost of Revenue': 'costofgoodsandservicessold',
                      'Gross Profit': 'grossprofit',
                      'Total Operational Expenses': 'operatingexpenses',
                      'Operating Income': 'operatingincomeloss',
                      'Income before Tax': 'incomelossfromcontinuingoperationsbeforeincometaxesextraordinaryitemsnoncontrollinginterest',
                      'Net Income': 'netincomeloss'}


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev')
    plt.switch_backend('Agg')
    return app


app = create_app()
if __name__ == "__main__":
    app.run()


def get_10k(stock):
    url = ''.join([URL_ROOT, RESOURCE, stock, API_KEY])
    response = requests.get(url)
    data = response.json()
    if response.status_code == requests.codes.ok:
        filings = [process_annual_filing(annual_filing) for annual_filing in data]
        years = [filing.period_ending for filing in filings]
        years = [year.split('-')[0] for year in years]
        revenues = [filing.total_revenue for filing in filings if filing.total_revenue != 'N/A']
        net_incomes = [filing.net_income for filing in filings if filing.net_income != 'N/A']
        years.reverse()
        net_incomes.reverse()
        revenues.reverse()
        plot = graph(years, net_incomes, revenues)
    # table = main_table(data_tables, years)
    table = DataTable(filings)
    return table, plot


def process_annual_filing(annual_filing):
    data = []
    for key in INCOME_DATA_POINTS.keys():
        if INCOME_DATA_POINTS[key] in annual_filing:
            value = annual_filing[INCOME_DATA_POINTS[key]]
            if key != 'Period Ending':
                value = int(float(value) / MILLIONS)
        else:
            if key == 'Total Revenue':
                for alternate_key in ['revenuefromcontractwithcustomerexcludingassessedtax', 'revenues']:
                    if alternate_key in annual_filing:
                        value = annual_filing[alternate_key]
                        value = int(float(value) / MILLIONS)
                        break;
            else:
                value = 'N/A'
        data.append(value)
    period_ending, total_revenue, revenue_cost, gross_profit, total_operational_expenses, operating_income, income_before_tax, net_income = data
    return Filing(period_ending, total_revenue, revenue_cost, gross_profit, total_operational_expenses, operating_income, income_before_tax, net_income)


def graph(years, net_incomes, revenues):
    plt.plot(years, net_incomes, label='Net Income')
    if len(revenues) == len(net_incomes):
        plt.plot(years, revenues, label='Revenue')
    plt.xlabel('Year')
    plt.legend(loc='lower right')
    plot_url = 'static/plots/plot.png'
    plt.savefig(plot_url)
    image = io.BytesIO()
    FigureCanvas(plt.gcf()).print_png(image)
    image_string = "data:image/png;base64,"
    image_string += base64.b64encode(image.getvalue()).decode('utf8')
    plt.clf()
    return image_string


@app.route('/')
def start():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    form = Index()
    if request.method == 'POST':
        return results(form.company.data)
    return render_template('index.html', form=form)


@app.route('/results', methods=['GET'])
def results(stock):
    table, plot = get_10k(stock)
    return render_template('results.html', stock=stock, table=table, plot=plot)







