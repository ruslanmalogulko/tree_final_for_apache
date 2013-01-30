from django.http import HttpResponseRedirect
from django.template import RequestContext, loader


from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext
import xml.etree.ElementTree as ET
from apps.models import TreeStore, VersionStore, RestoreActions
import MySQLdb, sys, os, random
import ldap

from tree.forms import UploadFileForm

import tempfile, zipfile, datetime
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

import xml.etree.ElementTree as ET
from xml.dom.minidom import Document

# this ads comments to test git
def login(request):
    global urls
    urls = []
    errors = []
    login = ''
    password = ''
    username = ''
    request.session.clear()
    server = 'ldap://172.22.64.41:389'

    base_dn='ou=Technical,dc=nc,dc=local'

    if 'login' in request.POST:
        user = request.POST['login']
        username = r"nc.local\%s" % user
        if not user:
            errors.append('It seems to be no login was entered')
    if 'password' in request.POST:
        password = request.POST['password']
        if not password:
            errors.append('It seems to be no password was entered')

    if len(errors) == 0 and 'login' in request.POST and 'password' in request.POST:    
        l = ldap.initialize(server)
        l.protocol_version = 3
        try :
            l.simple_bind_s(username,password)
            searchFilter = "cn=*"
            retrieveAttributes = ['cn']
            results = l.search_s(base_dn,ldap.SCOPE_SUBTREE,searchFilter, retrieveAttributes)
            errors.append("Access granded")
            request.session['user'] = user
            print request.session.values()
            print urls
            return redirect('/tree')
        except ldap.LDAPError:
            print ldap.LDAPError
            errors.append("Permission denied by Active Directory")

    return render_to_response('login.html',
        {'errors': errors})


def tree(request):
    return render_to_response('tree.html', {}, context_instance=RequestContext(request))

# Root path for all nodes
root_path = TreeStore.objects.filter(level=1)[0]

# Select all items from Testtree model and form lines array with nodes paths
base = TreeStore.objects.all()
# lines = []
# for line in base:
#     lines.append(line.path)
# lines.sort()


# Gives us generated xml document 
def xml_data(request): 

    
    if request.POST:
        if 'id' in request.POST:
            if request.POST['id'] == "0":
                print "POST id: %s" % request.POST['id']
                root_path = TreeStore.objects.filter(level=1)[0]
            else:
                print 'there is post for xml_data'
                print "POST id: %s" % request.POST['id']
                root_path = TreeStore.objects.get(fullpath=request.POST['id'])
                print 'root path %s' % root_path.fullpath
    # else:
    #     root_path = TreeStore.objects.filter(level=1)[0]
    doc = Document()
    root = doc.createElement('root')
    doc.appendChild(root)         
    
    child_list = getChild(root_path)
    # print "STart parsing child_list"
    for f in child_list:
        # print("Fullpath %s" % f.fullpath)
        if isdir(f):
            elem = doc.createElement('item')
            elem.setAttribute('id', f.fullpath)
            elem.setAttribute('state', 'closed')
            elem.setAttribute('rel', 'folder')
            nodecontent = doc.createElement('content')
            elem.appendChild(nodecontent)
            nodename = doc.createElement('name')
            nodecontent.appendChild(nodename)
            nodetext = doc.createTextNode(f.fullpath.split('/')[-1])
            # print "DIR: %s" % f.fullpath.split('/')[-1]
            nodename.appendChild(nodetext)
        else:
            print "FILE: %s" % f.fullpath.split('/')[-1]
            elem = doc.createElement('item')
            elem.setAttribute('parent_id', f.fullpath)
            elem.setAttribute('id', f.fullpath)
            # elem.setAttribute('state', 'open')
            elem.setAttribute('rel', 'file')
            nodecontent = doc.createElement('content')
            elem.appendChild(nodecontent)
            nodename = doc.createElement('name')
            nodecontent.appendChild(nodename)
            nodetext = doc.createTextNode(f.fullpath.split('/')[-1])
            # print "FILE: %s" % f.fullpath.split('/')[-1]
            nodename.appendChild(nodetext)
        root.appendChild(elem)

    # print(doc.toprettyxml())
    # print "End of xml_data"
    return HttpResponse(doc.toprettyxml(), mimetype="application/xhtml+xml")


