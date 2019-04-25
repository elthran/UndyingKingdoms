from undyingkingdoms.models.technologies import Technology

rogue_technology = {
    'espionage i': Technology(name='espionage i',
                              required=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'espionage ii': Technology(name='espionage ii',
                               required=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'espionage iii': Technology(name='espionage iii',
                                required=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
