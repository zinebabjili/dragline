import math

from PyQt5.QtWidgets import QWidget

from PyQt5.QtGui import QPolygon, QPolygonF, QColor, QPen, QFont
from PyQt5.QtGui import QPainter, QFontMetrics, QConicalGradient

from PyQt5.QtCore import Qt, QTime, QTimer, QPoint, QPointF, QRect, QSize
from PyQt5.QtCore import QObject, pyqtSignal


class AnalogGaugeWidget(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(AnalogGaugeWidget, self).__init__(parent)

        self.use_timer_event = False

        self.value_min = 0
        self.value_max = 110
        self.value = self.value_min
        self.value_needle_snapzone = 0.05
        self.last_value = 0

        self.needle_scale_factor = 0.5

        self.set_NeedleColor(50, 50, 50, 255)
        self.set_NeedleColorDrag(255, 0, 00, 255)

        self.set_ScaleValueColor(50, 50, 50, 255)
        self.set_DisplayValueColor(50, 50, 50, 255)

        self.set_CenterPointColor(50, 50, 50, 255)
        self.scala_main_count = 10

        # self.value_needle = QObject

        self.change_value_needle_style([QPolygon([
            QPoint(4, 4),
            QPoint(-4, 4),
            QPoint(-3, -120),
            QPoint(0, -126),
            QPoint(3, -120)
        ])])

        self.scale_angle_start_value = 135
        self.scale_angle_size = 270

        self.scala_subdiv_count = 5

        self.pen = QPen(QColor(0, 0, 0))
        self.font = QFont('Decorative', 20)

        self.set_enable_ScaleText(True)

        self.scale_fontname = "Decorative"
        self.initial_scale_fontsize = 15
        self.scale_fontsize = self.initial_scale_fontsize

        # initialize Main value text
        self.value_fontname = "Decorative"
        self.initial_value_fontsize = 40
        self.value_fontsize = self.initial_value_fontsize

        self.set_enable_filled_Polygon(True)

        self.enable_CenterPoint = True
        self.enable_fine_scaled_marker = True
        self.enable_big_scaled_marker = True

        self.enable_Needle_Polygon = True

        self.rescale_method()

    def rescale_method(self):
        # print("slotMethod")
        if self.width() <= self.height():
            self.widget_diameter = self.width()
        else:
            self.widget_diameter = self.height()

        self.change_value_needle_style([QPolygon([
            QPoint(4, 30),
            QPoint(-4, 30),
            QPoint(-2, - self.widget_diameter / 2 * self.needle_scale_factor),
            QPoint(0, - self.widget_diameter / 2 * self.needle_scale_factor - 6),
            QPoint(2, - self.widget_diameter / 2 * self.needle_scale_factor)
        ])])

        self.scale_fontsize = self.initial_scale_fontsize * self.widget_diameter / 400
        self.value_fontsize = self.initial_value_fontsize * self.widget_diameter / 400

        pass

    def change_value_needle_style(self, design):
        # prepared for multiple needle instrument
        self.value_needle = []
        for i in design:
            self.value_needle.append(i)

    def update_value(self, value):
        if value <= self.value_min:
            self.value = self.value_min
        elif value >= self.value_max:
            self.value = self.value_max
        else:
            self.value = value
        # self.paintEvent("")
        self.valueChanged.emit(int(value))
        # print(self.value)

        # ohne timer: aktiviere self.update()
        if not self.use_timer_event:
            self.update()

    def diff_value(self, value):
        self.var = 100 - value
        return self.var

    ###############################################################################################
    # Set Methods
    ###############################################################################################
    def set_NeedleColor(self, R, G, B, Transparency):
        self.NeedleColor = QColor(R, G, B, Transparency)
        self.NeedleColorReleased = self.NeedleColor

        if not self.use_timer_event:
            self.update()

    def set_NeedleColorDrag(self, R, G, B, Transparency):
        self.NeedleColorDrag = QColor(R, G, B, Transparency)

        if not self.use_timer_event:
            self.update()

    def set_ScaleValueColor(self, R, G, B, Transparency):
        self.ScaleValueColor = QColor(R, G, B, Transparency)

    def set_DisplayValueColor(self, R, G, B, Transparency):
        self.DisplayValueColor = QColor(R, G, B, Transparency)

    def set_CenterPointColor(self, R, G, B, Transparency):
        self.CenterPointColor = QColor(R, G, B, Transparency)

    def set_enable_ScaleText(self, enable=True):
        self.enable_scale_text = enable

        if not self.use_timer_event:
            self.update()

    def set_enable_filled_Polygon(self, enable=True):
        self.enable_filled_Polygon = enable

    ###############################################################################################
    # Scale Marker
    ###############################################################################################

    # for big scales
    def draw_big_scaled_markter(self):
        my_painter = QPainter(self)
        my_painter.setRenderHint(QPainter.Antialiasing)

        my_painter.translate(self.width() / 2, self.height() / 2)

        self.pen = QPen(QColor(0, 0, 0, 255))
        self.pen.setWidth(2)

        my_painter.setPen(self.pen)

        # POUR NE PAS VOIR LES SCALES EN BAS
        my_painter.rotate(self.scale_angle_start_value)
        steps_size = (float(self.scale_angle_size) / float(self.scala_main_count))
        scale_line_outer_start = self.widget_diameter / 2
        scale_line_lenght = (self.widget_diameter / 2) - (self.widget_diameter / 20)

        for i in range(self.scala_main_count + 1):
            my_painter.drawLine(scale_line_lenght, 0, scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def create_scale_marker_values_text(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        font = QFont(self.scale_fontname, self.scale_fontsize)
        fm = QFontMetrics(font)

        pen_shadow = QPen()

        pen_shadow.setBrush(self.ScaleValueColor)
        painter.setPen(pen_shadow)

        text_radius_factor = 0.8
        text_radius = self.widget_diameter / 2 * text_radius_factor

        scale_per_div = int((self.value_max - self.value_min) / self.scala_main_count)

        angle_distance = (float(self.scale_angle_size) / float(self.scala_main_count))
        for i in range(self.scala_main_count + 1):
            # text = str(int((self.value_max - self.value_min) / self.scala_main_count * i))
            text = str(int(self.value_min + scale_per_div * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scale_fontname, self.scale_fontsize))
            angle = angle_distance * i + float(self.scale_angle_start_value)
            x = text_radius * math.cos(math.radians(angle))
            y = text_radius * math.sin(math.radians(angle))
            # print(w, h, x, y, text)
            text = [x - int(w / 2), y - int(h / 2), int(w), int(h), Qt.AlignCenter, text]
            painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])
        # painter.restore()

    def create_fine_scaled_marker(self):
        #  Description_dict = 0
        my_painter = QPainter(self)

        my_painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        my_painter.translate(self.width() / 2, self.height() / 2)

        my_painter.setPen(Qt.black)
        my_painter.rotate(self.scale_angle_start_value)
        steps_size = (float(self.scale_angle_size) / float(self.scala_main_count * self.scala_subdiv_count))
        scale_line_outer_start = self.widget_diameter / 2
        scale_line_lenght = (self.widget_diameter / 2) - (self.widget_diameter / 40)
        for i in range((self.scala_main_count * self.scala_subdiv_count) + 1):
            my_painter.drawLine(scale_line_lenght, 0, scale_line_outer_start, 0)
            my_painter.rotate(steps_size)

    def draw_big_needle_center_point(self, diameter=30):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)

        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        # painter.setPen(Qt.NoPen)
        painter.setBrush(self.CenterPointColor)
        # diameter = diameter # self.widget_diameter/6
        painter.drawEllipse(int(-diameter / 2), int(-diameter / 2), int(diameter), int(diameter))

    def draw_needle(self):
        painter = QPainter(self)
        # painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        # Koordinatenursprung in die Mitte der Flaeche legen
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.NeedleColor)
        painter.rotate(((self.value - self.value_min) * self.scale_angle_size /
                        (self.value_max - self.value_min)) + 90 + self.scale_angle_start_value)

        painter.drawConvexPolygon(self.value_needle[0])

    ###############################################################################################
    # Events
    ###############################################################################################

    def resizeEvent(self, event):
        self.rescale_method()

    def paintEvent(self, event):
        # Main Drawing Event:
        # Will be executed on every change
        # vgl http://doc.qt.io/qt-4.8/qt-demos-affine-xform-cpp.html
        # print("event", event
        # draw scale marker lines
        if self.enable_fine_scaled_marker:
            self.create_fine_scaled_marker()
        if self.enable_big_scaled_marker:
            self.draw_big_scaled_markter()

        # draw scale marker value text
        if self.enable_scale_text:
            self.create_scale_marker_values_text()

        # draw needle 1
        if self.enable_Needle_Polygon:
            self.draw_needle()

        # Draw Center Point
        if self.enable_CenterPoint:
            self.draw_big_needle_center_point(diameter=(self.widget_diameter / 6))

    ###############################################################################################
    # MouseEvents
    ###############################################################################################

    # for the needle mouvement
    def mouseMoveEvent(self, event):
        x, y = event.x() - (self.width() / 2), event.y() - (self.height() / 2)
        if not x == 0:
            angle = math.atan2(y, x) / math.pi * 180
            # winkellaenge der anzeige immer positiv 0 - 360deg
            # min wert + umskalierter wert
            value = (float(math.fmod(angle - self.scale_angle_start_value + 720, 360)) /
                     (float(self.scale_angle_size) / float(self.value_max - self.value_min))) + self.value_min
            if (self.value - (self.value_max - self.value_min) * self.value_needle_snapzone) <= \
                    value <= \
                    (self.value + (self.value_max - self.value_min) * self.value_needle_snapzone):
                self.NeedleColor = self.NeedleColorDrag

                # if value >= self.value_max and self.last_value < (self.value_max - self.value_min) / 2:
                if value >= self.value_max and self.last_value < (self.value_max - self.value_min) / 2:
                    value = self.value_max
                    self.last_value = self.value_min
                    self.valueChanged.emit(int(value))
                elif value >= self.value_max >= self.last_value:
                    value = self.value_max
                    self.last_value = self.value_max
                    self.valueChanged.emit(int(value))
                else:
                    self.last_value = value
                    self.valueChanged.emit(int(value))