# def xml_test(request): 
#     doc = Document()
#     root = doc.createElement('root')
#     doc.appendChild(root)         
#     # print lines
#     def makenode(path):
#         # "Return a document node contains a directory tree for the path."
#         node = doc.createElement('item')
#         node.setAttribute('id', path)
#         node.setAttribute('rel', 'folder')
#         nodecontent = doc.createElement('content')
#         node.appendChild(nodecontent)
#         nodename = doc.createElement('name')
#         nodecontent.appendChild(nodename)
#         nodetext = doc.createTextNode(path.split('/')[-1])
#         nodename.appendChild(nodetext)
#         for f in os.listdir(path):
#             fullname = os.path.join(path, f)
#             if os.path.isdir(fullname):
#                 elem = makenode(fullname)
#             # else:
#             #     elem = doc.createElement('item')
#             #     elem.setAttribute('parent_id', path)
#             #     elem.setAttribute('id', fullname)
#             #     elem.setAttribute('rel', 'file')
#             #     nodecontent = doc.createElement('content')
#             #     elem.appendChild(nodecontent)
#             #     nodename = doc.createElement('name')
#             #     nodecontent.appendChild(nodename)
#             #     nodetext = doc.createTextNode(f)
#             #     nodename.appendChild(nodetext)
#                 node.appendChild(elem) #if want, backup after
#         return node
#     root.appendChild(makenode('/home/russel/Downloads'))
#     print(doc)
#     return HttpResponse(doc.toprettyxml(), mimetype="application/xhtml+xml")


# Get all child elements for node with path 
def getChild(path):
    data = TreeStore.objects.filter(level=path.level+1, fullpath__contains=path.fullpath)
    # print(data)
    childs = []
    for item in data:
        if path.fullpath!=item.fullpath:
            print item.fullpath
            childs.append(item)
            # print str(vars(childs))

    # for line in lines:
    #     if path in line and len(line) != len(path):
    #         path_splitted = path.split('/')
    #         line_splitted = line.split('/')
    #         new_path = ''
    #         for item in line_splitted[1:len(path_splitted)+1]:
    #             new_path += '/' + item
    #         if new_path not in childs:
    #             childs.append(new_path)          
    return childs
# print(getChild(path))


# Checks node type. Is node a directory? (Boolean)
def isdir(path):
    if (path.file_is==0):
        return True
    else:
        return False
# print(isdir(path))


# For using in form for file uploads at the future (optional)
def upload_file(request):
    form = UploadFileForm(request.POST)
    if request.POST:
        print "there is post"
    if request.FILES:
        print "there is files"
    print form.is_valid()
    if request.POST:
        print request.POST['id']
        file_data = request.FILES['file']
        print request.POST['title']
        print file_data.size
    return render_to_response('upload.html', {'form' : form})


def post(request):
    # id = ''
    # if request.POST:
    #     print "there is post"
    #     id = request.POST['id']
    #     # request.session['idn'] = id
    # if request.FILES:
    #     print "there is files"
    if request.POST['id']:
        id = request.POST['id']
        print id
        p = RestoreActions(version_store_id=id, dt_created=datetime.datetime.now())
        p.save()
    # print request.session['idn']
        
    # if request.session['idn']:
    #     filename = request.session['idn']
    #     wrapper = FileWrapper(file(filename))
    #     response = HttpResponse(wrapper, content_type='application/zip')
    #     response['Content-Disposition'] = 'attachment; filename='+filename.split('/')[-1]
    #     response['Content-Length'] = os.path.getsize(filename)
    #     print response['Content-Length']
    # # return HttpResponse('Hello world')
    #     print filename
    return 


def show_child(request):
    print "there is /tree/childs"
    path = ''
    # if request.session['path']:
    #     path = request.session['path']
    childs = []
    elements = ''
    if request.GET:
        print "there is get"
    print "request.POST['id']: %s" % request.POST['id']
    path = request.POST['id']
    items = VersionStore.objects.filter(tree_store_id=TreeStore.objects.filter(fullpath=path))
    # if request.POST:
    #     print "there is post"
    #     # request.session['path'] = request.POST['id']
    #     print "request.POST['id']: %s" % request.POST['id']
    #     path = request.session['path']
    #     items = VersionStore.objects.filter(tree_store_id=TreeStore.objects.filter(fullpath=path))
        

    # print path
    # if path!='':
    #     childs = os.listdir(path)
    print items
    for item in items:
        print item.id
        print item.dt_created
        elements = '<li id="'+ str(item.id) + '" class="ui-widget-content">' +str(item.dt_created) + '</li>'
        print "ELements: %s" % elements

    # elements = '''<li class="ui-widget-content">2018-01-30 14:28:22+00:00</li>'''
    print elements
    return HttpResponse(elements)


# Sending file to the browser
def send_file(request):
    filename = '/home/russel/djcode/slideshow_2013_01_15.zip'
    wrapper = FileWrapper(file(filename))
    response1 = HttpResponse(wrapper, content_type='application/zip')
    response1['Content-Disposition'] = 'attachment; filename=test.zip'
    response1['Content-Length'] = os.path.getsize(filename)
    print response['Content-Length']
    return response


# Sending zip file to the browser
def send_zip(request):
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for index in range(10):
        filename = '/home/russel/djcode/slideshow_2013_01_15.zip'
        archive.write(filename, 'file%d.txt' % index)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response
