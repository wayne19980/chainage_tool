# -*- coding: utf-8 -*-

"""
/***************************************************************************
 ChainageTool
                                 A QGIS plugin
 This tool provides utility to convert line to chainage points.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-07-25
        copyright            : (C) 2024 by Wayne
        email                : wayne.hu2007@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = "Wayne"
__date__ = "2024-07-25"
__copyright__ = "(C) 2024 by Wayne"

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = "$Format:%H$"

"""
Import Note
需要添加和删除属性需要导入QVariant->3.38之后的版本替换成QMetaType
可能会需要：
QgsVectorLayer, QgsField, QgsFeature, QgsGeometry,QgsPointXY, QgsProject
import pandas as pd
from math import radians, degrees, floor, ceil
"""

from qgis.PyQt.QtCore import QCoreApplication, QVariant, QMetaType
from qgis.core import (
    QgsProcessing,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSink,
    QgsGeometry,
    QgsField,
    QgsFields,
    Qgis,
    QgsMessageLog,
)
from math import ceil
import copy


class ChainageToolAddField(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = "OUTPUT"
    INPUT = "INPUT"

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output layer"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(parameters, self.INPUT, context)
        # define fields
        custom_fields = source.fields()
        # fields.append( QgsField(name="id", type=QVariant.Int))
        custom_fields.append(QgsField("line_id", QMetaType.Type.Int if Qgis.QGIS_VERSION_INT > 33800 else QVariant.Int))
        custom_fields.append(QgsField("start_mileage", QMetaType.Type.Double if Qgis.QGIS_VERSION_INT > 33800 else QVariant.Double))
        custom_fields.append(QgsField("end_mileage", QMetaType.Type.Double if Qgis.QGIS_VERSION_INT > 33800 else QVariant.Double))
        custom_fields.append(QgsField("distance", QMetaType.Type.Double if Qgis.QGIS_VERSION_INT > 33800 else QVariant.Double))
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            custom_fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()

        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            # 处理开始
            # 1. Loop through line features, get Nth feature (geom + props)
            # geom = feature.geometry()
            # attrs = feature.attributes()
            # geom_type = geom.wkbType()
            sink.addFeature(feature, QgsFeatureSink.FastInsert)

            # 5. Update Progress.
            # Update the progress bar
            feedback.setProgress(int(current * total))

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "Init layer fields"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "Vector Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ChainageToolAddField()


class ChainageToolAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT = "OUTPUT"
    INPUT = "INPUT"
    ID = "ID"
    DISTANCE = "DISTANCE"
    START_MILEAGE = "START_MILEAGE"
    END_MILEAGE = "END_MILEAGE"

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        所有的输入和输出都在这里定义,self.tr()中的字符串是名字.
        # TODO: if field name is standard, fill in window straightaway(should be in init?)
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input layer"),
                [QgsProcessing.TypeVectorAnyGeometry],
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.ID,
                self.tr("Select identifier field"),
                None,
                self.INPUT,
                QgsProcessingParameterField.DataType.Any,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.START_MILEAGE,
                self.tr("Select start mileage field"),
                None,
                self.INPUT,
                QgsProcessingParameterField.DataType.Any,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.END_MILEAGE,
                self.tr("Select end mileage field"),
                None,
                self.INPUT,
                QgsProcessingParameterField.DataType.Any,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.DISTANCE,
                self.tr("Select interpolation distance field"),
                None,
                self.INPUT,
                QgsProcessingParameterField.DataType.Any,
                optional=True,
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr("Output layer"))
        )

    def processAlgorithm(self, parameters, context, feedback):
        def interpolate_by_vmileage(
            vStart,
            vEnd,
            vDis,
            geom,
            fid,
            sr_attrs,
            # force,
        ):
            """
            Creating Points at coordinates along the line
            """
            reverse = vEnd < vStart
            if reverse:
                # Extract the coordinates from the original geometry
                coords = geom.asPolyline()

                # Reverse the order of the points (QgsPointXY objects)
                reversed_coords = coords[::-1]

                # Create a new QgsGeometry with the reversed coordinates
                geom = QgsGeometry.fromPolylineXY(reversed_coords)

                vStart, vEnd = vEnd, vStart
                
            # don't allow distance to be zero and loop endlessly
            # 如果间距为负，设为线段长
            vLength = vEnd - vStart
            print()
            vDis = abs(vDis)
            
            if vDis > vLength or vDis == 0:
                    vDis = vLength

            length = geom.length()
            print()
            lengthRatio = length / vLength
            dis = vDis * lengthRatio
            print("vStart:", vStart, "vEnd:", vEnd, "vLength:", vLength, "vDis:", vDis, "dis:", dis, "length:", length)

            QgsMessageLog.logMessage(f"vStart {vStart}, vEnd {vEnd},vLength {vLength},vDis {vDis},dis {dis},length {length}", "Chainage Tools",0)
            """
                # 如果终点长>总长，设为总长
                if length < vEnd:
                    vEnd = length
                # 如果等分有值，复制一份length2，如果起终点有值，再减去
                if divide > 0:
                    length2 = length
                    if vStart > 0:
                        length2 = length - vStart
                    if vEnd > 0:
                        length2 = vEnd
                    if vStart > 0 and vEnd > 0:
                        length2 = vEnd - vStart  # length-(length-endpoint)-startpoint
                    vDis = length2 / divide
                    dis = vDis
                else:
                    dis = vDis

                if vEnd > 0:
                    length = vEnd
                """

            feats = []

            # # define fields
            # fields = QgsFields()
            # # fields.append( QgsField(name="id", type=QVariant.Int))
            # fields.append(QgsField("line_id", QMetaType.Type.Int if Qgis.QGIS_VERSION_INT > 33800 else QVariant.Int))
            # fields.append(QgsField("mileage_value", QMetaType.Type.Double if Qgis.QGIS_VERSION_INT > 33800 else QVariant.Double))
            # fields.append(QgsField("dist", QMetaType.Type.Double if Qgis.QGIS_VERSION_INT > 33800 else QVariant.Double))

            def add_interpolate_custom(geom, length, mileage_value, id):
                # Get a point along the line at the current distance
                point = geom.interpolate(length)
                # Create a new QgsFeature and assign it the new geometry
                feature = QgsFeature(custom_fields)
                feature.setGeometry(point)
                tem_attrs=copy.copy(sr_attrs)
                tem_attrs.extend([mileage_value,length])
                feature.setAttributes(tem_attrs)
                # feature["dist"] = length
                # feature["mileage_value"] = mileage_value
                # feature["line_id"] = id
                feats.append(feature)

            current_dis = 0
            current_mileage = vStart

            if current_mileage != ceil(vStart / vDis) * vDis:
                add_interpolate_custom(geom, current_dis, current_mileage, fid)
                current_mileage = ceil(vStart / vDis) * vDis
                current_dis = (ceil(vStart / vDis) * vDis - vStart) * lengthRatio
                ##不对的，忘记比例换算了

            while (
                current_mileage
                < vEnd
                # current_dis + dis < length
            ):  # 条件：当下一个点还在范围内（先用老办法，按道理这样会避免最后一个点进去）
                add_interpolate_custom(geom, current_dis, current_mileage, fid)
                # Increase the distance
                current_dis += dis
                current_mileage += vDis

            # set the last point at endpoint
            end = geom.length()
            add_interpolate_custom(geom, end, vEnd, fid)
            return feats

        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        source = self.parameterAsSource(parameters, self.INPUT, context)
        # define fields
        custom_fields = source.fields()
        # fields.append( QgsField(name="id", type=QVariant.Int))
        # custom_fields.append(QgsField("line_id", QMetaType.Type.Int if Qgis.QGIS_VERSION_INT > 33800 else QVariant.Int))
        custom_fields.append(QgsField("mileage_value", QMetaType.Type.Double if Qgis.QGIS_VERSION_INT > 33800 else QVariant.Double))
        custom_fields.append(QgsField("dist", QMetaType.Type.Double if Qgis.QGIS_VERSION_INT > 33800 else QVariant.Double))
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            custom_fields,
            Qgis.WkbType(1),
            source.sourceCrs(),
        )

        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / source.featureCount() if source.featureCount() else 0
        features = source.getFeatures()

        for current, feature in enumerate(features):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break
            # 处理开始
            # TODO: 如果是三维线，转成二维，因为桩号不考虑高程
            # 1. Loop through line features, get Nth feature (geom + props)
            geom = feature.geometry()
            attrs = feature.attributes()
            geom_type = geom.wkbType()
            # Pass looping if feature is not polyline
            if geom_type != 2:
                pass
            # else:
            # 2. vLength = eM - sM = IN4 - IN3; vD = IN5;<-get from attrs[field input]
            sM = feature[parameters[self.START_MILEAGE]]
            eM = feature[parameters[self.END_MILEAGE]]
            vD = feature[parameters[self.DISTANCE]]
            id = feature[parameters[self.ID]]

            # 3. ~~Generate list of fraction of total length (0-1);~~
            # Generate point array directly and add to sink
            frac_list = interpolate_by_vmileage(
                vStart=sM,
                vEnd=eM,
                vDis=vD,
                geom=geom,
                fid=id,
                sr_attrs=attrs,
            )
            # 4. Interpolate point on line on $Length \* fraction; Add line props to points, return and add to feature sink;

            for i in frac_list:
                # Add a feature in the sink
                sink.addFeature(i, QgsFeatureSink.FastInsert)

            # 5. Update Progress.
            # Update the progress bar
            feedback.setProgress(int(current * total))

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "Line interpolate equidistant points"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "Vector Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return ChainageToolAlgorithm()
