import math

class Cluster(object):
    """Cluster class

    The basic class of a cluster of seeds.

    Attributes:
        radius: The radius of a cluster of seeds
    """
    def __init__(self, radius):
        self.radius = radius
        self.area = math.pi * radius * radius

    def get_radius(self):
        return self.radius

class Pot(object):
    """Pot class

    The basic class of a pot for planting.

    Attributes:
        radius: The radius of the pot
    """

    def __init__(self):
        """Initialize the Pot class with cluster
        """
        self.cluster = []


    def add_cluster(self, cluster):
        """Add a cluster of seeds to the pot

        Args:
            cluster: A cluster instance
        """
        self.cluster.append(cluster)


class CircularPot(Pot):
    """Class for a circular pot
    """
    
    def __init__(self, radius):
        """Initializes radius and area
        """
        super(CircularPot, self).__init__()
        self.radius = radius
        self.area = math.pi * radius * radius

    def get_radius(self):
        """Returns the radius of the pot
        """
        return self.radius

    def cluster_calculation(self, seed_cluster_radius, radius_difference):
        """Returns the maximum number of clusters of the type of seed inputted
        that can be planted in the Pot.

        This algorithm is taken from The Engineering ToolBox
        """

        # calculate the number of clusters
        number_of_circles = math.floor((2 * math.pi * radius_difference) / (2 * seed_cluster_radius))
        x0 = radius_difference * math.cos(0 * 2 * math.pi / number_of_circles)
        x1 = radius_difference * math.cos(1 * 2 * math.pi / number_of_circles)
        y0 = radius_difference * math.sin(0 * 2 * math.pi / number_of_circles)
        y1 = radius_difference * math.sin(1 * 2 * math.pi / number_of_circles)
        distance = math.pow((math.pow(x0 - x1, 2)) + (math.pow(y0 - y1, 2)), 0.5)
        if distance < 2 * seed_cluster_radius:
            number_of_circles -=1

        # add cluster to optimal_clusters for image manipulation
        for i in xrange(int(number_of_circles)):
            self.optimal_clusters.append({"radius": seed_cluster_radius,
                                          "x": radius_difference * math.cos(i*2*math.pi/number_of_circles),
                                          "y": radius_difference * math.sin(i*2*math.pi/number_of_circles)
                                         })

        new_radius_difference = radius_difference - (2 * seed_cluster_radius)
        if new_radius_difference >= seed_cluster_radius:
            return number_of_circles + self.cluster_calculation(seed_cluster_radius, new_radius_difference)
        elif radius_difference > (2 * seed_cluster_radius):
            return number_of_circles + 1
        else:
            return number_of_circles

    def num_cluster_available(self, cluster):
        """Returns the maximum number of clusters of the type of seed inputted
        that can be planted in the given Pot.
        """
        self.optimal_clusters = []

        if self.get_radius() < cluster.get_radius():
            return (0, self.optimal_clusters)

        if self.get_radius() < cluster.get_radius() * 2:
            return (1, self.optimal_clusters)


        radius_difference = self.get_radius() - cluster.get_radius()
        return (int(self.cluster_calculation(cluster.get_radius(),
            radius_difference)), self.optimal_clusters)

class RectangularPot(Pot):
    """ Class for rectangular pot
    """
    def __init__(self, length, width):
        """Initializes area, length, and width
        """
        super(RectangularPot, self).__init__()
        self.length = length
        self.width = width
        self.area = length * width
    
    def get_length(self):
        """Return length of the pot
        """
        return self.length

    def get_width(self):
        """Return width of the pot
        """
        return self.width

    def cluster_calculation(self, seed_cluster_radius):
        # calculate the number of clusters
        seed_cluster_x_count = int(self.get_length() / (seed_cluster_radius * 2))
        seed_cluster_y_count = int(self.get_width() / (seed_cluster_radius* 2))

        # add cluster to .optimal_clusters for image manipulation
        for x_count in xrange(seed_cluster_x_count):
            for y_count in xrange(seed_cluster_y_count):
                self.optimal_clusters.append({"radius": seed_cluster_radius,
                                              "x": seed_cluster_radius + (x_count * seed_cluster_radius * 2),
                                              "y": seed_cluster_radius + (y_count * seed_cluster_radius * 2)
                                             })
        return seed_cluster_x_count * seed_cluster_y_count

    def num_cluster_available(self, cluster):
        """Returns the maximum number of clusters of the type of seed inputted
        that can be planted in the given Pot.
        """
        self.optimal_clusters = []
    
        if (self.get_length() < cluster.get_radius() or 
            self.get_width < cluster.get_radius()):
            return (0, self.optimal_clusters)
        
        return (self.cluster_calculation(cluster.get_radius()), self.optimal_clusters)

def circular_pot_calculation(pot_radius, cluster_radius):
    """Calculate the number of seed clusters that can be planted in a given pot

    Sometimes we want to see how many clusters of seeds we can plant in a 
    large circular pot for a home garden, and this is useful for determining
    that.

    Args:
        pot_radius: Radius of a pot
        cluster_radius: Optimal radius of a cluster of seeds

    Returns:
        A tuple (cluster_count, cluster_location)
    """
    pot = CircularPot(radius=float(pot_radius))
    seeds = Cluster(radius=float(cluster_radius))
    return pot.num_cluster_available(seeds)

def rectangular_pot_calculation(pot_length, pot_width, cluster_radius):
    """Calculate the number of seed clusters that can be planted in a
    rectangular pot

    Args:
        pot_length: the length of the pot
        pot_width: the width of the pot
        cluster_radius: optimal radius of a cluster of seeds

    Returns:
        A tuple (cluster_count, cluster_location)
    """
    pot = RectangularPot(float(pot_length), float(pot_width))
    seeds = Cluster(radius=float(cluster_radius))
    return pot.num_cluster_available(seeds)
