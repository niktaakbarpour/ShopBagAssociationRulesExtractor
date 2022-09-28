import matplotlib.pyplot as plt
import numpy as np
from Utils import list2series, csv2list
import squarify
from statistics import mean


class DataAnalyzerUtil:
    def __init__(self, file_name):
        self.transactions_list = csv2list(file_name)

    def get_average_of_item_count_in_each_transaction(self):
        return mean(len(t) for t in self.transactions_list)

    def get_small_bags_items(self, indicator):
        return (items for items in self.transactions_list if len(items) < indicator)

    def get_big_bags_items(self, indicator):
        return (items for items in self.transactions_list if len(items) > indicator)

    def divide_transaction_by_item_count(self, indicator):
        small_bag = []
        big_bag = []
        for transaction in self.transactions_list:
            if len(transaction) > indicator:
                big_bag.append(transaction)
            else:
                small_bag.append(transaction)
        return small_bag, big_bag

    def draw_chart_for_bags_items(self, max_count, bag_type='all', reducer='head', chart_type='bar'):
        average = self.get_average_of_item_count_in_each_transaction()
        if bag_type == 'big':
            bag_items = self.get_big_bags_items(average)
            bag_title = 'Big'
        elif bag_type == 'small':
            bag_items = self.get_small_bags_items(average)
            bag_title = 'Small'
        else:
            bag_items = self.transactions_list
            bag_title = 'All'

        items = list2series(bag_items).value_counts()
        if reducer == 'tail':
            items = items.tail(max_count)
            count_title = 'Least'
        else:
            items = items.head(max_count)
            count_title = 'Most'

        if chart_type == 'tree_map':
            self.draw_tree_map(items, f'Tree Map Of Top {max_count} {count_title} Frequent Items In {bag_title} Bags')
        elif chart_type == 'bar':
            self.draw_bar_chart(items, f'Bar Chart Of Top {max_count} {count_title} Frequent Items In {bag_title} Bags',
                                'Count', 'Items')

    @staticmethod
    def draw_bar_chart(items, title, y_label, x_label):
        color = plt.cm.inferno(np.linspace(0, 1, len(items)))
        items.plot.bar(color=color)
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.title(title)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.show()

    @staticmethod
    def draw_tree_map(items, title):
        plt.rcParams['figure.figsize'] = (10, 10)
        size = items.values
        label = items.index
        color = plt.cm.inferno(np.linspace(0, 1, len(items)))
        squarify.plot(sizes=size, label=label, alpha=0.7, color=color)
        plt.title(title)
        plt.axis('off')
        plt.show()
