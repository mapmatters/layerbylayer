import subprocess

project_id = 'supple-design-237807'
bucket_name = 'geoposts'
path = '/home/yong_inline/files/post_info/merge/'
file_nm = sys.argv[1]

# file로 저장 '{} {}'.format(1, 2)
cmd1 = "gsutil cp {}* gs://{}/".format(path, bucket_name)
subprocess.call(cmd1, shell=True)

# 저장한 file 다시 불러오기
cmd3 = "gsutil cp gs://{}/seoul_bas_polygon_modified.geojson /home/yong_inline/data/seoul_bas_polygon_modified.geojson".format(bucket_name)
subprocess.call(cmd3, shell=True)
bas = gpd.read_file('/home/yong_inline/data/seoul_bas_polygon_modified.geojson')
