#%%
from os.path import dirname, join
from bokeh.core.enums import Location, Orientation
from bokeh.io import show,curdoc
from bokeh.models.annotations import ColorBar
from bokeh.models.widgets import Tabs, Panel, widget
from bokeh.io.showing import show
from bokeh.models import CustomJS, Slider,ColumnDataSource,Label
from bokeh.models import Div
from bokeh.plotting import figure
from bokeh.util.compiler import TypeScript
import numpy as np
from numpy import linspace
from bokeh.layouts import column, layout, row
desc = Div(text=open(join(dirname(__file__), "descripcion.html")).read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "descripcion2.html")).read(), sizing_mode="stretch_width")

#%%
x=np.arange(-10,10,1)
y=np.arange(0,1,0.05)

source=ColumnDataSource(data=dict(x=x,y=y))
plot=figure(y_range=(-0.1,1.1),width=600,height=400)
plot.xaxis.axis_label = 'Utilidad B - Utilidad A'
plot.yaxis.axis_label = 'Probabilidad de elegir A'
plot.line('x','y',source=source,line_width=4,line_alpha=0.6,color="navy")
beta_slider=Slider(start=0,end=10,value=0,step=.1,title="Beta")
callback=CustomJS(args=dict(source=source),
code="""
const data=source.data;
const B= cb_obj.value;
const y=data['y'];


function softmax_choice(utilities,beta)
{
    let proba_A=Math.exp(utilities[0]*B)/(Math.exp(utilities[0]*B)+Math.exp(utilities[1]*B));
    return Math.random() < proba_A ? 0 : 1;
    
    ;
};

function range(start, stop, step)
{
    if (typeof stop == 'undefined')
    {
        stop = start;
        start = 0;
    }
    if (typeof step == 'undefined')
        step = 1;
    if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) 
        return [];
    var result = [];
    for (var i = start; step > 0 ? i < stop : i > stop; i += step)
        result.push(i);
    return result;
}

var utilities_list = []
for(i in range(20))
    utilities_list.push([i,10]);

var probabilities=[];
for(var i in range(utilities_list.length))
{
    var mean=0.0;
    var trials = 100;
    for (var trial in range(0,trials,1))
        mean += softmax_choice(utilities_list[i],B)
    mean /= trials;
    probabilities.push(1-mean);
    
}

//console.log(probabilities);

function softmax(utilities,beta)
{
    let probs=Math.exp(utilities[0]*B)/(Math.exp(utilities[0]*B)+Math.exp(utilities[1]*B));
    return probs;
}

var probs_A=[];
for (var i in range(utilities_list.length))
{
    //console.log(utilities_list[i]);
    probs_A.push(softmax(utilities_list[i],B));
    y[i]=probs_A[i];
    
}

source.change.emit();
""")

#%%
fig1 = plot
fig2=beta_slider
dumdiv1 = Div(text='  ', width=10)

l1 = layout([[row(desc2,dumdiv1),column(fig1, fig2)]], sizing_mode='scale_both')

tab1 = Panel(child=desc,title="Introducción")
tab2 = Panel(child=l1,title="Sobre el modelo")
tabs = Tabs(tabs=[ tab1, tab2])

beta_slider.js_on_change('value',callback)
   
show(tabs)

curdoc().add_root(tabs)

