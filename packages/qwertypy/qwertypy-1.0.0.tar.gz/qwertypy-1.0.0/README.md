# qwertypy

Python utilities library for financial utilities, data analysis, visualization and DSA.

## Quick links

-   [Github](https://github.com/qwertyvipul/qwertypy)
-   [PyPI](https://pypi.org/project/qwertypy)
-   [Docs](https://qwertyvipul.io/qwertypy/#usage)

## Installation

```bash
pip install qwertypy
```

### Upgrade

```bash
pip install --upgrade qwertypy
```

## Usage

-   Try on colab: [Click here](https://colab.research.google.com/drive/1SK96YfBgIPY-CKNfvQxvBKkJnNA7fSCe?usp=sharing)

### `qwertypy.greetings`

```py
import qwertypy.greetings as qpyGreetings

print(qpyGreetings.hello())
```

### `qwertypy.tickertape`

#### `qwertypy.tickertape.companies`

```py
import qwertypy.tickertape.companies as ttCompanies

topCompanies = ttCompanies.getTopCompanies()
print("TOP = ", len(topCompanies))
# print("ALL = ", len(ttCompanies.getAllCompanies()))

ttName = "reliance-industries-RELI"
companyInfo = ttCompanies.getCompanyInfo(ttName)
print(companyInfo)
```

#### `qwertypy.tickertape.financials`

```py
import qwertypy.tickertape.financials as ttFinancials

ttName = "reliance-industries-RELI"
for statementType in ttFinancials.statementTypes:
    statement = ttFinancials.getStatement(ttName, statementType)
    print(statementType, type(statement))

ttName = "reliance-industries-RELI"
statementType = ttFinancials.statementTypes["income"]
statement = ttFinancials.getStatement(ttName, statementType)
yearsAndValues = ttFinancials.getYearsAndValues(statement, "incDps")
print(yearsAndValues)
```

### `qwertypy.data_analysis`

#### `qwertypy.data_analysis.regression`

```py
import qwertypy.data_analysis.regression as qpyRegression

xTrain = [1, 2, 3, 4, 5, 6]
yTrain = [2, 4, 6, 8, 10, 12]
model = qpyRegression.QpyLinearRegression(xTrain, yTrain)
model.train()
yPredict = model.getPrediction()
print("yPredict: ", yPredict)

xPredict2 = [10, 11]
yExpected = [20, 22]
yPredict2 = model.getPrediction(xPredict2)
print("yPredict2: ", yPredict2)
```

### `qwertypy.data_plots`

#### `qwertypy.data_plots.trend_plot`

```py
import random

import qwertypy.data_plots.trend_plot as qpyTrendPlot

xValues = [i for i in range(10)]
yValues = [random.randint(1, 10) for _ in range(10)]
xTicks = ["xTick" + str(i+1) for i in range(10)]
trendValues = list(yValues)
qpyTrendPlot.trendPlot(
    xValues, yValues,
    xTicks = xTicks,
    rotateXTicks = 90,
    xLabel = "xLabel",
    yLabel = "yLabel",
    plotTitle = "plotTitle",
    trendValues = trendValues,
    legends = ["trendLegend", "barLegend"],
    text = "text",
    textBackground = "red",
    watermark = "watermark",
    showValues = True,
    # saveToFile = "testImage.jpg"
)
```

### `qwertypy.dsa`

#### `qwertypy.dsa.single_source_shortest_path`

```py
from collections import defaultdict

from qwertypy.dsa.single_source_shortest_path import dijkstra

n = 9
edges = [
    (0, 1, 4),
    (0, 7, 8),
    (1, 7, 11),
    (1, 2, 8),
    (7, 8, 7),
    (7, 6, 1),
    (2, 8, 2),
    (8, 6, 6),
    (2, 3, 7),
    (2, 5, 4),
    (6, 5, 2),
    (3, 5, 14),
    (3, 4, 9),
    (5, 4, 10)
]

graph = defaultdict(lambda: defaultdict(int))
for u, v, d in edges:
    graph[u][v] = graph[v][u] = d

print(dijkstra(graph, 0, n))
print(dijkstra(graph, 1, n))
```

#### `qwertypy.dsa.all_pairs_shortest_path`

```py
from collections import defaultdict

from qwertypy.dsa.all_pairs_shortest_path import fw

edges = [
    [1, 2, 3],
    [1, 4, 7],
    [2, 1, 8],
    [2, 3, 2],
    [3, 1, 5],
    [3, 4, 1],
    [4, 1, 2]
]
graph = defaultdict(dict)
for u, v, cost in edges:
    graph[u-1][v-1] = cost
fw(graph, len(graph))
```

#### `qwertypy.dsa.strongly_connected_components`

```py
from collections import defaultdict

from qwertypy.dsa.strongly_connected_components import tarjan

edges = [[0,1],[2,0],[1,3],[3,4],[4,5],[5,6],[6,4]]
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)

low = tarjan(graph)
print("low: ", low)

scc = defaultdict(list)
for key in low:
    scc[low[key]].append(key)

print("Strongly connected components: ", list(scc.values()))

bridges = []
for u, v in edges:
    if scc[u] != scc[v]:
        bridges.append([u, v])

print("Bridges: ", bridges)
```
