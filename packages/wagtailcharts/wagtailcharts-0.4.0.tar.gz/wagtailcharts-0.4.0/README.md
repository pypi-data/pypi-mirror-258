# Wagtail Charts
Chart.js charts in Wagtail, edited and customised from the Wagtail admin

## Getting started

Assuming you have a Wagtail project up and running:

`pip install wagtailcharts`

Add `wagtailcharts` to your settings.py in the INSTALLED_APPS section, before the core wagtail packages:

```python
INSTALLED_APPS = [
    # ...
    'wagtailcharts',
    # ...
]
```

Add a wagtailcharts ChartBlock to one of your StreamFields:

```python
from wagtailcharts.blocks import ChartBlock

class ContentBlocks(StreamBlock):
    chart_block = ChartBlock()
```

Include your streamblock in one of your pages

```python
class HomePage(Page):
    body = StreamField(ContentBlocks())

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
```

Add the `wagtailcharts_tags` templatetag to your template and call the `render_charts` tag just before your `</body>` closing tag.
Please note that you must render your chart block so that the `render_charts` tag can detect the charts.
Here is a tiny example of a page rendering template:

```django
{% load wagtailcore_tags wagtailcharts_tags %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-6">
            <h1>{{self.title}}</h1>
            <div class="excerpt">{{self.excerpt|richtext}}</div>
        </div>
    </div>
    {% for block in self.body %}
        {% include_block block %}
    {% endfor %}
</div>
{% endblock %}

{% block extra_js %}
{% render_charts %}
{% endblock %}
```

## Configuration

`ChartBlock` accepts a few extra arguments in addition to the standard `StructBlock` arguments.

### `colors`
A tuple of color tuples defining the available colors in the editor.

```python
from wagtailcharts.blocks import ChartBlock

COLORS = (
    ('#ff0000', 'Red'),
    ('#00ff00', 'Green'),
    ('#0000ff', 'Blue'),
)

class ContentBlocks(StreamBlock):
    chart_block = ChartBlock(colors=COLORS)
```

### `chart_types`

You can override the default chart types available for your `ChartBlock` instance:

```python
from wagtailcharts.blocks import ChartBlock

CHART_TYPES = (
    ('line', 'Custom title for line chart'),
)

class ContentBlocks(StreamBlock):
    chart_block = ChartBlock(chart_types=CHART_TYPES)
```

The default types are:

```python
CHART_TYPES = (
    ('line', 'Line Chart'),
    ('bar', 'Vertical Bar Chart'),
    ('bar_horizontal', 'Horizontal Bar Chart'),
    ('area', 'Area Chart'),
    ('multi', 'Combo Line/Bar/Area Chart'),
    ('pie', 'Pie Chart'),
    ('doughnut', 'Doughnut Chart'),
    ('radar', 'Radar Chart'),
    ('polar', 'Polar Chart'),
    ('waterfall', 'Waterfall Chart')
)
```


## Dependencies
* This project relies on [Jspreadsheet Community Edition](https://bossanova.uk/jspreadsheet/v4/) for data entry and manipulation. 
* Charts are rendered using [Chart.js](https://www.chartjs.org/). 
* 100% stacked bar charts use a plugin [https://github.com/y-takey/chartjs-plugin-stacked100](https://github.com/y-takey/chartjs-plugin-stacked100)
* Datalabels use a plugin [https://chartjs-plugin-datalabels.netlify.app] (https://chartjs-plugin-datalabels.netlify.app)


# Release notes

## Version 0.3.3
* Fixed a regression from release 0.3.3 when using multiple charts on same page.

## Version 0.3.2
* Added support for external HTML legend
* Fixed bug in doughnut chart

## Version 0.3.1
* Added options for border width and border color for pie charts
* Added support for Wagtail 5
* Removed support for Wagtail <3

## Version 0.3
* Added Waterfall Chart
* Added DataLabels
* Added options for:
  * grid display
  * axis display
  * y tick precision
  * datalabel and tooltip precision
* Added grouping of options into multiple collapsible panels with buttons
* Multiple bugfixes

## Version 0.2
* Added support for Wagtail 3.0

## Version 0.1
* Initial release
