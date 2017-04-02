"""
    This is the module for doing monster analysis.
"""
from __future__ import division
import math
from FlaskWebProject1.experience import Experience, ExpRate, ExpTable

class Analytic(object):
    """Class for organizing all methods of monster analysis."""
    def __init__(self, map_list):
        self.map_list = map_list

    def filter_by_exp(self, player_level, exp_type):
        """Filter by experience with renewal mechanism.
        This method is not used in RO Gravindo with classical mechanism."""
        if exp_type == Experience.FULL:
            monster_max_level = player_level + 2
            monster_min_level = player_level - 5
        elif exp_type == Experience.NINETY_FIVE:
            monster_max_level = player_level - 6
            monster_min_level = player_level - 10
        elif exp_type == Experience.NINETY:
            monster_max_level = player_level - 11
            monster_min_level = player_level - 15
        elif exp_type == Experience.OVER:
            monster_max_level = player_level + 10
            monster_min_level = player_level + 3

        return self.__list_filter(self.map_list, monster_min_level, monster_max_level)

    def classic_exp_filter(self, player_level, target_exp):
        """Filter the monsters with classic experience mechanism."""
        lvl_row = [row for row in ExpTable.BASE if row[0] == player_level]
        next_exp = lvl_row[0][2]

        if target_exp == ExpRate.HUGE:
            max_exp = 6
            min_exp = 4
        elif target_exp == ExpRate.LARGE:
            max_exp = 4
            min_exp = 2
        elif target_exp == ExpRate.SMALL:
            max_exp = 2
            min_exp = 1
        elif target_exp == ExpRate.LITTLE:
            max_exp = 1
            min_exp = 0.1
        elif target_exp == ExpRate.SAD:
            max_exp = 0.1
            min_exp = 0.001

        return self.__list_filter_by_exp(self.map_list, min_exp, max_exp, next_exp)

    def __list_filter_by_exp(self, map_data, monster_min_exp, monster_max_exp, next_exp):
        """Filtering map data based on monster exp.
        It is suitable for classic mechanism which always gain 100% experience."""
        filtered = []
        for mapitem in map_data:
            # Monster selection
            exp_to_percent = [(x/next_exp)*100 for x in mapitem['map_monster_exp']]
            if max(exp_to_percent) >= monster_min_exp and max(exp_to_percent) <= monster_max_exp:
                last_monster = ""
                monster_list = []
                for monster in mapitem['map_monsters']:
                    # Grouping the same name of the monster
                    if monster['respawn'] == "Instant":
                        if monster['name'] != last_monster:
                            monster_list.append(monster)
                    else:
                        if monster['name'] != last_monster:
                            monster_list.append(monster)

                    last_monster = monster['name']

                mapitem['map_monsters'] = monster_list
                filtered.append(mapitem)

        return filtered

    def __list_filter(self, map_data, monster_min_level, monster_max_level):
        """Filtering map data based on the player level and monster level.
        It use renewal mechanism with penalty experience."""
        filtered = []
        for mapitem in map_data:
            # Monster selection
            if max(mapitem['map_level']) <= monster_max_level and max(mapitem['map_level']) >= monster_min_level:
                last_monster = ""
                monster_list = []
                for monster in mapitem['map_monsters']:
                    # Grouping the same name of the monster
                    if monster['respawn'] == "Instant":
                        if monster['name'] != last_monster:
                            monster_list.append(monster)
                    else:
                        if monster['name'] != last_monster:
                            monster_list.append(monster)

                    last_monster = monster['name']

                mapitem['map_monsters'] = monster_list
                filtered.append(mapitem)

        return filtered
