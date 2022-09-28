import pandas as pd
import plotly.graph_objects as go


def csv2list(file_name, header=None):
    dataset = pd.read_csv(file_name, header=header)
    row, col = dataset.shape
    transactions = []
    for i in range(row):
        items = []
        for j in range(col):
            item = dataset.values[i, j]
            if not pd.isna(item):
                items.append(str(item).lower())
        transactions.append(items)
    return transactions


def list2map(m_list):
    m_map = {}
    for index in range(len(m_list)):
        for item in m_list[index]:
            if item not in m_map:
                m_map[item] = set()
            m_map[item].add(index)
    return m_map


def list2series(m_list):
    return pd.concat([pd.Series(item) for item in m_list], ignore_index=True)


def export_html(rules, path, header=''):
    def get_table_row(row, index='', is_head=False):
        if is_head:
            tag = 'th'
            row_cells = f'\n\t\t\t\t<th>#</th>'
        else:
            tag = 'td'
            row_cells = f'\n\t\t\t\t<td>{index}</td>'
        for cell in row:
            if type(cell) == set or type(cell) == frozenset:
                formatted_text = ', '.join(cell)
            else:
                formatted_text = str(cell)
            row_cells += f'\n\t\t\t\t<{tag}>{formatted_text}</{tag}>'
        return f'\n\t\t\t<tr>{row_cells}\n\t\t\t</tr>'

    def get_table(items):
        head = get_table_row(row=items.columns, is_head=True)
        rows = head
        for index, row in items.iterrows():
            rows += get_table_row(row=row, index=str(index + 1))
        return f'\t\t<table>{rows}\n\t\t</table>'

    html = """
<!DOCTYPE html>
<html>
    <head>
        <title></title>
        <meta content="">
        <style>
            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 15px;
                text-align: left;
            }
            tr:nth-child(odd) {
                background-color: #eee;
            }
            tr:nth-child(even) {
                background-color: #fff;
            }
            th {
                text-transform:uppercase;
                background-color: #c7c7c7;
            }
        </style>
    </head>
    <body>
"""
    html += header
    html += get_table(items=rules)
    html += "\n\t</body>\n</html>"

    file = open(path, 'w')
    file.write(html)


def draw_scatter_plot_for_rules(rules, title):
    def get_text_for_rule(item):
        return ('Left: {left}<br>' +
                'Right: {right}<br>' +
                'Left Support: {left_support}<br>' +
                'Right Support: {right_support}<br>' +
                'Support: {support}<br>' +
                'Confidence: {confidence}<br>' +
                'Lift: {lift}<br>').format(left=', '.join(item.left),
                                           right=', '.join(item.right),
                                           left_support=item.left_support,
                                           right_support=item.right_support,
                                           support=item.support,
                                           confidence=item.confidence,
                                           lift=item.lift)

    hover_text = [get_text_for_rule(rule) for rule in rules.itertuples()]
    size_ref = 2. * max(rules['lift']) / (10 ** 2)
    fig = go.Figure(
        data=[go.Scatter(x=rules['support'], y=rules['confidence'], text=hover_text, mode='markers', marker=dict(
            color=rules['lift'],
            size=rules['lift'],
            showscale=True,
            sizeref=size_ref
        ))])

    fig.update_layout(
        title=title,
        xaxis=dict(
            title='Support',
            gridcolor='white',
            type='log',
            gridwidth=2,
        ),
        yaxis=dict(
            title='Confidence',
            gridcolor='white',
            gridwidth=2,
        )
    )
    fig.show()
