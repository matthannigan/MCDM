from bokeh.models import ColumnDataSource, Paragraph
from bokeh.layouts import widgetbox, layout


p_width = 500
header_font_size = 21
p_font_size = 12

open = Paragraph(text="Instructions for Decision Tool", width=p_width, style={"font-size": "{}pt".format(header_font_size)})

p1 = Paragraph(text="This tool will help you determine which of your criteria is most important and which decision will "
                    "best meet those criteria. There are 3 parts to this tool. First is the rubric, second is the "
                    "features checklist, and third is the multicriteria decision making model (MCDM).", width=p_width,
               style={"font-size": "{}pt".format(p_font_size)})

h1 = Paragraph(text="Rubric", width=p_width, style={"font-size": "{}pt".format(header_font_size)})

p2 = Paragraph(text="The rubric shows and defines the criteria used in your model. Each criteria is graded on a scale "
                    "from excellent to poor. Hover over each box to show see the definition of each grade. This is "
                    "intended to allow users to see the variation of each tools across your criteria and make "
                    "comparisons across all tools easy.", width=p_width,
               style={"font-size": "{}pt".format(p_font_size)})

h2 = Paragraph(text="Features Checklist", width=p_width, style={"font-size": "{}pt".format(header_font_size)})

p3 = Paragraph(text="The features checklist shows a detailed list of the features for each tool you are comparing. "
                    "Again, hover over the dots to see the feature definition.", width=p_width,
               style={"font-size": "{}pt".format(p_font_size)})

h3 = Paragraph(text="Features Checklist", width=p_width, style={"font-size": "{}pt".format(header_font_size)})

p4 = Paragraph(text="The MCDM helps you make your final decision regarding which tool you should use. To use this "
                    "tab follow these instructions:", width=p_width, style={"font-size": "{}pt".format(p_font_size)})

p5 = Paragraph(text="1) Choose the subset of criteria that are most important to you from the box. Click 'Submit "
                    "Criteria' when you have finished.", width=p_width, style={"font-size": "{}pt".format(p_font_size)})

p6 = Paragraph(text="2) Rank each criteria you selected with a unique number. Lower numbers mean that the criteria "
                    "is more important. Be sure to pay attention to the Swing Weighting Matrix on the bottom of the "
                    "page. This will help you define each criteria if you hover over the boxes. Click 'Calculate "
                    "Ranks' when you have finished.", width=p_width, style={"font-size": "{}pt".format(p_font_size)})

p7 = Paragraph(text="3) Use the sliders that appear to tell the tool how important that criterion is relative to "
                    "the others you have selected. The criteria you rank 1st will have a weight of 1 and this cannot "
                    "be changed. The remaining criteria will be given a default weight that you should alter. You "
                    "should weight each criteria so that it reflects how important that criterion is to you should you "
                    "ONLY be able to have the best outcome for that criterion but the worst in every other criteria. "
                    "Please refer to the Swing Weighting Matrix for the definitions of best and worst for each "
                    "criterion. The weights will be between 0 and 1. Click 'Update Model' when finished.",
               width=p_width, style={"font-size": "{}pt".format(p_font_size)})
p8 = Paragraph(text="4) A new table will appear with the tools ranks from best to worst with their final scores. "
                    "Use this to make your decision.", width=p_width, style={"font-size": "{}pt".format(p_font_size)})

app_layout = layout([open,
                     p1,
                     h1,
                     p2,
                     h2,
                     p3,
                     h3,
                     p4,
                     p5,
                     p6,
                     p7,
                     p8])