# to SEND data from s3 to local file
from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
import pycurl
import certifi
import os
import time
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
filepath = form.getvalue('filepath')
#fi="'"+f+"'"
a=form.getvalue('accessKey')
s=form.getvalue('secretKey')
b=form.getvalue('bucketName')
u=form.getvalue('fileUrl')
op=form.getvalue('checkOption')

class FileReader:
    def __init__(self, fp):
        self.fp = fp
    def read_callback(self, size):
        return self.fp.read(size)
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
    
    print "<button type=\"button\" onclick=\"location.href='http://localhost:8000/InputPage.html'\">Try Again </button>"
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
            
    print 'hello'
    
    def doWork():
        #u="https://s3-us-west-2.amazonaws.com/medhabucket1/test/sample.xlsx"
        fp = open(filepath, "rb")
        filename = fp.name
        statbuf = os.stat(filename)
        changeTime = statbuf.st_mtime
        fp.close()
        while True:
                fp = open(filepath, "rb")
                filename = fp.name
                statbuf = os.stat(filename)
                newTime = statbuf.st_mtime 
                if newTime!=changeTime:
                        changeTime = newTime
                        print "Modification time:",changeTime 
                        print "last modified: %s" % time.ctime(changeTime)
                        
                        c = pycurl.Curl()
                        c.setopt(pycurl.CAINFO, certifi.where())
                        c.setopt(pycurl.URL, u)
                        c.setopt(pycurl.UPLOAD, 1)
                        
                        if 1:
                            c.setopt(pycurl.READFUNCTION, FileReader(open(filename, 'rb')).read_callback)
                        else:
                            c.setopt(pycurl.READFUNCTION, open(filename, 'rb').read)
    
                        # Set size of file to be uploaded.
                        filesize = os.path.getsize(filename)
                        c.setopt(pycurl.INFILESIZE, filesize)
    
                        # Start transfer
                        print 'Uploading file %s to url %s' % (filename, u)
                        print "Modification time:",changeTime 
                        print "last modified: %s" % time.ctime(changeTime)
                        c.perform()
                        c.close()
                fp.close()
                time.sleep(10)      
                        
    doWork();
