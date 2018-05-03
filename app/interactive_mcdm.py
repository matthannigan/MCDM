import pandas as pd
from bokeh.plotting import figure, show, curdoc
from bokeh.layouts import widgetbox, layout, row, column
from bokeh.models import ColumnDataSource, Button, Slider, Dropdown, PreText, DataTable, TableColumn, MultiSelect, NumberFormatter, CustomJS
from collections import OrderedDict, Counter
import numpy as np

from functools import partial

import swing_table

import os

doc = curdoc()

file_path = os.path.dirname(os.path.abspath(__file__))


class MCDMModel:

    def __init__(self):

        self.rubric = pd.read_excel(os.path.join(file_path, "data/Rubric.xlsx"), "Rubric v3")

        try:

            self.rubric.drop(["Category", "Definition", "Grading Scale"], inplace=True, axis=1)

        except KeyError:

            pass

        self.criteria = self.rubric["Criteria"].drop_duplicates().tolist()

        self.swing_table = swing_table.create_swing_table()

        self.chosen_criteria = []

        self.criteria_selection = MultiSelect(title="Choose Criteria:", size=10)
        self.choose_criteria()

        self.rubric_values = self.rubric.replace("Excellent", 1.0)
        self.rubric_values.replace("Good", 0.5, inplace=True)
        self.rubric_values.replace("Poor", 0, inplace=True)

        self.rubric_values = self.rubric_values.melt(id_vars=["Criteria"], var_name=["Tool"], value_name="Score")

        self.weight_sliders = OrderedDict()
        self.ranking = OrderedDict()

        self.b = Button(label="Update Model", button_type="primary")
        self.b.on_click(self.submit_callback)

        self.criteria_b = Button(label="Submit Criteria", button_type="primary")
        self.criteria_b.on_click(self.choose_criteria_callback)

        self.rank_submit = Button(label="Calculate Ranks", button_type="primary")
        self.rank_submit.on_click(self.submit_ranks)

        self.source = ColumnDataSource()

        self.data_table = DataTable

        self.app_layout = layout()

    def choose_criteria(self):

        self.criteria_selection.options = self.rubric["Criteria"].drop_duplicates().tolist()

    def choose_criteria_callback(self):

        self.chosen_criteria = []

        self.chosen_criteria = self.criteria_selection.value

        if len(self.chosen_criteria) > 0:

            self.ranking = OrderedDict()
            self.rank_criteria()

            self.swing_table = swing_table.create_swing_table(self.chosen_criteria)

            try:
                self.app_layout.children.pop(1)
            except IndexError:

                pass

            self.app_layout.children.append(layout([[self.swing_table],
                                                    *[self.ranking[k] for k in self.ranking.keys()],
                                                    [self.rank_submit]]))

    def rank_criteria(self):

        for c in sorted(self.chosen_criteria):

            self.ranking.update({c: [PreText(text="Scenario {}".format(sorted(self.criteria).index(c) + 1)),
                                     Dropdown(menu=[(str(i), str(i)) for i in range(1, len(self.chosen_criteria) + 1)],
                                              button_type="primary", label="Rank")]})

        for k in self.ranking.keys():

            self.ranking[k][1].on_change("value", partial(self.ranking_label_callback, k=k))

    def weight_calc(self):

        for c in self.chosen_criteria:

            self.weight_sliders.update({c: Slider(start=0, end=1, step=.01, title=c, id=c,
                                                  value=1/len(self.chosen_criteria))})

        self.weight_sliders[self.chosen_criteria[0]].disabled = True
        self.weight_sliders[self.chosen_criteria[0]].value = 1

        for w in self.weight_sliders.keys():

            self.weight_sliders[w].on_change("value", partial(self.weight_callback, c=w))

    def ranking_label_callback(self, attr, old, new, k):

        self.ranking[k][1].label = new

        if self.ranking[k][1].button_type == "danger":

            print("test")

            self.ranking[k][1].button_type = "primary"

            try:
                self.ranking[k].pop(-1)

                self.app_layout.children.pop(1)

                self.app_layout.children.append(layout([[self.swing_table],
                                                        *[self.ranking[k] for k in self.ranking.keys()],
                                                        [self.rank_submit]]))

            except IndexError:

                pass

    def submit_ranks(self):

        self.weight_sliders = OrderedDict()

        ranks = []

        for k in self.chosen_criteria:

            if not self.ranking[k][1].value:

                self.ranking[k][1].button_type = "danger"

                self.ranking[k].append(PreText(text="Please enter a rank for all chosen criteria"))

                self.app_layout.children.pop(1)

                self.app_layout.children.append(layout([[self.swing_table],
                                                        *[self.ranking[k] for k in self.ranking.keys()],
                                                       [self.rank_submit]]))

            else:

                ranks.append(self.ranking[k][1].value)

        if len(ranks) == len(self.ranking.keys()):

            if len(ranks) != len(list(set(ranks))):

                dup_values = []

                for crit, count in Counter(ranks).items():

                    if count > 1:

                        dup_values.append(crit)

                for k in self.ranking.keys():

                    if self.ranking[k][1].value in dup_values:

                        self.ranking[k][1].button_type = "danger"

                        self.ranking[k].append(PreText(text="Please enter unique ranks for each criteria"))

                self.app_layout.children.pop(1)

                self.app_layout.children.append(layout([[self.swing_table],
                                                        *[self.ranking[k] for k in self.ranking.keys()],
                                                        [self.rank_submit]]))

            else:

                for k in self.ranking.keys():

                    self.ranking[k][1].button_type = "primary"

                temp_list = []

                for r in np.argsort(ranks):

                    temp_list.append(self.chosen_criteria[r])

                self.chosen_criteria = temp_list

                self.add_weight_changes()

    def weight_callback(self, attr, old, new, c):

        next_index = self.chosen_criteria.index(c) + 1
        prev_index = self.chosen_criteria.index(c) - 1

        if next_index != len(self.chosen_criteria):

            if self.weight_sliders[self.chosen_criteria[next_index]].value > new:
                self.weight_sliders[self.chosen_criteria[next_index]].value = new

        if prev_index != 0:

            if self.weight_sliders[self.chosen_criteria[prev_index]].value < new:
                self.weight_sliders[self.chosen_criteria[prev_index]].value = new

    def submit_callback(self):

        total_weight = sum([self.weight_sliders[s].value for s in self.weight_sliders.keys()])

        normed_weights = []

        for w in self.weight_sliders.keys():

            normed_weights.append((w, self.weight_sliders[w].value/total_weight))

        weights_df = pd.DataFrame(normed_weights, columns=["Criteria", "Normed_Weights"])

        rubric_calc = self.rubric_values.merge(weights_df, on=["Criteria"])

        rubric_calc["WeightedScore"] = rubric_calc["Score"] * rubric_calc["Normed_Weights"]

        values = rubric_calc[["Tool", "WeightedScore"]].groupby(["Tool"]).sum().reset_index()

        values.sort_values(by="WeightedScore", inplace=True, ascending=False)
        values["Rank"] = values.rank(method="dense", numeric_only=True, ascending=False)

        self.source = ColumnDataSource()

        self.source.data.update({"tool": values["Tool"].tolist(), "score": values["WeightedScore"],
                                 "rank": values["Rank"].tolist()})

        self.add_rank_table()

    def start_model(self):

        self.app_layout = layout([[self.criteria_selection, self.criteria_b]])

        self.app_layout.children.append(layout(self.swing_table))

        return self.app_layout

    def add_weight_changes(self):

        self.weight_calc()

        buttons = zip([self.ranking[k][0] for k in self.chosen_criteria],
                      [self.ranking[k][1] for k in self.chosen_criteria],
                      [self.weight_sliders[k] for k in self.weight_sliders.keys()])
        b_layout = [[t[0], t[1], t[2]] for t in buttons]
        b_layout.append([self.rank_submit, self.b])
        b_layout.insert(0, [self.swing_table])

        self.app_layout.children.pop(1)

        self.app_layout.children.append(layout(b_layout))

    def add_rank_table(self):

        columns = [TableColumn(field="tool", title="Tool"),
                   TableColumn(field="score", title="Weighted Score", formatter=NumberFormatter(format="0.00")),
                   TableColumn(field="rank", title="Rank")]

        self.data_table = DataTable(columns=columns, source=self.source, reorderable=True)

        buttons = zip([self.ranking[k][0] for k in self.chosen_criteria],
                      [self.ranking[k][1] for k in self.chosen_criteria],
                      [self.weight_sliders[k] for k in self.weight_sliders.keys()])

        self.app_layout.children.pop(1)

        b_layout = [[t[0], t[1], t[2]] for t in buttons]

        b_layout.append([self.rank_submit, self.b])
        b_layout.append(widgetbox(self.data_table))
        self.app_layout.children.append(layout(b_layout))


mcdm = MCDMModel()
app_layout = mcdm.start_model()
