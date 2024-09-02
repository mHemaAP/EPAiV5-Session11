import polygons
from polygons import *
from datetime import datetime
import pytest
from io import StringIO 
import sys
import time
import inspect
import os
import re

README_CONTENT_CHECK_FOR = [
"polygon",
"iterator",
"__iter__",
"__next__",
"lazy",
"StopIteration"
]

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(polygons)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(polygons, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

def test_polygon():
    abs_tol = 0.001
    rel_tol = 0.001
    
    try:
        p = Polygon(2, 10)
        assert False, ('Creating a Polygon with 2 sides: '
                       ' Exception expected, not received')
    except ValueError:
        pass
                       
    n = 3
    R = 1
    p = Polygon(n, R)
    assert str(p) == 'Polygon(n=3, R=1)', f'actual: {str(p)}'
    assert p.count_vertices == n, (f'actual: {p.count_vertices},'
                                   f' expected: {n}')
    assert p.count_edges == n, f'actual: {p.count_edges}, expected: {n}'
    assert p.circumradius == R, f'actual: {p.circumradius}, expected: {n}'
    assert p.interior_angle == 60, (f'actual: {p.interior_angle},'
                                    ' expected: 60')
    n = 4
    R = 1
    p = Polygon(n, R)
    assert p.interior_angle == 90, (f'actual: {p.interior_angle}, '
                                    ' expected: 90')
    assert math.isclose(p.area, 2, 
                        rel_tol=abs_tol, 
                        abs_tol=abs_tol), (f'actual: {p.area},'
                                           ' expected: 2.0')
    
    assert math.isclose(p.side_length, math.sqrt(2),
                       rel_tol=rel_tol,
                       abs_tol=abs_tol), (f'actual: {p.side_length},'
                                          f' expected: {math.sqrt(2)}')
    
    assert math.isclose(p.perimeter, 4 * math.sqrt(2),
                       rel_tol=rel_tol,
                       abs_tol=abs_tol), (f'actual: {p.perimeter},'
                                          f' expected: {4 * math.sqrt(2)}')
    
    assert math.isclose(p.apothem, 0.707,
                       rel_tol=rel_tol,
                       abs_tol=abs_tol), (f'actual: {p.perimeter},'
                                          ' expected: 0.707')
    p = Polygon(6, 2)
    assert math.isclose(p.side_length, 2,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.apothem, 1.73205,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.area, 10.3923,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.perimeter, 12,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.interior_angle, 120,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    
    p = Polygon(12, 3)
    assert math.isclose(p.side_length, 1.55291,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.apothem, 2.89778,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.area, 27,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.perimeter, 18.635,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    assert math.isclose(p.interior_angle, 150,
                        rel_tol=rel_tol, abs_tol=abs_tol)
    
    p1 = Polygon(3, 10)
    p2 = Polygon(10, 10)
    p3 = Polygon(15, 10)
    p4 = Polygon(15, 100)
    p5 = Polygon(15, 100)
    
    assert p2 > p1
    assert p2 < p3
    assert p3 != p4
    assert p1 != p4
    assert p4 == p5

# Test function for lazy evaluation
def test_lazy_evaluation():
    p = Polygon(6, 2)  # A hexagon

    # Initial counts should be zero
    assert p._interior_angle_calls == 0
    assert p._side_length_calls == 0
    assert p._apothem_calls == 0
    assert p._area_calls == 0
    assert p._perimeter_calls == 0

    # Accessing each property should increment the respective call count once
    _ = p.interior_angle
    assert p._interior_angle_calls == 1
    assert p._side_length_calls == 0
    assert p._apothem_calls == 0
    assert p._area_calls == 0
    assert p._perimeter_calls == 0

    _ = p.side_length
    assert p._side_length_calls == 1
    assert p._interior_angle_calls == 1
    assert p._apothem_calls == 0
    assert p._area_calls == 0
    assert p._perimeter_calls == 0

    _ = p.apothem
    assert p._apothem_calls == 1
    assert p._side_length_calls == 1
    assert p._interior_angle_calls == 1
    assert p._area_calls == 0
    assert p._perimeter_calls == 0

    _ = p.area
    assert p._area_calls == 1
    assert p._apothem_calls == 1
    assert p._side_length_calls == 1
    assert p._interior_angle_calls == 1
    assert p._perimeter_calls == 0

    _ = p.area
    _ = p.perimeter
    assert p._perimeter_calls == 1
    assert p._area_calls == 1
    assert p._apothem_calls == 1
    assert p._side_length_calls == 1
    assert p._interior_angle_calls == 1

    # Changing circumradius should invalidate cache and cause recalculation
    p.circumradius = 4
    _ = p.side_length
    _ = p.area
    _ = p.perimeter
    _ = p.apothem
    _ = p.interior_angle            
    assert p._side_length_calls == 2
    assert p._interior_angle_calls == 2
    assert p._apothem_calls == 2
    assert p._area_calls == 2
    assert p._perimeter_calls == 2

    # Changing count_vertices should invalidate cache and cause recalculation
    p.count_vertices = 8
    _ = p.side_length
    _ = p.area
    _ = p.perimeter
    _ = p.apothem    
    _ = p.interior_angle       
    assert p._side_length_calls == 3
    assert p._interior_angle_calls == 3
    assert p._apothem_calls == 3
    assert p._area_calls == 3
    assert p._perimeter_calls == 3

    _ = p.side_length
    _ = p.area
    _ = p.perimeter
    _ = p.apothem    
    _ = p.interior_angle       
    assert p._side_length_calls == 3
    assert p._interior_angle_calls == 3
    assert p._apothem_calls == 3
    assert p._area_calls == 3
    assert p._perimeter_calls == 3

    # Run the test
    print("Lazy evaluation with cache invalidation test passed!")
