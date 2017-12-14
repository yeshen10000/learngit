import requests

url = 'http://www.baidu.com'
#url = 'http://www.xiami.com/'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
cookies = {'Cookie':'gid=149813674674138; _xiamitoken=5d1af3c92a90a0ccf689ad268931275d; _unsign_token=64e54c3d6b238581dc726cbaeaa1aece; user_from=1; cna=/v16EVJO0zMCAXL/KDZRlSxg; UM_distinctid=15ccfe886a3bb2-07544676650007-572f7b6e-1aeaa0-15ccfe886a4679; isg=Ao2N2Zuu6CB7K0wL_2RRzOSjhakHasE8G6U2t88SsSSTxq94l77NDZ7YZGdd; __utma=251084815.747644262.1498137368.1498137368.1498137368.1; __utmz=251084815.1498137368.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); login_method=mobilelogin; t_sign_auth=0; __XIAMI_SESSID=1b61a00239efecf3dce4833e732e99c4; CNZZDATA921634=cnzz_eid%3D986508935-1498134039-null%26ntime%3D1498198418; CNZZDATA2629111=cnzz_eid%3D2062625599-1498135444-null%26ntime%3D1498199580'}
try:
	r = requests.get(url)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	print(r.status_code)
except:
	print('wrong')