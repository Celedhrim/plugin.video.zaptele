from xbmcswift2 import Plugin
import urllib2
import CommonFunctions
common = CommonFunctions
common.plugin = "Zap-tele.com-1.0"

ZAP_URL = 'http://www.zap-tele.com'
TELE_CAT = '2'
ACTU_CAT = '3'

plugin = Plugin()
storage = plugin.get_storage('storage', TTL=1200)

def get_category(category):
	page = urllib2.urlopen(ZAP_URL + '/posts?category_id=' + category)
	html = page.read()
	div = common.parseDOM(html, "div", attrs = { "class": "caption" })
	clean = common.parseDOM(div, "h2")
	links = common.parseDOM(clean, "a" , ret = "href")
	return links

def video_info(link):
    page = urllib2.urlopen(ZAP_URL + link)
    html = page.read()
    vurl = common.parseDOM(html, "video", ret = "src")[0]
    vtitle = common.parseDOM(html, "title")[0]
    vtitle = common.replaceHTMLCodes(vtitle)
    vthumb = common.parseDOM(html, "video", ret = "poster")[0]
    vinfo = common.parseDOM(html, "p")[0]
    vinfo = common.stripTags(vinfo)
    return {
        'url': vurl,
        'title': vtitle,
        'thumb': vthumb,
        'info': vinfo
        }

	page = urllib2.urlopen(ZAP_URL + link)
	html = page.read()
	vurl = common.parseDOM(html, "video", ret = "src")[0]
	vtitle = common.parseDOM(html, "title")[0]
	vtitle = common.replaceHTMLCodes(vtitle)
	vthumb = common.parseDOM(html, "video", ret = "poster")[0]
	vinfo = common.parseDOM(html, "p")[0]
	vinfo = common.stripTags(vinfo)
	return {
		'url': vurl,
		'title': vtitle,
		'thumb': vthumb,
		'info': vinfo
		}

def merge_cat(tv,actu):
	num = len(tv)
	i = 0
	actutv = []
	while i < 12:
		actutv.append(tv[i])
		actutv.append(actu[i])
		i = i + 1
	return actutv

def get_items(links):
	result = []
	for link in links:
		video = video_info(link)
		newitem = {
			'label': video['title'],
			'thumbnail': video['thumb'],
			'info': {
				'plot':video['info'],
			},
			'path': video['url'],
			'is_playable': True
		}

		result.append(newitem)
	return result	

@plugin.route('/')
def index():
	items = [
		{'label': plugin.get_string(30001), 'path': plugin.url_for('show_label', label='all')},
		{'label': plugin.get_string(30003), 'path': plugin.url_for('show_label', label='actu')},
		{'label': plugin.get_string(30002), 'path': plugin.url_for('show_label', label='tv')},	
	]
	return items

if 'tv_items' in storage:
        tv_items = storage['tv_items']
else:
        rep = get_items(get_category(TELE_CAT))
        storage['tv_items'] = rep
        storage.sync()
        tv_items = storage['tv_items']

if 'actu_items' in storage:
        actu_items = storage['actu_items']
else:
        rep = get_items(get_category(ACTU_CAT))
        storage['actu_items'] = rep
        storage.sync()
        actu_items = storage['actu_items']

if 'all_items' in storage:
        all_items = storage['all_items']
else:
        rep = merge_cat(tv_items,actu_items)
        storage['all_items'] = rep
        storage.sync()
        all_items = storage['all_items']


@plugin.route('/labels/<label>/')
def show_label(label):
        if label == 'all':
                items = all_items
        elif label == 'actu':
                items = actu_items
        else:
                items = tv_items

        return items



if __name__ == '__main__':
    plugin.run()
