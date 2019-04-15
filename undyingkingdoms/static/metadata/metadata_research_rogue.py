from undyingkingdoms.models.technologies import Technology

rogue_technology = {
    'espionage i': Technology(name='espionage i',
                              required=500,
                              tier=1,
                              max_level=1,
                              description='All thievery operations are an additional 5% more likely to be successful.'),
    'espionage ii': Technology(name='espionage ii',
                               required=750,
                               tier=2,
                               max_level=1,
                               description='All thievery operations are an additional  10% more likely to be successful.'),
    'espionage iii': Technology(name='espionage iii',
                                required=1000,
                                tier=3,
                                max_level=1,
                                description='All thievery operations are an additional 10% more likely to be successful.')
}
