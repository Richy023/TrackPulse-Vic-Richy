def getVlineStopType(stopName, emoji=False):
    print(f'establishing stop type for {stopName}')
    if stopName.upper().endswith('RAILWAY STATION '):
        if emoji:
            return '<:vline:1241165814258729092>'
        else:
            return 'train'
    else:
        if emoji:
            return '<:coach:1241165858274021489>'
        else:
            return 'coach'