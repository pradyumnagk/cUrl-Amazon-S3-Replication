# to GET data from s3 to local file
from boto.s3.connection import S3Connection
import pycurl
import certifi
import os
import time
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
filepath = form.getvalue('filepath')
a=form.getvalue('accessKey')
s=form.getvalue('secretKey')
b=form.getvalue('bucketName')
u=form.getvalue('fileUrl')


try:
    conn = S3Connection(a,s)
    server = conn.host
    bucket = conn.get_bucket(b)
except S3ResponseError:
    print "Content-Type: text/html\r\n"
    print "<html>"
    print "<body bgcolor:\"\#c1ceda\">"
    #print "<img src=\"../cgi-bin/banner-1.jpg\" alt=\"eebfkjembkf\" width=\"500\">"
    print "<h2>Oops, Invalid Credentials !</h2>"
    
    print "<button type=\"button\" onclick=\"location.href='http://localhost:8000/RestorePage.html'\">Try Again </button>"
    print "<button type=\"button\" onclick=\"location.href='http://localhost:8000/Grid.html'\">Go Home </button>"
    print "</body>"
    print "</html>"
else:
    urls = []
    preauth_response = {}
    options = { "transport" : "http" }
    for f in bucket.get_all_keys():
            print "- %s" % f.name
            url = "%s://%s/%s/%s" % (options['transport'],server,bucket.name,f.name)
            urls.append(url.rstrip())
            
    #u="https://s3-us-west-2.amazonaws.com/medhabucket1/test/hello1.docx"
    #for u in urls:
    fp = open(filepath, "wb")
    pc = pycurl.Curl()
    pc.setopt(pycurl.CAINFO, certifi.where())
    pc.setopt(pycurl.URL,u)
    pc.setopt(pycurl.FOLLOWLOCATION, 1)
    pc.setopt(pycurl.WRITEDATA, fp)
    pc.perform()
    print pc.getinfo(pycurl.HTTP_CODE), pc.getinfo(pycurl.EFFECTIVE_URL)
    
    print "Content-type:text/html\r\n\r\n"
    print '<html>'
    print '<head>'
    print '<title>Data Restore</title>'
    print '</head>'
    print '<body>'
    print " <h1>Your file is restored at :\" %s\" </h1>" %(filepath)
    
    # print cgi.escape(name)
    print '</body>'
    print '</html>'
    #preauth_response[u] = code
    #print "- %s" % code
