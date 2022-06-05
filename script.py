import cadquery as cq

length = 172
widthLeft = 112
widthRight = 112
height = 10
kbPadding = 8

switchHoleLength = 14
switchHoleGap = 5
gap = switchHoleLength + switchHoleGap


colShift = [0, 0, 12, 17.5, 11, 9]
startX = -3 * gap
startY = -2 * gap

caseStartX = startX - switchHoleLength / 2 - kbPadding
caseStartY = startY - switchHoleLength / 2 - kbPadding * 2

# result = cq.Workplane("front").rect(length, width)  # current point is the center of the circle, at (0, 0)
startThumbDegrees = -15
result = (
    cq.Workplane("front")
    .moveTo(caseStartX, caseStartY)
    .lineTo(caseStartX+86+2, caseStartY)
    .polarLine(switchHoleLength+4, startThumbDegrees)
    .polarLine(switchHoleLength+4, startThumbDegrees-15)
    .polarLine(switchHoleLength+3+kbPadding, startThumbDegrees-15*2)
    .polarLine(kbPadding+gap*2, 45)
    .polarLine(widthRight, 90)
    .polarLine(length, 180)
    .polarLine(widthLeft, 270)
    .close())

for x in range(0, len(colShift)):
    newX = startX + x * gap

    for y in range(4):
        newY = startY + y * gap + colShift[x]
        result = result.moveTo(newX, newY).rect(
            switchHoleLength, switchHoleLength)  # new work center is (1.5, 0.0)

for y in range(1, 4):
    newX = startX + 6 * gap
    newY = startY + y * gap + colShift[5]
    result = result.moveTo(newX, newY).rect(switchHoleLength, switchHoleLength)

# Thumb cluster
newX = startX + 45
newY = startY - 8
result = result.moveTo(newX, newY).rect(switchHoleLength, switchHoleLength)

newX = newX + gap
result = result.moveTo(newX, newY).rect(switchHoleLength, switchHoleLength)

result = result.extrude(height)

centerX = -newX
centerY = -newY

result = result.translate((centerX, centerY, 0))

rotationCenterY = switchHoleLength / 2 + 77
result = result.translate((0, rotationCenterY, 0))

# inner thumb cluster
result = result.rotate((0, 0, 0), (0, 0, 1), 15)
result = (
    result.moveTo(0, rotationCenterY)
          .rect(switchHoleLength, switchHoleLength))
result = result.cutThruAll()

# base thumb cluster
result = result.rotate((0, 0, 0), (0, 0, 1), 15)
result = (
    result.moveTo(0, rotationCenterY)
          .rect(switchHoleLength, switchHoleLength))
result = (
    result.moveTo(0, rotationCenterY+gap)
          .rect(switchHoleLength, switchHoleLength))
result = result.cutThruAll()

# outer thumb cluster
result = result.rotate((0, 0, 0), (0, 0, 1), 15)
result = (
    result.moveTo(0, rotationCenterY)
          .rect(switchHoleLength, switchHoleLength))
result = (
    result.moveTo(0, rotationCenterY+gap)
          .rect(switchHoleLength, switchHoleLength))
result = result.cutThruAll()

# rotate back
result = result.rotate((0, 0, 0), (0, 0, 1), -15*3)

result = result.translate((0, -rotationCenterY, 0))
result = result.translate((-centerX, -centerY, 0))

# Render the solid
show_object(result)

# Export
cq.exporters.export(result, 'result.stl')
cq.exporters.export(result.section(), 'result.dxf')
cq.exporters.export(result, 'result.step')
