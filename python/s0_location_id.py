import pandas as pd

location_ids = [
        ['연세로','1059469290920649'],
        ['홍대입구역','242033926'],
        ['강남역','215188434'],
        ['성수역','251871679'],
        ['합정역','251020013'],
        ['상수역','251074619'],
        ['한강','1821696111189493'],
        ['river-thames','199485697062285'],
        ['westminster','224652648'],
        ['seine-river','1631067606921988'],
        ['강변역','428047374'],
        ['과천중앙공원','154836595115953']
        ]

location_df = pd.DataFrame(location_ids, columns=['name','loc_id'])
path = '../../files/location_info/'
location_df.to_csv(path+'location_ids.csv', index=False)

location_ids = [
        ['amazon-river-brazil','623139961042534'],
        ['amazon-river','302062193'],
        ['hudson-river-nyc','254469222'],
        ['rhine-river','235397743'],
        ['jonggak-station','216985153'],
        ['종각역','252924192'],
        ['사당역','404000368'],
        ['잠실역','296783693'],
        ['신촌역','249552138'],
        ['안국역','219057635'],
        ['왕십리역','2188489'],
        ['chao-phraya-river','51486967'],
        ['spree-river-berlin','269016260224503'],
        ['charles-river-basin','237903058'],
        ['donau-river-wien-austria','254165578'],
        ['fiumo-tevere-river-rome-italy','313389933'],
        ['mississippi-river','283539423'],
        ['nile-river','214467585']
        ]

location_df = pd.DataFrame(location_ids, columns=['name','loc_id'])
path = '../../files/location_info/'
location_df.to_csv(path+'location_ids_2.csv', index=False)
