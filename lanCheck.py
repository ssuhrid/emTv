import tempfile
from smb.SMBConnection import SMBConnection

conn = SMBConnection('username','',' ',' ','',# use_ntlm_v2=True,
    # sign_options=SMBConnection.SIGN_WHEN_SUPPORTED,
    is_direct_tcp=True)

connected = conn.connect('192.168.1.10',445)
Response = conn.listShares(timeout=30)

for i in range(len(Response)):
    print("Share[",i,"] =", Response[i].name)

file_obj = tempfile.NamedTemporaryFile()
file_attributes, filesize = conn.retrieveFile('F_Rai\'s','/lan-tv/data/messages.txt',file_obj);
print filesize;

mess = [];
copy_file_object = open('data/copied.txt', 'w');
try:
    file_obj.seek(0);
    for i in range(0, 5):
        temp = file_obj.readline();
        copy_file_object.write(temp);
        mess.append(temp);
    # Close opend file
except:
    pass

for i in range(0,5):
    print mess[i];

