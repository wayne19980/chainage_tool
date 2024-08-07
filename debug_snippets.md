# debug_snippets
## get features
``` python
features = iface.activeLayer().getFeatures()
>>features
#<qgis._core.QgsFeatureIterator object at 0x0000024D0B267F50>

for i in features:
 print (i)

<qgis._core.QgsFeature object at 0x0000024D0B267E30>

layer = iface.activeLayer()
fid = 1
iterator = layer.getFeatures(QgsFeatureRequest().setFilterFid(fid))
feature = next(iterator)
attrs = feature.attributes()
attrs
"""
[1, 1, '江安路', -180.0, 503.5, 100.0, 771.166653667316]
"""

print(attrs[1])
"""
1
"""
feature["name"]
"""
'江安路'
"""
in1 = "name"
feature[in1]
"""
'江安路'
"""
```