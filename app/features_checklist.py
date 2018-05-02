import pandas as pd
import seaborn
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, FactorRange, CategoricalAxis, HoverTool

from numpy import nan
import os

file_path = os.path.dirname(os.path.abspath(__file__))

palette = seaborn.color_palette("GnBu", 2).as_hex()*10

df = pd.read_excel(os.path.join(file_path, "data/Refined Features checklist.xlsx"), "refined")

categories = df[["Category", "Features", "Definition"]]

unique_categories = df["Category"].drop_duplicates().tolist()


# df = df[["Features", "NVivo", "Dedoose", "QDA Miner", "Atlas.ti", "Transana", "TOM", "MAXQDA"]]

df.drop(["Definition", "Category"], inplace=True, axis=1)

df.dropna(axis=1, how="all", inplace=True)

tool_list = df.columns.tolist()[1:]

df = df.loc[~df.Features.isnull()]

df = df.melt(id_vars=["Features"], var_name=["Tool"])

df['Tool'] = pd.Categorical(df['Tool'], tool_list)
df["Features"] = pd.Categorical(df["Features"], df["Features"].drop_duplicates(keep="first").tolist())

df["value"].replace(0, nan, inplace=True)

df = df.loc[~df.value.isnull()]

categories = categories[["Features", "Category", "Definition"]]

df = df.merge(categories, how="left", on=["Features"])
y_range = FactorRange(factors=[i for i in df.sort_values(by="Category")[["Category", "Features"]].drop_duplicates().values.tolist()[::-1]])
x_range = FactorRange(factors=df["Tool"].drop_duplicates().tolist())


choose_color = 0
for c in df.sort_values(by="Category")["Category"].drop_duplicates().tolist():

    df.loc[df.Category == c, "color"] = palette[choose_color]
    choose_color += 1

source = ColumnDataSource(data=dict(tool=df["Tool"].tolist(), feature=df[["Category", "Features"]].values.tolist(),
                                    color=df["color"].tolist(), category=df["Category"].tolist(),
                                    desc=df["Definition"].tolist()))

hover = HoverTool(tooltips=[("Tool", "@tool"),
                            ("Feature Definition", "@desc")])

p = figure(x_range=x_range, y_range=y_range, plot_height=7500, plot_width=1500, x_axis_location="above", tools=[hover])


p.circle(x="tool", y="feature", color="black", source=source, size=35)

p.add_layout(CategoricalAxis(), 'below')

p.xaxis.major_label_text_font_size = "12pt"
p.yaxis.major_label_text_font_size = "12pt"