import matplotlib
matplotlib.use('Agg')
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import show, curdoc
from bokeh.layouts import layout
import rubric
import interactive_mcdm
import features_checklist
import instructions
# import swing_table

doc = curdoc()

doc.title = "Decision Making Model"

rubric = rubric.p
mcdm = interactive_mcdm.app_layout
features = features_checklist.p
instr = instructions.app_layout
# swing = swing_table.swing_table


instr_tab = Panel(child=instr, title="Instructions")
tab1 = Panel(child=rubric, title="Rubric")
tab2 = Panel(child=features, title="Features Checklist")
tab3 = Panel(child=mcdm, title="MCDM")

tabs = Tabs(tabs=[instr_tab, tab1, tab2, tab3], width=400)#, tab4])


app_layout = layout([tabs])
doc.add_root(app_layout)
