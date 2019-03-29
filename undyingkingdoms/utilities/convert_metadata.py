import pandas as pd
from undyingkingdoms.static.metadata import metadata, metadata_armies_all, metadata_armies_human, metadata_armies_elf, \
    metadata_armies_dwarf, metadata_armies_goblin
# from undyingkingdoms.static.metadata import *


def build_race_table():
    """Generate a spreadsheet of all race and background data."""

    modifiers = [mod for mod in dir(metadata) if "modifier" in mod]
    mod_dfs = {' '.join(mod.split('_')).title(): pd.DataFrame(getattr(metadata, mod)) for mod in modifiers}

    cols = ["Race", "Background", "Modifier Label", "Modifier Type", "Modifier Value", "Modifier Description"]
    df = pd.DataFrame(index=range(44), columns=cols)

    i = 0
    for mod_key, mod_df in mod_dfs.items():
        for r_b in mod_df:
            if r_b in metadata.metadata_races:
                df.Race[i] = r_b
            else:  # col is Background
                df.Background[i] = r_b
            df['Modifier Type'][i] = mod_key
            df['Modifier Label'][i] = mod_df[r_b][0]
            df['Modifier Value'][i] = mod_df[r_b][1]
            i += 1

    for race in metadata.metadata_races:
        if race not in df.Race.dropna().unique():
            df.Race[i] = race
            i += 1

    for background in metadata.metadata_backgrounds:
        if background not in df.Background.dropna().unique():
            df.Background[i] = background
            i += 1
    df = df.sort_values(['Race', 'Background', 'Modifier Label']).reset_index(drop=True)

    for name in df['Modifier Label']:
        try:
            row = df['Modifier Label'] == name
            val = df.loc[row, "Modifier Value"].iloc[0]
            if int(val) == val:  # is a fixed value
                if val > 0:
                    val = '+' + str(int(val))
            else:  # is a percent
                val = int(val * 100)
                if val > 0:
                    val = '+' + str(val)
                val = str(val) + '%'
            label = df.loc[row, "Modifier Type"].iloc[0][:-9]
            df.loc[row, 'Modifier Description'] = '{}: {} {}'.format(name, val, label)
        except IndexError:
            pass

    df.to_csv('undyingkingdoms/static/dist/modifiers.csv')


def build_modifier_table():
    """Generate a spreadsheet of all army data."""
    gen_armies = metadata_armies_all.generic_armies
    army_args = ['name', 'class_name', 'class_name_plural', 'total', 'trainable_per_day',
                 'gold', 'iron', 'wood', 'upkeep', 'attack', 'defence', 'health', 'description']

    cols = ['Race', 'Name', 'Class Name', 'Class Name Plural', 'Total',
            'Trainable Per Day', 'Gold', 'Iron', 'Wood', 'Upkeep', 'Attack',
            'Defence', 'Health', 'Description']
    size = len(gen_armies) * len(metadata.metadata_races)
    df = pd.DataFrame(index=range(size), columns=cols)

    i = 0
    for k, v in gen_armies.items():
        for j, col in enumerate(cols[1:]):
            df.loc[i, col] = getattr(v, army_args[j])
        i += 1

    for race in metadata.metadata_races:
        mod = globals()['metadata_armies_' + race.lower()]
        army = getattr(mod, race.lower() + '_armies')
        for k, v in army.items():
            df.loc[i, 'Race'] = race
            for j, col in enumerate(cols[1:]):
                df.loc[i, col] = getattr(v, army_args[j])
            i += 1

    df.to_csv('undyingkingdoms/static/dist/armies.csv')
