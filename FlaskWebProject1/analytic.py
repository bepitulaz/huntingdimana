"""
    This is the module for doing monster analysis.
"""
from experience import Experience

class Analytic:
    def __init__(self, map_list):
        self.map_list = map_list

    def filter_by_exp(self, player_level, exp_type):
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

    def __list_filter(self, map_data, monster_min_level, monster_max_level):
        """Filtering map data based on the level"""
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
