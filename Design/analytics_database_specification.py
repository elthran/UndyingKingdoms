GameState:
'''
Gamestate tables shouldn't be used in analysis. Only the User table will be if we want to look at more in-depth user data, such as comparing purchases of users for each retention grouping or by looking at play styles and pulling user age into the analysis. That way we don't need to duplicate this data into every table and they will be easy to read.
'''

User()
# Current summary for each user. Can be joined with other tables on user_id when they need more data. Only the rows needed for analysis will be listed here
join_date = DateTime
ages_completed = Integer # (starts at 0) Adds one each time the user starts a new age (monthly events). We can query ages_completed by months since account creation to see how active a user is long term
day1_retention = Integer # (starts -1) After 1 day, turns 1 if the user returned or 0 if the user didn't. That way we can easily see what % of users return after creating an account
day7_retention = Integer # (starts at -1) On the seventh day after creating an account, turns 1 if the user logged in that day or 0 if they didn't. Checks what % of users log in a week after account creation
lifetime_revenue_in_CAD = Float # Should match up with sum(revenue.amount_in_CAD for revenue in Revenue.query.filter_by(user_id=id).all())
country = String # (From metadata) If it possible to get country? Can we get it from their IP? What are the options here.

Analytics:

Activity()
# This should create a row on every session, being updated on a login or logout. At the end of each day we can build a DAU table from it, and we can routinely delete old entries here (likely end of each month).
# So when you log in a row is created. When you log out, it will update that row. If logout cant find a row to update, then it will have its own row and assume some things.
user_id = ForeignKey
login_time = TimeStamp # (Default null)
logout_time = TimeStamp # (Default null). On a log out it will populate. Otherwise it's assumed you are still logged in.
minutes_played = Integer # How long that session was. If it's unknown then we put Null or a default value? Need to look into Flask auto logging out expired sessions to improve this accuracy
ip = String # Do we need this? Can we get this? Might help locate duplicate accounts, allow blacklisting of users, stop certain spam attacks if one ip sends too many commands? Not sure here

DAU()
# One row for each user each day, if that user logged in that day. Sessions are built from Activity() table, ads_watched from Ads() table, etc.
user_id = ForeignKey
age_in_days = Integer # How old the account is in days
sessions = Integer # How many login events, ignoring ones which happen within 15 minutes of a previous one
minutes_played = Integer # How many minutes played that day. Sum of difference between each login/logout, taking a max if the gap is too large
ads_watched = Integer # Depends how ads are set-up. Could be ads_clicked, etc. That way we can look on a daily rate what % of users interact with ads

Transactions()
# Every time the user spends in-game currency on buildings or armies it creates a row
user_id = ForeignKey
days_in_age = Integer # How far into the current age it is. Purchases should different greatly between beginning to end
gold_available = Integer # When a purchase is made, we should see how much resources they have. That way we can compare purchases of rich counties to that of poor counties.
...
...
purchase = String # (should be selected from a metadata list so the strings always match) Eg. 'BuildingPurchase' or 'ArmyPurchase'
peasants = Integer # Amount of each item bought. Null if not applicable, otherwise 0 if applicable but not bought.
house = Integer # Amount, as above
...
...

Revenue()
# Every time the user spends real money it will create a row. Most likely this would only be donations since nothing in the game will cost real money.
user_id = ForeignKey
amount = Float # Always in USD
currency = String # (mapped from a list in metadata)
amount_in_CAD = Float # Might not be needed. But for amounts where they pay X in their currency and we receive CAD, we should know both
purchase  = String # (should be selected from a metadata list so the strings always match) Eg. 'Donation'

Battles()
# Every battle in the game should create a row. I'm wondering if this table should be shrunk and can be joined with the County table when we want to populate all the county details like race.
# This should give a recording of all battles so we can check for trends (this race wins higher %, this unit type sucks, etc.) as well as let me look into specific battles if a user complains.
days_in_age = Integer # How far into the current age we are
attacker_wins = Boolean
attack_type = String # (Selected from metadata) Eg. 'Standard' or 'Plunder'
attacker_id = ForeignKey # Not sure if this should be the user or the county
defender_id = ForeignKey # As above
attacker_power = Integer # Total attack power after calculations
defender_power = Integer # As above
attacker_race = String
defender_race = String
land_gained = Integer # (Default 0)
gold_gained = Integer
...
...
attacker_peasants = Integer # Amount of peasants attacker brought
...
...
defender_peasants = Integer # Ditto
...
...
attacker_peasants_dead = Integer
...
...
defender_peasants_dead = Integer
...
...

