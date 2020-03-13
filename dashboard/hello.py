# hello.py

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models.widgets import TextInput, Button, Paragraph

# create some widgets
button = Button(label="Say HI")
button2 = Button(label="Another button")
input = TextInput(value="Bokeh")
output = Paragraph()

# add a callback to a widget
def update():
    output.text = "Hello, " + input.value

button.on_click(update)
button2.on_click(update)

# create a layout for everything
layout = column(button, input, output, button2)

# add the layout to curdoc
curdoc().add_root(layout)
