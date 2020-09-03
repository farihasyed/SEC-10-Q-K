from flask_table import Table, Col, DateCol, create_table


def main_table(data, years):
    options = dict(classes=['table', 'table-hover'], thead_classes=['thead-light'], no_items='N/A')
    TableCls = create_table(options=options)
    for year in years:
        TableCls.add_column(str(year), DateCol(year))
    table = TableCls(data)
    return table


class DataTable(Table):
    # th_html_attrs = {'data-show-header': 'false'}
    # classes = ['table', 'table-sm', 'table-borderless']
    classes = ['table', 'table-hover']
    thead_classes = ['thead-light']
    no_items = 'N/A'
    period_ending = Col('Period Ending')
    total_revenue = Col('Total Revenue')
    revenue_cost = Col('Cost of Revenue')
    gross_profit = Col('Gross Profit')
    total_operational_expenses = Col('Total Operational Expenses')
    operating_income = Col('Operating Income')
    income_before_tax = Col('Income before Tax')
    net_income = Col('Net Income')


