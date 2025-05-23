import csv
import svgwrite
import os
import math
import sys

# script for creating SVG images containing coloured shapes, described in shape_lists* files
# to use, call the script with the path to the shape list file as the first and only argument, for example:
#
# $ python svgGenerator.py ..\ShapeLists\shape_lists_0.csv

input_file = sys.argv[1]
input_file_stripped = os.path.splitext(os.path.basename(input_file))[0]

# Ensure output directory exists
output_dir = "../ShapeSVGs/" + input_file_stripped
os.makedirs(output_dir, exist_ok=True)


svg_size=(150, 150)
svg_centre=(svg_size[0] / 2.0, svg_size[1] / 2.0)
shape_size=svg_size[0] / 2.0

colormap = {
    'blue':'#3580DB',
    'red':'#CC482C',
    'green':'#3FCC3B',
    'orange':'#FF8200'
}


def generate_sun_triangles(cx, cy, size):
    """Generate triangle point sets for the sun shape."""
    vertices = []

    # Outer points (0–7)
    radius = size
    for i in range(8):
        angle = 2 * math.pi / 8 * i
        x = cx + radius * math.sin(angle)
        y = cy - radius * math.cos(angle)
        vertices.append((x, y))

    # Mid-layer points (8–23)
    radius = size * 0.6
    for i in range(16):
        a = 0.5 + i
        angle = 2 * math.pi / 16 * a
        x = cx + radius * math.sin(angle)
        y = cy - radius * math.cos(angle)
        vertices.append((x, y))

    # Triangle indices
    triangles = [
        (0, 8, 23), (1, 10, 9), (2, 12, 11), (3, 14, 13),
        (4, 16, 15), (5, 18, 17), (6, 20, 19), (7, 22, 21)
    ]
    # Return triangle point sets
    return [[vertices[i] for i in tri] for tri in triangles]

def generate_cross_triangles(cx, cy, size):
    """Returns triangle point sets for the cross object from Unity."""
    raw_vertices = [
        (-0.1, 0.1), (0.1, 0.1), (0.1, -0.1), (-0.1, -0.1),
        (-0.1, 0.3), (0.1, 0.3), (0.4, 0.1), (0.4, -0.1),
        (0.1, -0.3), (-0.1, -0.3), (-0.4, -0.1), (-0.4, 0.1),
        (-0.2, 0.3), (0.0, 0.4), (0.2, 0.3),
        (0.4, 0.2), (0.5, 0.0), (0.4, -0.2),
        (0.2, -0.3), (0.0, -0.4), (-0.2, -0.3),
        (-0.4, -0.2), (-0.5, 0.0), (-0.4, 0.2)
    ]

    # Triangle indices from Unity mesh
    triangles = [
        (11, 6, 7), (11, 7, 10),
        (4, 5, 8), (4, 8, 9),
        (12, 13, 14), (15, 16, 17),
        (18, 19, 20), (21, 22, 23)
    ]

    # Scale and offset to SVG coordinates
    def scale(v):
        x, y = v
        return (cx + x * size, cy - y * size)  # SVG Y-axis is inverted

    # Return list of triangle point sets
    return [[scale(raw_vertices[i]) for i in tri] for tri in triangles]


def generate_star_triangles(cx, cy, size):
    """Generate triangle point sets for a 5-point star with one tip pointing up."""
    vertices = []

    # Outer radius
    r_outer = size
    angle = 2 * math.pi / 5

    # Outer points (0–4)
    for i in range(5):
        theta = i * angle
        x = cx + r_outer * math.sin(theta)
        y = cy - r_outer * math.cos(theta)
        vertices.append((x, y))

    # Inner radius (40% of outer)
    r_inner = r_outer * 0.4
    for i in range(5):
        theta = (i + 0.5) * angle
        x = cx + r_inner * math.sin(theta)
        y = cy - r_inner * math.cos(theta)
        vertices.append((x, y))

    # Triangle indices from Unity
    triangles = [
        (0, 5, 9), (1, 6, 5), (2, 7, 6),
        (3, 8, 7), (4, 9, 8), (7, 8, 9),
        (9, 5, 6), (9, 6, 7)
    ]

    # Convert index triangles to point sets
    return [[vertices[i] for i in tri] for tri in triangles]


