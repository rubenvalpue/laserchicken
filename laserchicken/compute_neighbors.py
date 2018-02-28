from laserchicken import utils, kd_tree
from laserchicken.volume_specification import Sphere, InfiniteCylinder


def compute_cylinder_neighborhood(environment_pc, target_pc, radius):
    """Find the indices of points within a cylindrical neighbourhood (using KD Tree)
    for a given point of a target point cloud among the points from an environment point cloud.

    :param environment_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param radius: search radius for neighbors
    :return: indices of neighboring points from the environment point cloud for each target point
             the returned indices also contains the index of the target point.
    """

    env_tree = kd_tree.get_kdtree_for_pc(environment_pc)
    target_tree = kd_tree.get_kdtree_for_pc(target_pc)
    return target_tree.query_ball_tree(env_tree, radius)


def compute_sphere_neighborhood(environment_pc, target_pc, radius):
    """
    Find the indices of points within a spherical neighbourhood for a given point of a target point cloud among
    the points from an environment point cloud.

    :param environment_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param radius: search radius for neighbors
    :return: indices of neighboring points from the environment point cloud for each target point
    """

    neighborhood_indices = compute_cylinder_neighborhood(environment_pc, target_pc, radius)

    result = []
    for i in range(len(neighborhood_indices)):
        target_x, target_y, target_z = utils.get_point(target_pc, i)
        neighbor_indices = neighborhood_indices[i]
        result_indices = []
        for j in neighbor_indices:
            env_x, env_y, env_z = utils.get_point(environment_pc, j)
            if abs(target_z - env_z) > radius:
                continue
            if (env_x - target_x) ** 2 + (env_y - target_y) ** 2 + (env_z - target_z) ** 2 <=  radius ** 2 :
                result_indices.append(j)
        result.append(result_indices)
    return result


def compute_neighborhoods(env_pc, target_pc, volume_description):
    """
    Find a subset of points in a neighbourhood in the environment point cloud for each point in a target point cloud.

    :param env_pc: environment point cloud
    :param target_pc: point cloud that contains the points at which neighborhoods are to be calculated
    :param volume_description: volume object that describes the shape and size of the search volume
    :return: indices of neighboring points from the environment point cloud for each target point
    """
    volume_type = volume_description.get_type()
    if volume_type == Sphere.TYPE:
        return compute_sphere_neighborhood(env_pc, target_pc, volume_description.radius)
    elif volume_type == InfiniteCylinder.TYPE:
        return compute_cylinder_neighborhood(env_pc, target_pc, volume_description.radius)
    raise ValueError('Neighborhood computation error because volume type "{}" is unknown.'.format(volume_type))
