import pandas as pd
from Arules import Arules
from DataAnalyzerUtil import DataAnalyzerUtil
from Utils import export_html, draw_scatter_plot_for_rules


def main():
    file_name = '../raw/dataset.csv'
    draw_charts(file_name)

    generate_top_frequent_items_sets_and_rules(file_name=file_name,
                                               max_count=10,
                                               min_support=0.001,
                                               min_confidence=0.001,
                                               min_lift=1,
                                               sort_by='lift')

    generate_and_export_and_draw_rules(file_name=file_name,
                                       min_support=0.001,
                                       min_confidence=0.5,
                                       min_lift=3,
                                       sort_by='support')


def draw_charts(file_name):
    analyzer = DataAnalyzerUtil(file_name)
    # Bar Charts
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='all', reducer='head', chart_type='bar')
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='all', reducer='tail', chart_type='bar')
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='big', reducer='head', chart_type='bar')
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='big', reducer='tail', chart_type='bar')
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='small', reducer='head', chart_type='bar')
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='small', reducer='tail', chart_type='bar')

    # Tree Map
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='all', reducer='head', chart_type='tree_map')
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='all', reducer='tail', chart_type='tree_map')
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='big', reducer='head', chart_type='tree_map')
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='big', reducer='tail', chart_type='tree_map')
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='small', reducer='head', chart_type='tree_map')
    analyzer.draw_chart_for_bags_items(max_count=20, bag_type='small', reducer='tail', chart_type='tree_map')


def generate_top_frequent_items_sets_and_rules(file_name, max_count, min_support, min_confidence, min_lift, sort_by):
    rules_generator = Arules(file_name=file_name)
    sorted_data = sorted(rules_generator.get_frequent_item_sets(min_support), key=lambda fi: fi.support, reverse=True)
    top = [fi for fi in sorted_data if len(fi.items) > 1][0:max_count]
    top_ten_frequent_header = f"""\t\t<h1 style="text-align: center;">Top {max_count} Frequent Item Set</h3>
        \t\t<p style="text-align: center;">Frequent Item Set Count: {len(top)}</p>
        \t\t<p style="text-align: center;">Minimum Support: {min_support}</p>"""
    export_html(pd.DataFrame(data=top), '../out/top_ten_frequent_item_set.html', top_ten_frequent_header)

    rules_data_frame = rules_generator.get_arules(frequent_item_sets=top,
                                                  min_confidence=min_confidence,
                                                  min_lift=min_lift,
                                                  sort_by=sort_by)
    rules_count = len(rules_data_frame)
    header = f"""\t\t<h2 style="text-align: center;">Association Rules Of Top {max_count} Frequent Item Set</h3>
        \t\t<p style="text-align: center;">Rules Count: {rules_count}</p>
        \t\t<p style="text-align: center;">Minimum Support: {min_support}</p>
        \t\t<p style="text-align: center;">Minimum Confidence: {min_confidence}</p>
        \t\t<p style="text-align: center;">Minimum Lift: {min_lift}</p>
        \t\t<p style="text-align: center;">Sorted By: {sort_by}</p>
        """
    export_html(rules_data_frame, '../out/top_ten_rules.html', header)
    title = f"Association Rules Bubble Chart Of Top {max_count} Frequent Item Set: Rules Count: {rules_count} / " \
            f"Minimum Support: {min_support} / Minimum Confidence: {min_confidence} / Minimum Lift: {min_lift}"
    draw_scatter_plot_for_rules(rules_data_frame, title)


def generate_and_export_and_draw_rules(file_name, min_support, min_confidence, min_lift, sort_by):
    rules_generator = Arules(file_name=file_name)
    frequent_item_sets = rules_generator.get_frequent_item_sets(min_support)
    rules_data_frame = rules_generator.get_arules(
        frequent_item_sets=frequent_item_sets,
        min_confidence=min_confidence,
        min_lift=min_lift,
        sort_by=sort_by
    )

    rules_count = len(rules_data_frame)
    header = f"""\t\t<h2 style="text-align: center;">Association Rules</h3>
    \t\t<p style="text-align: center;">Rules Count: {rules_count}</p>
    \t\t<p style="text-align: center;">Minimum Support: {min_support}</p>
    \t\t<p style="text-align: center;">Minimum Confidence: {min_confidence}</p>
    \t\t<p style="text-align: center;">Minimum Lift: {min_lift}</p>
    \t\t<p style="text-align: center;">Sorted By: {sort_by}</p>
    """

    title = f"Association Rules Bubble Chart: Rules Count: {rules_count} / Minimum Support: {min_support} / " \
            f"Minimum Confidence: {min_confidence} / Minimum Lift: {min_lift}"
    export_html(rules_data_frame, '../out/index.html', header)
    draw_scatter_plot_for_rules(rules_data_frame, title)


if __name__ == '__main__':
    main()
