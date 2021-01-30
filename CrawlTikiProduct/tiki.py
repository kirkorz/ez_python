import requests as req
import json 
import pymongo

connectstring='mongodb://localhost:27017/cdcll2021'
myclient = pymongo.MongoClient(connectstring)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
root_urls = ['https://tiki.vn/api/v2/products?limit=48&category=1815&page='+str(i) for i in range(1,4)]
product_url = 'https://tiki.vn/api/v2/products/'
product_id =  []
usercomment = 'https://tiki.vn/api/v2/reviews?product_id={pid}&page={page}&limit=10&include=comments'
def item(id):
    product = {}
    p_url = product_url+str(id)
    res = json.loads(req.get(p_url,headers=headers).text)
    product['_id'] = res['id']
    product['name'] = res['name']
    product['price'] = res['price']
    product['productset_group_name'] = res['productset_group_name']
    product['description'] = res['description']
    product['specifications'] = res['specifications']
    try:
        myclient['cdcl2021']['product'].insert_one(product)
        print('user ok')
    except:
        print('user err')
def user(id):
    for j in range(1,5):
        u_url = usercomment.format(pid=id,page=j)
        res = json.loads(req.get(u_url,headers=headers).text)['data']
        for i in res:
            user = {}
            danhgia = {}
            user['_id'] = i['created_by']['id']
            user['name'] = i['created_by']['name']
            danhgia['user'] = user['_id']
            danhgia['product'] = id
            danhgia['content'] = i['content']
            danhgia['rating'] = i['rating']
            danhgia['purchased'] = i['created_by']['purchased']
            try:
                myclient['cdcl2021']['user'].insert_one(user)
                print('user ok')
            except:
                print('user danh gia err')
            try:
                myclient['cdcl2021']['danhgia'].insert_one(danhgia)
                print('danh gia gia ok')
            except: 
                print('danh gia err')
for url in root_urls:
    res = req.get(url,headers=headers)
    data = json.loads(res.text)['data']
    for i in data:
        item(i['id'])
        user(i['id'])













