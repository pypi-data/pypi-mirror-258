## 
# CairoBackend.py 
#
# This file is part of the Chemical Data Processing Toolkit
#
# Copyright (C) 2003 Thomas Seidel <thomas.seidel@univie.ac.at>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; see the file COPYING. If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
##


from __future__ import absolute_import

import array
import cairo
import math

import CDPL.Vis as Vis


__all__ = [ 'CairoFontMetrics', 'CairoRenderer2D' ]


dense1PatternData = array.array('B', [ 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255 ])
dense2PatternData = array.array('B', [ 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 0, 255, 255, 255, 255, 255 ])
dense3PatternData = array.array('B', [ 255, 0, 255, 255, 0, 255, 0, 255, 255, 255, 255, 0, 0, 255, 0, 255 ])
dense4PatternData = array.array('B', [ 255, 0, 255, 0, 0, 255, 0, 255, 255, 0, 255, 0, 0, 255, 0, 255 ])
dense5PatternData = array.array('B', [ 0, 255, 0, 0, 255, 0, 255, 0, 0, 0, 0, 255, 255, 0, 255, 0 ])
dense6PatternData = array.array('B', [ 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 0, 0, 0 ])
dense7PatternData = array.array('B', [ 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ])
horPatternData = array.array('B', [ 0, 0, 0, 0, 255, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0 ])
verPatternData = array.array('B', [ 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0 ])
crossPatternData = array.array('B', [ 0, 255, 0, 0, 255, 255, 255, 255, 0, 255, 0, 0, 0, 255, 0, 0 ])
leftDiagPatternData = array.array('B', [ 0, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 255, 0, 0, 0 ])
rightDiagPatternData = array.array('B', [ 255, 0, 0, 0, 0, 255, 0, 0, 0, 0, 255, 0, 0, 0, 0, 255 ])
diagCrossPatternData = array.array('B', [ 0, 0, 0, 255, 0, 0, 0, 0, 0, 0, 255, 0, 255, 0, 0, 0,
                                          0, 255, 0, 0, 0, 255, 0, 0, 255, 0, 0, 0, 0, 0, 255,
                                          0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 0, 0, 0, 0, 0, 255, 0,
                                          0, 255, 0, 0, 0, 255, 0, 0, 0, 0, 255, 0, 255, 0, 0, 0 ])

dense1Pattern    = cairo.ImageSurface.create_for_data(dense1PatternData,    cairo.FORMAT_A8, 4, 4, 4) 
dense2Pattern    = cairo.ImageSurface.create_for_data(dense2PatternData,    cairo.FORMAT_A8, 4, 4, 4) 
dense3Pattern    = cairo.ImageSurface.create_for_data(dense3PatternData,    cairo.FORMAT_A8, 4, 4, 4) 
dense4Pattern    = cairo.ImageSurface.create_for_data(dense4PatternData,    cairo.FORMAT_A8, 4, 4, 4) 
dense5Pattern    = cairo.ImageSurface.create_for_data(dense5PatternData,    cairo.FORMAT_A8, 4, 4, 4) 
dense6Pattern    = cairo.ImageSurface.create_for_data(dense6PatternData,    cairo.FORMAT_A8, 4, 4, 4) 
dense7Pattern    = cairo.ImageSurface.create_for_data(dense7PatternData,    cairo.FORMAT_A8, 4, 4, 4) 
horPattern       = cairo.ImageSurface.create_for_data(horPatternData,       cairo.FORMAT_A8, 4, 4, 4) 
verPattern       = cairo.ImageSurface.create_for_data(verPatternData,       cairo.FORMAT_A8, 4, 4, 4) 
crossPattern     = cairo.ImageSurface.create_for_data(crossPatternData,     cairo.FORMAT_A8, 4, 4, 4) 
leftDiagPattern  = cairo.ImageSurface.create_for_data(leftDiagPatternData,  cairo.FORMAT_A8, 4, 4, 4) 
rightDiagPattern = cairo.ImageSurface.create_for_data(rightDiagPatternData, cairo.FORMAT_A8, 4, 4, 4) 
diagCrossPattern = cairo.ImageSurface.create_for_data(diagCrossPatternData, cairo.FORMAT_A8, 8, 8, 8)

fillPatternMap = { Vis.Brush.DENSE1_PATTERN     : dense1Pattern,
                   Vis.Brush.DENSE2_PATTERN     : dense2Pattern,
                   Vis.Brush.DENSE3_PATTERN     : dense3Pattern,
                   Vis.Brush.DENSE4_PATTERN     : dense4Pattern,
                   Vis.Brush.DENSE5_PATTERN     : dense5Pattern,
                   Vis.Brush.DENSE6_PATTERN     : dense6Pattern,
                   Vis.Brush.DENSE7_PATTERN     : dense7Pattern,
                   Vis.Brush.H_PATTERN          : horPattern,
                   Vis.Brush.V_PATTERN          : verPattern,
                   Vis.Brush.CROSS_PATTERN      : crossPattern,
                   Vis.Brush.LEFT_DIAG_PATTERN  : leftDiagPattern,
                   Vis.Brush.RIGHT_DIAG_PATTERN : rightDiagPattern,
                   Vis.Brush.DIAG_CROSS_PATTERN : diagCrossPattern }

