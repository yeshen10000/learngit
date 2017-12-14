import requests
import re
import os



class Tools:
    removeImg = re.compile('<img.*?>')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>|<br>')
    replaceTd = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceExtraTag = re.compile('<.*?>')


    def remove(self,te):
        te = re.sub(self.removeImg,'',te)
        te = re.sub(self.removeAddr,'',te)
        te = re.sub(self.replaceLine,'\n',te)
        te = re.sub(self.replaceTd,'\t',te)
        te = re.sub(self.replacePara,'\n  ',te)
        te = re.sub(self.replaceExtraTag,'',te)
        return  te.strip()

def getHTML(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""

def getTitle(html):
	pattern = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
	result = re.search(pattern,html)
	if result:
		#print(result.group(1))#这里的group(0)表示的是整个得到的第一次匹配结果，group(1)表示的是第一组括号匹配得到的结果，注意上面的表达式中是有（）的
		return result.group(1).strip()
	else:
		return ""

def getPageNum(html):
	pattern = re.compile(r'<li class="l_reply_num".*?</span>.*?<span.*?>(.*?)</span>',re.S)
	result = pattern.search(html)
	if result:
		#print(result.group(0))
		return result.group(1).strip()
	else:
		return ""

def getContent(html):
	textTools = Tools()
	pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>',re.S)
	result = pattern.findall(html)#findall函数返回的是列表形式的字串，没有分组信息
	print(textTools.remove(result[1]))
	

def main():
	url ="https://tieba.baidu.com/p/3138733512?see_lz=1&pn=1"
	html = getHTML(url)
	title = getTitle(html)
	pageNum = getPageNum(html)
	getContent(html)
main()
