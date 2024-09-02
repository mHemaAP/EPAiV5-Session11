import math
from functools import cached_property

class Polygon:
    """
    A class to represent a regular polygon with a given number of sides and circumradius.

    Attributes:
    -----------
    count_vertices : int
        Number of vertices (or sides) of the polygon.
    count_edges : int
        Number of edges (equal to the number of vertices) of the polygon.
    circumradius : float
        The circumradius of the polygon.

    Methods:
    --------
    interior_angle() -> float:
        Returns the interior angle of the polygon.
    side_length() -> float:
        Returns the length of a side of the polygon.
    apothem() -> float:
        Returns the apothem of the polygon.
    area() -> float:
        Returns the area of the polygon.
    perimeter() -> float:
        Returns the perimeter of the polygon.
    __eq__(other) -> bool:
        Checks if two polygons are equal based on the number of edges and circumradius.
    __gt__(other) -> bool:
        Checks if the current polygon has more vertices than another polygon.
    """
    def __init__(self, n, R):
        """
        Initializes a regular polygon with n vertices and circumradius R.

        Parameters:
        -----------
        n : int
            Number of vertices (or sides) of the polygon. Must be at least 3.
        R : float
            The circumradius of the polygon.
        """
        if n < 3:
            raise ValueError('Polygon must have at least 3 vertices.')
        self._n = n
        self._R = R
        self._interior_angle_calls = 0
        self._side_length_calls = 0
        self._apothem_calls = 0
        self._area_calls = 0
        self._perimeter_calls = 0

    def __repr__(self):
        """
        Returns a string representation of the Polygon object.
        """
        return f'Polygon(n={self._n}, R={self._R})'

    @property
    def count_vertices(self):
        """
        Returns the number of vertices (or sides) of the polygon.
        """
        return self._n

    @count_vertices.setter
    def count_vertices(self, new_n):
        """
        Sets a new number of vertices (or sides) for the polygon and invalidates cached properties.

        Parameters:
        -----------
        new_n : int
            The new number of vertices (or sides). Must be at least 3.
        """
        if new_n < 3:
            raise ValueError('Polygon must have at least 3 vertices.')
        self._n = new_n
        self._invalidate_cache()

    @property
    def count_edges(self):
        """
        Returns the number of edges (equal to the number of vertices) of the polygon.
        """
        return self._n

    @property
    def circumradius(self):
        """
        Returns the circumradius of the polygon.
        """
        return self._R

    @circumradius.setter
    def circumradius(self, new_R):
        """
        Sets a new circumradius for the polygon and invalidates cached properties.

        Parameters:
        -----------
        new_R : float
            The new circumradius.
        """
        self._R = new_R
        self._invalidate_cache()

    def _invalidate_cache(self):
        """
        Invalidates the cached properties for the polygon.
        """
        for attr in ['side_length', 'apothem', 'area', 'perimeter', 'interior_angle']:
            if attr in self.__dict__:
                del self.__dict__[attr]

    @cached_property
    def interior_angle(self):
        """
        Returns the interior angle of the polygon in degrees.

        Returns:
        --------
        float: The interior angle of the polygon.
        """
        self._interior_angle_calls += 1
        return (self._n - 2) * 180 / self._n

    @cached_property
    def side_length(self):
        """
        Returns the length of a side of the polygon.

        Returns:
        --------
        float: The length of a side.
        """
        self._side_length_calls += 1
        return 2 * self._R * math.sin(math.pi / self._n)

    @cached_property
    def apothem(self):
        """
        Returns the apothem (the distance from the center to the midpoint of a side) of the polygon.

        Returns:
        --------
        float: The apothem of the polygon.
        """
        self._apothem_calls += 1
        return self._R * math.cos(math.pi / self._n)

    @cached_property
    def area(self):
        """
        Returns the area of the polygon.

        Returns:
        --------
        float: The area of the polygon.
        """
        self._area_calls += 1
        return self._n / 2 * self.side_length * self.apothem

    @cached_property
    def perimeter(self):
        """
        Returns the perimeter of the polygon.

        Returns:
        --------
        float: The perimeter of the polygon.
        """
        self._perimeter_calls += 1
        return self._n * self.side_length

    def __eq__(self, other):
        """
        Checks if two polygons are equal based on the number of edges and circumradius.

        Parameters:
        -----------
        other : Polygon
            The polygon to compare with.

        Returns:
        --------
        bool: True if polygons are equal, False otherwise.
        """
        if isinstance(other, self.__class__):
            return (self.count_edges == other.count_edges
                    and self.circumradius == other.circumradius)
        else:
            return NotImplemented

    def __gt__(self, other):
        """
        Checks if the current polygon has more vertices than another polygon.

        Parameters:
        -----------
        other : Polygon
            The polygon to compare with.

        Returns:
        --------
        bool: True if the current polygon has more vertices, False otherwise.
        """
        if isinstance(other, self.__class__):
            return self.count_vertices > other.count_vertices
        else:
            return NotImplemented



class Polygons:
    """
    A class to represent a sequence of regular polygons with the same circumradius.

    Attributes:
    -----------
    max_efficiency_polygon : Polygon
        The polygon with the highest area-to-perimeter ratio.

    Methods:
    --------
    __len__() -> int:
        Returns the number of polygons in the sequence.
    __iter__() -> PolygonIterator:
        Returns an iterator over the polygons.
    """
    def __init__(self, m, R):
        """
        Initializes a sequence of polygons with a maximum number of sides and a circumradius.

        Parameters:
        -----------
        m : int
            The maximum number of sides of the polygons in the sequence. Must be at least 3.
        R : float
            The circumradius of all polygons in the sequence.
        """
        if m < 3:
            raise ValueError('m must be greater than 3')
        self._m = m
        self._R = R

    def __len__(self):
        """
        Returns the number of polygons in the sequence.

        Returns:
        --------
        int: The number of polygons.
        """
        return self._m - 2

    def __repr__(self):
        """
        Returns a string representation of the Polygons object.
        """
        return f'Polygons(m={self._m}, R={self._R})'

    def __iter__(self):
        """
        Returns an iterator over the polygons.

        Returns:
        --------
        PolygonIterator: An iterator over the polygons.
        """
        return self.PolygonIterator(self._m, self._R)

    @property
    def max_efficiency_polygon(self):
        """
        Returns the polygon with the highest area-to-perimeter ratio.

        Returns:
        --------
        Polygon: The polygon with the highest area-to-perimeter ratio.
        """
        return max(self, key=lambda p: p.area/p.perimeter)

    class PolygonIterator:
        """
        An iterator class to iterate over a sequence of polygons.

        Methods:
        --------
        __iter__() -> PolygonIterator:
            Returns the iterator itself.
        __next__() -> Polygon:
            Returns the next polygon in the sequence.
        """
        def __init__(self, m, R):
            """
            Initializes the iterator with a maximum number of sides and a circumradius.

            Parameters:
            -----------
            m : int
                The maximum number of sides of the polygons in the sequence.
            R : float
                The circumradius of all polygons in the sequence.
            """
            self._m = m
            self._R = R
            self._index = 3

        def __iter__(self):
            """
            Returns the iterator itself.

            Returns:
            --------
            PolygonIterator: The iterator itself.
            """
            return self

        def __next__(self):
            """
            Returns the next polygon in the sequence.

            Returns:
            --------
            Polygon: The next polygon in the sequence.

            Raises:
            -------
            StopIteration: When all polygons have been iterated over.
            """
            if self._index > self._m:
                raise StopIteration
            else:
                polygon = Polygon(self._index, self._R)
                self._index += 1
                return polygon
