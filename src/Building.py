import math


class Building:
    def __init__(
        self, bldgarea=0, height=0, elev=0, cls=0, numfloor=0, numbldg=0, lat=0, lon=0, x=0, y=0
    ):
        """Initialize a building instance"""
        self.bldgarea = bldgarea  # Double: Building area sqft
        self.height = height  # Double: Building height to roof ft
        self.elev = elev  # Double: Base elevation from sea level ft
        self.cls = cls  # str: Class of building
        self.numfloor = numfloor  # Int: Number of floors per building
        self.numbldg = numbldg  # Int: Number of buildings per lot
        self.lon = lon  # longitude
        self.lat = lat  # latitude
        self.x = x  # x-coordinate on the floodmap
        self.y = y  # y_coordinate on the floodmap

    def damage_area(self, h):
        """Takes in inundation depth h and returns the damaged area"""
        if self.height > 0 and self.numbldg > 0 and self.numfloor > 0:
            if h <= self.elev:
                return 0
            elif (h - self.elev) > self.height:
                return self.bldgarea
            else:
                floor_area = self.bldgarea / self.numbldg / self.numfloor
                floor_height = self.height / self.numfloor
                floor_inun = math.ceil((h - self.elev) / floor_height)
                area_inun = floor_inun * floor_area * self.numbldg
                if area_inun > self.bldgarea:
                    return self.bldgarea
                else:
                    return area_inun
        else:   # Eliminate buildings with badly shaped properties
            return 0

    def damage_estim(self, h):
        """Takes in inundation depth h and returns a damage loss"""
        value = 0
        # Using median damage from Aertz 2013 ($/m2)

        c = 0.092903  # m2 per sqft
        if not(isinstance(self.cls, str)):
            return 0
        if any(("A" in self.cls, "B" in self.cls)):
            value = 1550 * c
        elif any(
            (
                "C" in self.cls,
                "D" in self.cls,
                "L" in self.cls,
                "N" in self.cls,
                "R" in self.cls,
                "S" in self.cls,
            )
        ):
            value = 2300 * c
        elif "E" in self.cls:
            value = 650 * c
        elif "F" in self.cls:
            value = 850 * c
        elif "G" in self.cls:
            value = 850 * c
        elif "H" in self.cls:
            value = 1450 * c
        elif "I" in self.cls:
            value = 1400 * c
        elif "J" in self.cls:
            value = 2750 * c
        elif "K" in self.cls:
            value = 2100 * c
        elif "M" in self.cls:
            value = 700 * c
        elif any(("O" in self.cls, "Y" in self.cls, "Z" in self.cls)):
            value = 1650 * c
        elif "P7" in self.cls:
            value = 700 * c
        elif "P8" in self.cls:
            value = 2650 * c
        elif "P" in self.cls:
            value = 1850 * c
        elif "Q" in self.cls:
            value = 1650 * c
        elif "W" in self.cls:
            value = 3300 * c
        loss = value * self.damage_area(h)
        return loss


def get_building_damage(building, flood=[], flood_elev=0):
    """
    Getting the estimated building damage.
    Input:
    (building) instance from Building class
    (flood) flood map
    (flood_elev) flood elevation if map is not provided
    """
    if len(flood) != 0:
        flood_elev = flood[building.y, building.x] * 3.28084  # Convert m to ft
        damage = building.damage_estim(flood_elev)
    else:
        damage = building.damage_estim(flood_elev)
    return damage


def get_total_damage(region, flood=[], flood_elev=0):
    """
    Getting the total building damage in the region.
    Input:
    (region) A dictionary of instances from Building class
    (flood) flood map
    (flood_elev) flood elevation if map is not provided
    """
    total_damage = 0
    for key in region:
        dmg = get_building_damage(region[key], flood, flood_elev)
        total_damage += dmg
    return total_damage