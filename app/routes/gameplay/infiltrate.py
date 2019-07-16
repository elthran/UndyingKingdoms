from math import floor
from random import randint, random

from flask import redirect, url_for, render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from app import app
from app.models.exports import Infiltration, County, Notification
from app.models.forms.infiltrate import InfiltrateForm
from app.routes.helpers import neither_allies_nor_armistices, not_self
from app.metadata.metadata import infiltration_missions


def probabilistic_round(x):
    """
    Takes a number and randomly rounds it up or down based on how close it is to either
    ie. 4.75 rounds up 75% of the time and down 25% of the time
    """
    return int(floor(x + random()))


@app.route('/gameplay/infiltrate/<int:county_id>', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/infiltrate.html')
@not_self
@neither_allies_nor_armistices
@login_required
def infiltrate(template, county_id):
    county = current_user.county
    espionage = county.espionage
    target = County.query.get(county_id)

    form = InfiltrateForm()
    form.county_id.data = county.id

    thieves = min(county.get_number_of_available_thieves(), espionage.thieves_per_mission)
    form.amount.choices = [(i + 1, i + 1) for i in range(thieves)]
    form.mission.choices = [(index, name) for index, name in enumerate(infiltration_missions)]

    duration_multiplier = espionage.duration_multiplier

    if form.validate_on_submit():
        mission = infiltration_missions[form.mission.data]
        report = Infiltration(county.id, target.id, county.kingdom.world.day,
                              county.day, mission, form.amount.data)
        report.save()

        chance_of_success = max(min(100 + form.amount.data - target.get_chance_to_catch_enemy_thieves(), 100), 0)

        gain_modifier = 1 + espionage.gain_modifier

        kingdom = county.kingdom
        target_kingdom = target.kingdom

        if chance_of_success >= randint(1, 100):
            # Add increase to war score
            kingdom.distribute_war_points(target_kingdom, form.amount.data)

            # End of war code
            report.success = True
            if mission == 'pilfer':
                # Thieves take minimum of 12 gold each
                gold_stolen = min(target.gold, randint(12 * form.amount.data,  probabilistic_round(20 * form.amount.data * gain_modifier * 1.25)))
                target.gold -= gold_stolen
                county.gold += gold_stolen
                report.pilfer_amount = gold_stolen
                report.duration = randint(8, 10) * duration_multiplier
                notification = Notification(
                    target,
                    "Thieves raided our lands",
                    f"They stole {gold_stolen} gold from our coffers.",
                )
            elif mission == 'burn crops':
                crops_burned = min(target.buildings['field'].total, probabilistic_round(form.amount.data * gain_modifier))
                target.buildings['field'].total -= crops_burned
                report.crops_burned = crops_burned
                report.duration = randint(14, 16) * duration_multiplier
                notification = Notification(
                    target,
                    "Thieves raided our lands",
                    f"They burned {crops_burned} of our {target.buildings['field'].class_name_plural.title()}."
                )
            elif mission == 'kill cattle':
                dairy_destroyed = min(target.buildings['pasture'].total, probabilistic_round(form.amount.data * gain_modifier))
                target.buildings['pasture'].total -= dairy_destroyed
                report.dairy_destroyed = dairy_destroyed
                report.duration = randint(14, 16) * duration_multiplier
                notification = Notification(
                    target,
                    "Thieves raided our lands",
                    f"They killed our cattle and destroyed {dairy_destroyed} of our "
                    f"{target.buildings['pasture'].class_name_plural.title()}."
                )
            elif mission == 'sow distrust':
                happiness_lost = min(target.happiness, probabilistic_round(form.amount.data * 3 * gain_modifier))
                target.happiness -= happiness_lost
                report.distrust = happiness_lost
                report.duration = randint(12, 14) * duration_multiplier
                notification = Notification(
                    target,
                    "Thieves raided our lands",
                    "They have caused some unrest in our kingdom.",
                )
            elif mission == 'scout military':
                report.get_troop_report(county, target, form.amount.data)
                report.duration = 3 * duration_multiplier
                notification = Notification(
                    target,
                    "Thieves raided our lands",
                    "They have found out some secrets regarding our military.",
                )
            elif mission == 'steal research':
                current_technology = target.research_choice
                research_stolen = min(current_technology.current, probabilistic_round(form.amount.data * 10 * gain_modifier))
                current_technology.current -= research_stolen
                county.research += research_stolen
                report.research_stolen = research_stolen
                report.duration = randint(6, 8) * duration_multiplier
                notification = Notification(
                    target,
                    "Thieves raided our lands",
                    f"They have stolen {research_stolen} of our research.",
                )
            else:
                raise KeyError("You tried to execute a mission that doesn't exits.")
        else:
            target_kingdom.distribute_war_points(kingdom, max(1, form.amount.data // 2))
            notification = Notification(
                target,
                f"You caught enemy thieves from {county.name}",
                "You caught them before they could accomplish their task",
            )
            report.duration = randint(16, 18) * duration_multiplier
            report.success = False
        notification.category = "Infiltration"
        notification.save()

        return redirect(url_for('infiltration'))

    return render_template(template, target=target, form=form)
