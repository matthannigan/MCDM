import pandas as pd
import seaborn
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, FactorRange, Legend, HoverTool


palette = seaborn.color_palette("RdYlGn").as_hex()
palette = [palette[0], palette[round(len(palette)/2)], palette[-1]]

cb_palette = seaborn.color_palette("Blues_r").as_hex()
cb_palette = [cb_palette[0], cb_palette[round(len(cb_palette)/2)], cb_palette[-1]]

colors = ["red", "yellow", "green"]
cb_colors = ["high", "medium", "low"]
color_map = {}
cb_color_map = {}

for p in palette:
    color_map.update({colors[palette.index(p)]: p})

for cp in cb_palette:
    cb_color_map.update({cb_colors[cb_palette.index(cp)]: cp})


df = pd.read_excel("/home/matt/GitRepos/systems/data/Rubric.xlsx", "Rubric v3")
df = df[["Criteria", "Atlas.ti", "Dedoose", "MAXQDA", "NVivo", "Transana", "TOM", "QDA Miner"]]

definitions = pd.read_excel("/home/matt/GitRepos/systems/data/Rubric.xlsx", "Definitions")

definitions["Definition"].fillna("", inplace=True)

df = df.melt(id_vars=["Criteria"], var_name="Tool", value_name="Score")
df = df.merge(definitions, how="left", on=["Criteria", "Score"])

df.loc[df.Score == "Excellent", "color"] = color_map["green"]
df.loc[df.Score == "Good", "color"] = color_map["yellow"]
df.loc[df.Score == "Poor", "color"] = color_map["red"]

df.loc[df.Score == "Excellent", "cb_color"] = cb_color_map["high"]
df.loc[df.Score == "Good", "cb_color"] = cb_color_map["medium"]
df.loc[df.Score == "Poor", "cb_color"] = cb_color_map["low"]

df['Score'] = pd.Categorical(df['Score'], ["Excellent", "Good", "Poor"])
df['Tool'] = pd.Categorical(df['Tool'], ["NVivo", "Dedoose", "QDA Miner", "Atlas.ti", "Transana", "TOM", "MAXQDA"])

df_excellent = df.loc[df.Score == "Excellent"]
df_fair = df.loc[df.Score == "Good"]
df_poor = df.loc[df.Score == "Poor"]


y_range = FactorRange(factors=df["Criteria"].drop_duplicates().tolist()[::-1])
x_range = FactorRange(factors=df["Tool"].drop_duplicates().tolist())


excellent_source = ColumnDataSource(data=dict(criteria=df_excellent["Criteria"].tolist(),
                                              tool=df_excellent["Tool"].tolist(),
                                              score=df_excellent["Score"].tolist(),
                                              color=df_excellent["color"].tolist(),
                                              cb_color=df_excellent["cb_color"].tolist(),
                                              desc=df_excellent["Definition"].tolist()))

fair_source = ColumnDataSource(data=dict(criteria=df_fair["Criteria"].tolist(), tool=df_fair["Tool"].tolist(),
                                         score=df_fair["Score"].tolist(), color=df_fair["color"].tolist(),
                                         cb_color=df_fair["cb_color"].tolist(), desc=df_fair["Definition"].tolist()))

poor_source = ColumnDataSource(data=dict(criteria=df_poor["Criteria"].tolist(), tool=df_poor["Tool"].tolist(),
                                         score=df_poor["Score"].tolist(), color=df_poor["color"].tolist(),
                                         cb_color=df_poor["cb_color"].tolist(), desc=df_poor["Definition"].tolist()))

hover = HoverTool(tooltips=[("description", "@desc")])

p = figure(y_range=y_range, x_range=x_range, plot_width=1900, plot_height=900, x_axis_location="above", tools=[hover, "save"])

p.xaxis.major_label_text_font_size = "15pt"
p.yaxis.major_label_text_font_size = "15pt"

excellent = p.rect(x="tool", y="criteria", color="cb_color", height=1, width=.96, source=excellent_source,
                   line_color="cb_color", alpha=.75)

fair = p.rect(x="tool", y="criteria", color="cb_color", height=1, width=.96, source=fair_source,
              line_color="cb_color", alpha=.75)

poor = p.rect(x="tool", y="criteria", color="cb_color", height=1, width=.96, source=poor_source,
              line_color="cb_color", alpha=.75)

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

p.xaxis.major_label_orientation = .85

legend = Legend(items=[("Excellent", [excellent]),
                       ("Good", [fair]),
                       ("Poor", [poor])])

# legend.label_text_font = "opensans"

# p.xaxis[0].major_label_text_font = "opensans"
# p.yaxis[0].major_label_text_font = "opensans"

legend.label_text_font_size = "15pt"
p.add_layout(legend, 'right')

