from random import randint

from flask import redirect, url_for, render_template
from flask_login import login_required, current_user
from flask_mobility.decorators import mobile_template

from undyingkingdoms import app
from undyingkingdoms.models import Infiltration, County, Notification
from undyingkingdoms.models.forms.infiltrate import InfiltrateForm
from undyingkingdoms.routes.helpers import not_allies, not_self
from undyingkingdoms.static.metadata.metadata import infiltration_missions, amount_of_thieves_modifier, \
    infiltration_results_modifier


@app.route('/gameplay/infiltrate/<int:county_id>', methods=['GET', 'POST'])
@mobile_template('{mobile/}gameplay/infiltrate.html')
@not_self
@not_allies
@login_required
def infiltrate(template, county_id):
    if county_id == current_user.county.id:
        return redirect(url_for('overview'))
    target = County.query.get(county_id)
    county = current_user.county

    form = InfiltrateForm()
    form.county_id.data = current_user.county.id
    max_thieves = 3 + amount_of_thieves_modifier.get(current_user.county.race, ("", 0))[1] + amount_of_thieves_modifier.get(current_user.county.background, ("", 0))[1]
    thieves = min(current_user.county.get_number_of_available_thieves(), max_thieves)
    form.amount.choices = [(i + 1, i + 1) for i in range(thieves)]
    form.mission.choices = [(index, name) for index, name in enumerate(infiltration_missions)]

    if form.validate_on_submit():
        mission = infiltration_missions[form.mission.data]
        report = Infiltration(current_user.county.id, target.id, current_user.county.kingdom.world.day,
                              current_user.county.day, mission, form.amount.data)
        report.save()

        chance_of_success = max(min(100 + form.amount.data - target.get_chance_to_catch_enemy_thieves(), 100), 0)

        gain_modifier = 1 + infiltration_results_modifier.get(county.race, ("", 0))[1] + infiltration_results_modifier.get(county.background, ("", 0))[1]

        if chance_of_success >= randint(1, 100):
            # Add increase to war score
            war = None
            kingdom = county.kingdom
            for each_war in kingdom.wars:
                if each_war.get_other_kingdom(kingdom) == target.kingdom:  # If this is true, we are at war with them
                    war = each_war
                    break
            if war:
                if war.kingdom_id == kingdom.id:
                    war.attacker_current += form.amount.data
                    if war.attacker_current >= war.attacker_goal:
                        kingdom.war_won(war)
                        war.status = "Won"
                else:
                    war.defender_current += form.amount.data
                    if war.defender_current >= war.defender_goal:
                        target.kingdom.war_won(war)
                        war.status = "Lost"
            # End of war code
            report.success = True
            if mission == 'pilfer':
                gold_stolen = int(min(randint(12 * form.amount.data, 20 * form.amount.data * gain_modifier) * 1.25, target.gold))
                target.gold -= gold_stolen
                county.gold += gold_stolen
                report.pilfer_amount = gold_stolen
                report.duration = randint(8, 10)
                notification = Notification(target.id,
                                            "Thieves raided our lands",
                                            f"They stole {gold_stolen} gold from our coffers.",
                                            county.kingdom.world.day)
            elif mission == 'burn crops':
                crops_burned = min(target.buildings['field'].total, form.amount.data * gain_modifier)
                target.buildings['field'].total -= crops_burned
                report.crops_burned = crops_burned
                report.duration = randint(14, 16)
                notification = Notification(target.id,
                                            "Thieves raided our lands",
                                            f"They burned {crops_burned} of our crops.",
                                            county.kingdom.world.day)
            elif mission == 'sow distrust':
                happiness_lost = min(target.happiness, form.amount.data * 3 * gain_modifier)
                target.happiness -= happiness_lost
                report.distrust = happiness_lost
                report.duration = randint(12, 14)
                notification = Notification(target.id,
                                            "Thieves raided our lands",
                                            "They have caused some unrest in our kingdom.",
                                            county.kingdom.world.day)
            elif mission == 'scout military':
                report.get_troop_report(county, target, form.amount.data)
                report.duration = 3
                notification = Notification(target.id,
                                            "Thieves raided our lands",
                                            "They have found out some secrets regarding our military.",
                                            county.kingdom.world.day)
            elif mission == 'steal research':
                current_technology = target.technologies[target.research_choice]
                research_stolen = min(current_technology.current, form.amount.data * 10 * gain_modifier)
                current_technology.current -= research_stolen
                county.research += research_stolen
                report.research_stolen = research_stolen
                report.duration = randint(6, 8)
                notification = Notification(target.id,
                                            "Thieves raided our lands",
                                            f"They have stolen {research_stolen} of our research.",
                                            county.kingdom.world.day)
        else:
            notification = Notification(target.id, f"You caught enemy thieves from {current_user.county.name}",
                                        "You caught them before they could accomplish their task",
                                        county.kingdom.world.day)
            report.duration = randint(16, 18)
            report.success = False
        notification.category = "Infiltration"
        notification.save()

        return redirect(url_for('infiltration'))

    return render_template(template, target=target, form=form)