capStyleMap = { Vis.Pen.FLAT_CAP   : cairo.LINE_CAP_BUTT,
                Vis.Pen.SQUARE_CAP : cairo.LINE_CAP_SQUARE,
                Vis.Pen.ROUND_CAP  : cairo.LINE_CAP_ROUND } 

joinStyleMap = { Vis.Pen.MITER_JOIN : cairo.LINE_JOIN_MITER,
                 Vis.Pen.BEVEL_JOIN : cairo.LINE_JOIN_BEVEL,
                 Vis.Pen.ROUND_JOIN : cairo.LINE_JOIN_ROUND }

class ToCairoPathConverter(Vis.Path2DConverter):

    def __init__(self, path, cairo_ctxt):
        Vis.Path2DConverter.__init__(self)
        self.__cairoContext = cairo_ctxt
        
        cairo_ctxt.new_path()

        if path.getFillRule() == Vis.Path2D.WINDING:
            fill_rule = cairo.FILL_RULE_WINDING
        else:
            fill_rule = cairo.FILL_RULE_EVEN_ODD
            
        cairo_ctxt.set_fill_rule(fill_rule)
        path.convert(self)
        
    def moveTo(self, x, y):
        self.__cairoContext.move_to(x, y)
 
    def arcTo(self, cx, cy, rx, ry, start_ang, sweep):
        start_ang *= math.pi / 180.0
        sweep *= math.pi / 180.0

        if rx == ry:
            if sweep >= 0.0:
                self.__cairoContext.arc(cx, cy, rx, start_ang, start_ang + sweep)
            else:
                self.__cairoContext.arc_negative(cx, cy, rx, start_ang, start_ang + sweep)
            return

        self.__cairoContext.save()
        self.__cairoContext.translate(cx, cy)
        self.__cairoContext.scale(rx, ry)

        if sweep >= 0.0:
            self.__cairoContext.arc(0.0, 0.0, 1.0, start_ang, start_ang + sweep)
        else:
            self.__cairoContext.arc_negative(0.0, 0.0, 1.0, start_ang, start_ang + sweep)

        self.__cairoContext.restore()


    def lineTo(self, x, y):
        self.__cairoContext.line_to(x, y)

    def closePath(self):
        self.__cairoContext.close_path()

    
class CairoFontMetrics(Vis.FontMetrics):

    def __init__(self, cairo_ctxt):
        "__init__(CairoFontMetrics self, cairo.Context cairo_ctxt) -> None :"
        Vis.FontMetrics.__init__(self)
        self.__cairoContext = cairo_ctxt

    def setFont(self, font):
        "setFont(CairoFontMetrics self, Vis.Font font) -> None :"
        if font.italic:
            font_slant = cairo.FONT_SLANT_ITALIC
        else:
            font_slant = cairo.FONT_SLANT_NORMAL

        if font.bold:
            font_weight = cairo.FONT_WEIGHT_BOLD
        else:
            font_weight = cairo.FONT_WEIGHT_NORMAL
            
        self.__cairoContext.select_font_face(font.family, font_slant, font_weight)
        self.__cairoContext.set_font_size(font.size)

        self.__fontExtents = self.__cairoContext.font_extents()
        
    def getAscent(self):
        "getAscent(CairoFontMetrics self) -> float :"
        return self.__fontExtents[0]
    
    def getDescent(self):
        "getDescent(CairoFontMetrics self) -> float :"
        return self.__fontExtents[1]
    
    def getHeight(self):
        "getHeight(CairoFontMetrics self) -> float :"
        return (self.getAscent() + self.getDescent() + 1.0)
    
    def getLeading(self):
        "getLeading(CairoFontMetrics self) -> float :"
        return (self.__fontExtents[2] - self.getHeight())
    
    def getWidth(self, string):
        "getWidth(CairoFontMetrics self) -> float :"
        return self.__cairoContext.text_extents(string)[4]

    def getBounds(self, string, bounds):
        "getBounds(CairoFontMetrics self, str string, Vis.Rectangle2D bounds) -> float :"
        text_extents = self.__cairoContext.text_extents(string)

        bounds.setBounds(text_extents[0], text_extents[1],
                         text_extents[2] + text_extents[0],
                         text_extents[3] + text_extents[1])


