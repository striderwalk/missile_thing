import math


def control_missile(missile, plane, dt):
    m2p = -missile.position + plane.position

    t = math.atan2(m2p.y, m2p.x)

    if not missile.has_seen_plane:

        missile.heading = t
        missile.target_heading = t

    missile.target_heading = t