# Define basic shape drawing functions
def draw_shape(dwg, shape, colorname):

    cx, cy = svg_centre
    size = shape_size

    color = colormap[colorname.lower()]

    if shape == "Circle":
        dwg.add(dwg.circle(center=svg_centre, r=size / 2, fill=color))
    
    elif shape == "Oval":
        dwg.add(dwg.ellipse(center=svg_centre, r=(size, size / 2), fill=color))
    
    elif shape == "Square":
        dwg.add(dwg.rect(insert=(cx - size / 2, cy - size / 2), size=(size, size), fill=color))
    
    elif shape == "Diamond":
        points = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
        dwg.add(dwg.polygon(points=points, fill=color))
    
    elif shape == "Triangle":
        tri_size = size * 0.66
        points = [(cx, cy - tri_size), (cx + tri_size, cy + tri_size), (cx - tri_size, cy + tri_size)]
        dwg.add(dwg.polygon(points=points, fill=color))
        
    elif shape == "Star":
        triangle_sets = generate_star_triangles(cx, cy, size)
        for tri_points in triangle_sets:
            dwg.add(dwg.polygon(points=tri_points, fill=color, stroke=color))

    
    elif shape == "Hexagon":
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.radians(angle_deg)
            x = cx + size * math.cos(angle_rad)
            y = cy + size * math.sin(angle_rad)
            points.append((x, y))
        dwg.add(dwg.polygon(points=points, fill=color))
        
    elif shape == "Sun":
        triangle_sets = generate_sun_triangles(cx, cy, size)
        for tri_points in triangle_sets:
            dwg.add(dwg.polygon(points=tri_points, fill=color))
        dwg.add(dwg.circle(center=svg_centre, r=size / 3, fill=color))

    elif shape == "SunFourPoint":
        triangle_sets = generate_sun_triangles(cx, cy, size)
        for i, tri_points in enumerate(triangle_sets):
            if i % 2 == 0:
                dwg.add(dwg.polygon(points=tri_points, fill=color))
        dwg.add(dwg.circle(center=svg_centre, r=size / 3, fill=color))


    elif shape == "SunTwoPoint":
        triangle_sets = generate_sun_triangles(cx, cy, size)
        for i, tri_points in enumerate(triangle_sets):
            if i % 4 == 0:
                dwg.add(dwg.polygon(points=tri_points, fill=color))
        dwg.add(dwg.circle(center=svg_centre, r=size / 3, fill=color))


    elif shape == "Cross":
        triangle_sets = generate_cross_triangles(cx, cy, size)
        for tri_points in triangle_sets:
            dwg.add(dwg.polygon(points=tri_points, fill=color, stroke=color))

    elif shape == "CrossSimple":
        dwg.add(dwg.rect(insert=(cx - size / 10, cy - size / 2), size=(size / 5, size), fill=color))
        dwg.add(dwg.rect(insert=(cx - size / 2, cy - size / 10), size=(size, size / 5), fill=color))
    
    elif shape == "CrossSimpleRotated":
        dwg.add(dwg.line(start=(cx - size / 2, cy - size / 2), end=(cx + size / 2, cy + size / 2), stroke=color, stroke_width=size / 10))
        dwg.add(dwg.line(start=(cx + size / 2, cy - size / 2), end=(cx - size / 2, cy + size / 2), stroke=color, stroke_width=size / 10))
    
    elif shape == "Pentagon":
        points = []
        for i in range(5):
            angle = math.radians(72 * i - 90)
            x = cx + size * math.cos(angle)
            y = cy + size * math.sin(angle)
            points.append((x, y))
        dwg.add(dwg.polygon(points=points, fill=color))
    
    elif shape == "DoubleTri":
        tri_h = size
        tri_w = size/2
        shift = tri_w * 0.4
        points1 = [(cx - shift, cy - tri_h/2), (cx + tri_w/2 - shift, cy + tri_h/2), (cx - tri_w/2 - shift, cy + tri_h/2)]
        points2 = [(cx + shift, cy - tri_h/2), (cx + tri_w/2 + shift, cy + tri_h/2), (cx - tri_w/2 + shift, cy + tri_h/2)]
        dwg.add(dwg.polygon(points=points1, fill=color))
        dwg.add(dwg.polygon(points=points2, fill=color))
    
    elif shape == "Tree":
        tri_h = size
        tri_w = size * 1.5
        shift = tri_h * 0.35
        dwg.add(dwg.polygon(points=[(cx, cy - tri_h/2 - shift), (cx + tri_w/2, cy + tri_h/2 - shift), (cx - tri_w/2, cy + tri_h/2 - shift)], fill=color))
        dwg.add(dwg.polygon(points=[(cx, cy - tri_h/2 + shift), (cx + tri_w/2, cy + tri_h/2 + shift), (cx - tri_w/2, cy + tri_h/2 + shift)], fill=color))
    
    elif shape == "OvalCross":
        dwg.add(dwg.ellipse(center=svg_centre, r=(size, size / 3), fill=color))
        dwg.add(dwg.ellipse(center=svg_centre, r=(size / 3, size), fill=color))
    
    else:
        dwg.add(dwg.text("Unknown", insert=(cx - 30, cy), fill="black"))





with open(input_file, encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):
        for part in ['p0', 'p1']:
            color = row[f'{part}_col']
            shape = row[f'{part}_shape']
            filename = f"{output_dir}/{part}_{i}.svg"
            
            # print(f'Will draw a {color} {shape}')

            dwg = svgwrite.Drawing(filename, profile='tiny', size=svg_size)
            draw_shape(dwg, shape, color)
            dwg.save()
