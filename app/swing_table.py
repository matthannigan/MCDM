import pandas as pd
import seaborn
from bokeh.models import ColumnDataSource, DataTable, TableColumn, FactorRange, Legend, HoverTool, CategoricalTicker
from bokeh.plotting import figure
import os



def create_swing_table(filter_col=None):

    file_path = os.path.dirname(os.path.abspath(__file__))

    cb_color_map = {}


    cb_palette = seaborn.color_palette("Blues_r").as_hex()

    cb_palette = [cb_palette[0], cb_palette[-1]]

    cb_colors = ["high", "low"]

    for cp in cb_palette:
        cb_color_map.update({cb_colors[cb_palette.index(cp)]: cp})


    definitions = pd.read_excel(os.path.join(file_path, "data/Rubric.xlsx"), "Definitions")

    definitions["Definition"] = definitions["Definition"].str.replace("^\w+:\s+", "")
    # definitions["Definition"] = definitions["Definition"].str.replace("\n", "<br>")

    criteria = definitions["Criteria"].sort_values().drop_duplicates().tolist()


    for c in criteria:

        definitions.loc[definitions.Criteria == c, "scenario"] = "Scenario {}".format(criteria.index(c) + 1)

    swing_tuples = []

    for c in criteria:

        for c2 in criteria:

            if c == c2:

                swing_tuples.append((c, c2, "Excellent"))

            else:

                swing_tuples.append((c, c2, "Poor"))

    df_ex_poor = pd.DataFrame(swing_tuples, columns=["x", "y", "Score"])

    df_ex_poor.loc[df_ex_poor.Score == "Excellent", "cb_color"] = cb_color_map["high"]
    df_ex_poor.loc[df_ex_poor.Score == "Poor", "cb_color"] = cb_color_map["low"]

    df_ex_poor['x'] = pd.Categorical(df_ex_poor['x'], df_ex_poor["x"].drop_duplicates().tolist())
    df_ex_poor['y'] = pd.Categorical(df_ex_poor['y'], df_ex_poor["y"].drop_duplicates().tolist())

    df_ex_poor = df_ex_poor.merge(definitions[["Criteria", "Score", "Definition"]], left_on=["y", "Score"],
                                  right_on=["Criteria", "Score"], how="left")

    df_ex_poor = df_ex_poor.merge(definitions[["Criteria", "Score", "Definition"]], left_on=["x", "Score"],
                                  right_on=["Criteria", "Score"], how="left")

    df_ex_poor.rename(columns={"Definition_x": "Definition_row",
                               "Definition_y": "Definition_col"}, inplace=True)

    df_ex_poor.drop(["Criteria_y", "Criteria_x"], axis=1, inplace=True)

    df_ex_poor = df_ex_poor.merge(definitions[["Criteria", "scenario"]].drop_duplicates(), left_on="y", right_on="Criteria", how="left")

    if filter_col:

        df_ex_poor = df_ex_poor.loc[df_ex_poor.x.isin(filter_col)]

    y_range = FactorRange(factors=df_ex_poor["scenario"].drop_duplicates().tolist()[::-1])
    x_range = FactorRange(factors=df_ex_poor["x"].drop_duplicates().sort_values().tolist())

    df_ex = df_ex_poor.loc[df_ex_poor.Score == "Excellent"]
    df_poor = df_ex_poor.loc[df_ex_poor.Score == "Poor"]

    excellent_source = ColumnDataSource(data=dict(x=df_ex["x"].tolist(),
                                                  y=df_ex["scenario"].tolist(),
                                                  score=df_ex["Score"].tolist(),
                                                  cb_color=df_ex["cb_color"].tolist(),
                                                  definition_row=df_ex["Definition_row"].tolist(),
                                                  definition_col=df_ex["Definition_col"].tolist()))

    poor_source = ColumnDataSource(data=dict(x=df_poor["x"].tolist(),
                                             y=df_poor["scenario"].tolist(),
                                             score=df_poor["Score"].tolist(),
                                             cb_color=df_poor["cb_color"].tolist(),
                                             definition_row=df_poor["Definition_row"].tolist(),
                                             definition_col=df_poor["Definition_col"].tolist()))

    hover = HoverTool(tooltips=[("Definition", "@definition_col")])

    p = figure(y_range=y_range, x_range=x_range, plot_width=1700, plot_height=900, x_axis_location="above", tools=[hover, "save"])

    excellent = p.rect(x="x", y="y", color="cb_color", source=excellent_source, height=.90, width=.98)
    poor = p.rect(x="x", y="y", color="cb_color", source=poor_source, height=.90, width=.98)

    legend = Legend(items=[("Excellent", [excellent]),
                           ("Poor", [poor])])

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    p.xaxis.major_label_orientation = .85

    p.add_layout(legend, 'right')

    return p