class CairoRenderer2D(Vis.Renderer2D):

    def __init__(self, cairo_ctxt):
        "__init__(CairoRenderer2D self, cairo.Context cairo_ctxt) -> None :"
        Vis.Renderer2D.__init__(self)
        self.__cairoContext = cairo_ctxt
        self.__penStack = [ Vis.Pen() ]
        self.__brushStack = [ Vis.Brush() ]
        self.__fontStack = [ Vis.Font() ]

    def saveState(self):
        "saveState(CairoRenderer2D self) -> None :"
        self.__cairoContext.save()

        self.__penStack.append(self.__penStack[-1])
        self.__brushStack.append(self.__brushStack[-1])
        self.__fontStack.append(self.__fontStack[-1])

    def restoreState(self):
        "restoreState(CairoRenderer2D self) -> None :"
        if len(self.__penStack) > 1:
            self.__cairoContext.restore()

            del self.__penStack[-1]
            del self.__brushStack[-1]
            del self.__fontStack[-1]

    def setTransform(self, xform):
        "setTransform(CairoRenderer2D self, Math.Matrix3D xform) -> None :"
        cairo_xform = cairo.Matrix(xform(0, 0), xform(1, 0), xform(0, 1), 
                                   xform(1, 1), xform(0, 2), xform(1, 2))

        self.__cairoContext.set_matrix(cairo_xform)

    def transform(self, xform):
        "transform(CairoRenderer2D self, Math.Matrix3D xform) -> None :"
        cairo_xform = cairo.Matrix(xform(0, 0), xform(1, 0), xform(0, 1), 
                                   xform(1, 1), xform(0, 2), xform(1, 2))
    
        self.__cairoContext.transform(cairo_xform)

    def setPen(self, pen):
        "setPen(CairoRenderer2D self, Vis.Pen pen) -> None :"
        if isinstance(pen, Vis.Color):
            pen = Vis.Pen(pen)
        
        self.__penStack[-1] = pen

    def setBrush(self, brush):
        "setBrush(CairoRenderer2D self, Vis.Brush brush) -> None :"
        if isinstance(brush, Vis.Color):
            brush = Vis.Brush(brush)
  
        self.__brushStack[-1] = brush

    def setFont(self, font):
        "setFont(CairoRenderer2D self, Vis.Font font) -> None :"
        if isinstance(font, str):
            font = Vis.Font(font)
        
        self.__fontStack[-1] = font

    def drawRectangle(self, x, y, width, height):
        "drawRectangle(CairoRenderer2D self, float x, float y, float width, float height) -> None :"
        self.__cairoContext.new_path()
        self.__cairoContext.rectangle(x, y, width, height)

        self.__fillPath()
        self.__strokePath()

    def drawPolygon(self, points):
        "drawPolygon(CairoRenderer2D self, Math.Vector2DArray points) -> None :"
        self.__cairoContext.new_path()

        move = True

        for point in points:
            if move:
                self.__cairoContext.move_to(point[0], point[1])
                move = False
            else:
                self.__cairoContext.line_to(point[0], point[1])

        self.__cairoContext.close_path()

        self.__fillPath()
        self.__strokePath()

    def drawLine(self, x1, y1, x2, y2):
        "drawLine(CairoRenderer2D self, float x1, float y1, float x2, float y2) -> None :"
        self.__cairoContext.new_path()

        self.__cairoContext.move_to(x1, y1)
        self.__cairoContext.line_to(x2, y2)

        self.__strokePath()

    def drawPolyline(self, points):
        "drawPolyline(CairoRenderer2D self, Math.Vector2DArray points) -> None :"
        self.__cairoContext.new_path()

        move = True
        
        for point in points:
            if move:
                self.__cairoContext.move_to(point[0], point[1])
                move = False
            else:
                self.__cairoContext.line_to(point[0], point[1])

        self.__strokePath()

    def drawLineSegments(self, points):
        "drawLineSegments(CairoRenderer2D self, Math.Vector2DArray points) -> None :"
        self.__cairoContext.new_path()

        for i in range(0, len(points), 2):
            point1 = points[i]
            point2 = points[i + 1]

            self.__cairoContext.move_to(point1[0], point1[1])
            self.__cairoContext.line_to(point2[0], point2[1])

        self.__strokePath()

    def drawPoint(self, x, y):
        "drawPoint(CairoRenderer2D self, float x, float y) -> None :"
        self.__cairoContext.new_path()

        radius = self.__penStack[-1].width * 0.5
        color = self.__penStack[-1].color

        self.__cairoContext.set_source_rgba(color.red, color.green, color.blue, color.alpha)

        self.__cairoContext.arc(x, y, radius, 0.0, 2.0 * math.pi)
        self.__cairoContext.fill()

    def drawEllipse(self, x, y, width, height):
        "drawEllipse(CairoRenderer2D self, float x, float y, float width, float height) -> None :"
        self.__cairoContext.new_path()

        self.__cairoContext.save()
        self.__cairoContext.translate(x, y)
        self.__cairoContext.scale(1.0, height / width)
        self.__cairoContext.arc(0.0, 0.0, width * 0.5, 0.0, 2 * 3.141593)
        self.__cairoContext.restore()
        
        self.__fillPath()
        self.__strokePath()

    def drawText(self, x, y, txt):
        "drawText(CairoRenderer2D self, float x, float y, str txt) -> None :"
        font = self.__fontStack[-1]
        
        if font.italic:
            font_slant = cairo.FONT_SLANT_ITALIC
        else:
            font_slant = cairo.FONT_SLANT_NORMAL

        if font.bold:
            font_weight = cairo.FONT_WEIGHT_BOLD
        else:
            font_weight = cairo.FONT_WEIGHT_NORMAL
            
        self.__cairoContext.select_font_face(font.family, font_slant, font_weight)
        self.__cairoContext.set_font_size(font.size)

        color = self.__penStack[-1].color

        self.__cairoContext.set_source_rgba(color.red, color.green, color.blue, color.alpha)
        self.__cairoContext.move_to(x, y)
        self.__cairoContext.show_text(txt)
        
    def drawPath(self, path):
        "drawPath(CairoRenderer2D self, Vis.Path2D path) -> None :"
        prev_fill_rule = self.__cairoContext.get_fill_rule()

        ToCairoPathConverter(path, self.__cairoContext)

        self.__fillPath()
        self.__strokePath()

        self.__cairoContext.set_fill_rule(prev_fill_rule)

    def setClipPath(self, path):
        "setClipPath(CairoRenderer2D self, Vis.Path2D path) -> None :"
        prev_fill_rule = self.__cairoContext.get_fill_rule()

        ToCairoPathConverter(path, self.__cairoContext)

        self.__cairoContext.clip()
        self.__cairoContext.set_fill_rule(prev_fill_rule)

    def clearClipPath(self):
        "clearClipPath(CairoRenderer2D self) -> None :"
        self.__cairoContext.reset_clip()

    def __fillPath(self):
        brush = self.__brushStack[-1]

        if brush.style == Vis.Brush.NO_PATTERN:
            return

        color = brush.color

        try:
            pattern = fillPatternMap[brush.style]
        except KeyError:
            self.__cairoContext.set_source_rgba(color.red, color.green, color.blue, color.alpha)
            self.__cairoContext.fill_preserve()
            return
    
        ptn_width = pattern.get_width()
        ptn_height = pattern.get_height()

        src_surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, ptn_width, ptn_height)
        src_ctxt = cairo.Context(src_surf)

        src_ctxt.set_source_rgba(color.red, color.green, color.blue, color.alpha)
        src_ctxt.mask_surface(pattern, 0.0, 0.0)

        src_pattern = cairo.SurfacePattern(src_surf)
        src_pattern.set_extend(cairo.EXTEND_REPEAT)

        self.__cairoContext.set_source(src_pattern)
        self.__cairoContext.fill_preserve()

    def __strokePath(self):
        pen = self.__penStack[-1]
        line_width = pen.width

        if line_width == 0.0:
            self.__cairoContext.set_dash([], 0)
        else:
            line_style = pen.lineStyle
            
            if line_style == Vis.Pen.NO_LINE:
                return
    
            elif line_style == Vis.Pen.DASH_LINE:
                self.__cairoContext.set_dash([ 5.0 * line_width ], 0)

            elif line_style == Vis.Pen.DOT_LINE:
                self.__cairoContext.set_dash([ line_width, line_width * 1.5 ], 0)

            elif line_style == Vis.Pen.DASH_DOT_LINE:
                self.__cairoContext.set_dash([ line_width * 5.0, line_width * 1.5,
                                               line_width, line_width * 1.5 ], 0)

            elif line_style == Vis.Pen.DASH_DOT_DOT_LINE:
                self.__cairoContext.set_dash([ line_width * 5.0, line_width * 1.5,
                                               line_width, line_width * 1.5,
                                               line_width, line_width * 1.5 ], 0)
            else:
                self.__cairoContext.set_dash([], 0)

        try:
            join_style = joinStyleMap[pen.joinStyle]
        except KeyError:
            join_style = cairo.LINE_JOIN_ROUND
    
        try:
            cap_style = capStyleMap[pen.capStyle]
        except KeyError:
            cap_style = cairo.LINE_CAP_ROUND

        color = pen.color
        
        self.__cairoContext.set_line_join(join_style)
        self.__cairoContext.set_line_cap(cap_style)
        self.__cairoContext.set_line_width(line_width)
        self.__cairoContext.set_source_rgba(color.red, color.green, color.blue, color.alpha)

        self.__cairoContext.stroke()
