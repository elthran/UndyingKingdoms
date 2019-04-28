from undyingkingdoms.models.technologies import Technology

hierophant_technology = {
    'sacrifice i': Technology(name='sacrifice i',
                              required=500,
                              tier=1,
                              max_level=1,
                              description='Each thieves den grants an additional thief.'),
    'sacrifice ii': Technology(name='sacrifice ii',
                               required=750,
                               tier=2,
                               max_level=1,
                               description='Each thieves den grants an additional thief.'),
    'sacrifice iii': Technology(name='sacrifice iii',
                                required=1000,
                                tier=3,
                                max_level=1,
                                description='Each thieves den grants an additional thief.')
}
