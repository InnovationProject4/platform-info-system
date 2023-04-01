import utils.chart as chart
import tkinter as tk
import random

root = tk.Tk()

def simple_chart():
    '''
    chart shows fresh data with line and old data gets hidden on big scale
    '''
    datachart = chart.LineChart(root, width=800, height=400, hbar_size=10, vbar_size=10,
                       hbar_fg="#101010", vbar_fg="#444444", sections_fg="#444444", 
                       text_color="#00ff00", font=('arial', 10, 'bold'),
                       sections=True, sections_count=50, max_value=2000000,
                       labels=True, labels_count=50, line_len=100,
                       left=10, right=10, bottom=40, top=40,
                       x=0, y=10
                       )
    datachart.pack()
    line = chart.Line(parent=datachart,height=4, color='blue')

    values = [x for x in range(2000000)]

    def loop():
        datachart.render(line=line, values=random.choices(values, k=1))
        root.after(500, loop)
    loop()

    root.mainloop()
    


def s_chart():
    datachart = chart.LineChart(root, width=600, height=400, hbar_size=5, vbar_size=5,
                       hbar_fg="#101010", vbar_fg="#444444", sections_fg="#444444", 
                       text_color="red", font=('arial', 8, 'bold'),
                       sections=True, sections_count=10, max_value=100,
                       labels=True, labels_count=10, line_len=20,
                       left=10, right=10, bottom=40, top=40,
                       x=0, y=0
                       )
    datachart.pack(fill=tk.BOTH, expand=True)
    line = chart.Line(parent=datachart,height=3, color='blue')

    values = [10, 5, 20, 30, 40, 50, 10, 20, 30, 40, 90, 10, 100]

    datachart.render(line=line, values=values)
   

    root.mainloop()
    


s_chart()