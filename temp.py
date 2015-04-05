from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext, Context
import constants as cc
import re
#from ipv6app.forms import formOptions
#from ipv6app.models import Prefix

global htmltext
global inipv6address
global ipv6address
global ipv6address_truncate
global ipv6address_binary
global ipv4address_embedded
global firstipv4address_embedded
global ipv4address_embedded
global subnet
global network
global subnetmask
global network_binary
global osubnet
global oipv6address
global oipv6address_binary
global oipv6address_truncate
global onetwork

def custom_proc(request):
    global htmltext
    global inipv6address
    global ipv6address
    global ipv6address_truncate
    global ipv6address_binary
    global ipv4address_embedded
    global firstipv4address_embedded
    global ipv4address_embedded
    global subnet
    global network
    global subnetmask
    global network_binary
    global osubnet
    global oipv6address
    global oipv6address_binary
    global oipv6address_truncate
    global onetwork
    if request.method == 'POST':
        inipv6address = request.POST['inipv6address']
        #myForm = formOptions(request.POST)
    else:
        inipv6address = "::"
        #myForm = formOptions()
    ipv6address = inipv6address
    ipv6address_truncate = ""
    ipv6address_binary = ""
    ipv4address_embedded = ""
    firstipv4address_embedded = ""
    ipv4address_embedded = ""
    subnet = 0
    network = ""
    subnetmask = ""
    network_binary = ""
    htmltext = []
    
    htmltext.append(cc.starttable1+cc.startrow1+" Original Input"+cc.rowdivider1+inipv6address+cc.endrow1)

    response = convertinput(inipv6address)
    if not response:
        zalert('Bad Conversion.')
        return False

    oipv6address               = ipv6address
    oipv6address_truncate      = ipv6address_truncate
    oipv6address_binary        = ipv6address_binary
    #ofirstipv4address_embedded = firstipv4address_embedded
    #oipv4address_embedded      = ipv4address_embedded
    osubnet                    = subnet
    onetwork                   = str(network)
    #ztemp2=""
    flag = cc.hexstring.find(ipv6address_truncate[17:18])
    if (flag & 2):
        isglobal = "global"
    else:
        isglobal = "local"
    interfaceID=ipv6address_truncate[16:32]

    htmltext.append(cc.startrow1+" IPv6 Address"+cc.rowdivider1+ipv6address+"/"+str(subnet)+cc.endrow1)
    htmltext.append(cc.startrow1+" Network Prefix"+cc.rowdivider1+str(network)+cc.endrow1)
    htmltext.append(cc.startrow1+" InterfaceIdentifier"+cc.rowdivider1+interfaceID+"   G/L bit:"+isglobal+cc.endrow1)

    if firstipv4address_embedded != "...":
        htmltext.append(cc.startrow1+" Entered IPv4"+cc.rowdivider1+firstipv4address_embedded+cc.endrow1)
    if ipv4address_embedded != "...":
        htmltext.append(cc.startrow1+" Entered IPv4"+cc.rowdivider1+ipv4address_embedded+cc.endrow1)
    htmltext.append(cc.startrow1+" IPv6 Addr-bin"+cc.rowdivider1+ipv6address_binary+cc.endrow1)
    htmltext.append(cc.startrow1+" Subnet Mask"+cc.rowdivider1+subnetmask+cc.endrow1)
    htmltext.append(cc.startrow1+" Network Pfx-bin"+cc.rowdivider1+network_binary+cc.endrow1)

    checkmasks()
    htmltext.append(cc.closetable1)
    maskanalyze()
    htmltext.append(cc.closetable2)    
    return {
        'inipv6address' : inipv6address,
        'htmltext' : htmltext,
    }

def index(request):
    c = RequestContext(request,processors=[custom_proc])
    return render_to_response('ipv6app/index.html',c)
    
def about(request):
    return HttpResponse("Thank you for checking out Version 1.2<br>Built on:<li>Python 2.7</li><li>Django 1.8</li><li>MySql 5.x</li>")

def convertinput(this_ipv6address):
    global htmltext
    global inipv6address
    global ipv6address
    global ipv6address_truncate
    global ipv6address_binary
    global ipv4address_embedded
    global firstipv4address_embedded
    global ipv4address_embedded
    global subnet
    global network
    global subnetmask
    global network_binary
    global osubnet
    global oipv6address
    global oipv6address_binary
    global oipv6address_truncate
    global onetwork
    
    convertstring = this_ipv6address
    lastchar=""
    doublecolon=-1
    currentchunk=0
    chunk=[]
    currentoctet = 0
    firstoctet=[]
    octet=[]
    zchar2 = ""

    while (len(chunk)<9):
        chunk.append('')
    while (len(firstoctet)<4):
        firstoctet.append("")
        octet.append("")

    currentchar = 0
    while (currentchar < len(convertstring)):
        zchar = convertstring[currentchar:currentchar+1]
        if zchar == ".":
            if chunk[currentchunk] == "":
                zalert('Bad ipv4 address embedding!')
                return False
            if currentoctet>0:
                for ztemp in range (0,4):
                    firstoctet[ztemp]=octet[ztemp]
                currentoctet=0
            octet[currentoctet]=chunk[currentchunk]
            chunk[currentchunk]=''
            currentoctet += 1
            if currentchar+1 <= len(convertstring):
                for ztemp in range (currentchar+1, len(convertstring)):
                    lastchar=zchar2
                    zchar2=convertstring[ztemp:ztemp+1]
                    if zchar2 == ".":
                        if chunk[currentchunk] == "":
                            zalert('Bad ipv4 address embedding!')
                            return False
                        octet[currentoctet]=chunk[currentchunk]
                        chunk[currentchunk]=""
                        currentoctet += 1
                    elif zchar2 == ":" or zchar2 == "/":
                        if currentoctet<3:
                            zalert('Not enough octets in ipv4 address!')
                            return False
                        break
                    elif not re.match(r'[0-9]',zchar2):
                        zalert('Invalid char in ipv4 address!')
                        return False
                    else:
                        chunk[currentchunk]=chunk[currentchunk]+zchar2
                octet[currentoctet]=chunk[currentchunk]
                chunk[currentchunk]=''
                currentoctet += 1
                zchar=zchar2
                currentchar=ztemp
                chunk[currentchunk]=(hex(int(octet[0])).split('x')[1]).zfill(2)+(hex(int(octet[1])).split('x')[1]).zfill(2)
                currentchunk += 1
                
                if currentchunk>7:
                    zalert('More than 8 chunks!')
                    return False
                chunk[currentchunk]=(hex(int(octet[2])).split('x')[1]).zfill(2)+(hex(int(octet[3])).split('x')[1]).zfill(2)
            if currentchar >= len(convertstring):
                return True
        if zchar == "/":
            ztemp = convertstring.find("/")
            ztemp2=len(convertstring)-ztemp
            if ztemp2:
                zchar = convertstring[ztemp+1:ztemp+1+ztemp2]
            else:
                zchar="0"
            subnet = int(zchar)
            currentchar = len(convertstring)+1
            if (subnet>128) or (subnet<0):
                zalert('Bad prefix bits!')
                return False
        elif zchar == ":":
            if lastchar == ":":
                if doublecolon > -1:
                    zalert('More than 1 double colon!')
                    return False
                doublecolon=currentchunk
            while (len(chunk[currentchunk]) < 4):
                chunk[currentchunk]="0"+chunk[currentchunk]
            currentchunk += 1
            if currentchunk>7:
                zalert('More than 8 chunks!')
                return False
            chunk[currentchunk]=''
        elif re.match(r'[0-9AaBbCcDdEeFf]',zchar):
            if len(chunk[currentchunk])>3:
                zalert('Too many in chunk!')
                return False
            zchar=zchar.upper()
            chunk[currentchunk] = chunk[currentchunk]+zchar
        else:
            zalert('Illegal character in address['+zchar+']!')
            return False
        lastchar=zchar
        currentchar += 1
    while (len(chunk[currentchunk])<4):
        chunk[currentchunk]="0"+chunk[currentchunk]
    maxchunks=currentchunk
    currentchunk=0

    if maxchunks<7:
        if doublecolon == -1:
            zalert('Bad chunk count! Missing doublecolon?')
            return False
        for currentchunk in range(doublecolon,doublecolon+(7-maxchunks)):
            revchunk=0
            for revchunk in range (7,currentchunk,-1):
                if revchunk>0:
                    chunk[revchunk]=chunk[revchunk-1]
            chunk[revchunk]=""

    for currentchunk in range (0,8):
        while (len(chunk[currentchunk])<4):
            chunk[currentchunk]="0"+chunk[currentchunk]
    
    ipv6address=(chunk[0]+":"+chunk[1]+":"+chunk[2]+":"+chunk[3]+":"+chunk[4]+":"+chunk[5]+":"+chunk[6]+":"+chunk[7]).upper()
    ipv6address_truncate=(chunk[0]+chunk[1]+chunk[2]+chunk[3]+chunk[4]+chunk[5]+chunk[6]+chunk[7]).upper()
    ipv4address_embedded=octet[0]+"."+octet[1]+"."+octet[2]+"."+octet[3]
    firstipv4address_embedded=firstoctet[0]+"."+firstoctet[1]+"."+firstoctet[2]+"."+firstoctet[3]
    ipv6address_binary=hexToBin(ipv6address_truncate)
    subnetmask=""
    for ztemp in range (0,subnet):
        subnetmask=subnetmask+"1"
    while (len(subnetmask)<128):
        subnetmask=subnetmask+"0"

    network_binary=zand(ipv6address_binary,subnetmask)
    ztemp=binToHex(network_binary)
    network=zchunk(ztemp)
    return True

def checkmasks():
    global htmltext
    global inipv6address
    global ipv6address
    global ipv6address_truncate
    global ipv6address_binary
    global ipv4address_embedded
    global firstipv4address_embedded
    global ipv4address_embedded
    global subnet
    global network
    global subnetmask
    global network_binary
    global osubnet
    global oipv6address
    global oipv6address_binary
    global oipv6address_truncate
    global onetwork

    oipv6address_binary=ipv6address_binary
    details = Prefix.objects.all()
    htmltext.append(cc.startrow3+" Mask Mapping to reserved Addresses"+cc.endrow1)

    for detail in details:
        details_ip       = detail.ip
        details_mask     = detail.mask
        details_name     = detail.name
        details_possible = detail.possible
        details_flag     = detail.flag
        if details_ip == "":
            return True
        zchar=convertinput(details_ip)
        if not zchar:
            zalert('Bad details_ip Conversion.')
            return False
        #zprefix=ipv6address
        zprefix_bin=ipv6address_binary
        znetmask=subnetmask
        #zsubnet=subnet
        if details_mask != "":
            zchar=convertinput(details_mask)
            if not zchar:
                zalert('Bad details_mask Conversion.')
                return False
            znetmask=ipv6address_binary
            #zsubnet="non-contiguous"
        ztemp2=zand(znetmask,oipv6address_binary)
        if ztemp2 == zprefix_bin:
            if details_possible>50:
                zchar="Yes"
            elif details_possible>49:
                zchar="Probable"
            else:
                zchar="Possible"
        else:
            zchar="No"
        if zchar != "No":
            htmltext.append(cc.startrow1+details_ip+cc.rowdivider2+zchar+cc.rowdivider2+details_name+cc.endrow1)
            if details_flag == "6to4":
                #6to4;
                v4addr=getv4(oipv6address_truncate[4:12])
                istrue = isprivate(v4addr)
                #islegal=""
                if istrue:
                    islegal="illegal"
                else:
                    islegal="legal"
                if v4addr[0:9] == "192.88.99":
                    htmltext.append(cc.startrow2+"...6to4 Relay v4"+cc.rowdivider2+v4addr+cc.endrow1)
                else:
                    htmltext.append(cc.startrow2+"...6to4 Router v4"+cc.rowdivider2+v4addr+" - "+islegal+" for 6to4 site."+cc.endrow1)
            elif details_flag == "ISATAP":
                #ISATAP;
                v4addr=getv4(oipv6address_truncate[24:32])
                istrue = isprivate(v4addr)
                ispriv=""
                if istrue:
                    ispriv="Private"
                else:
                    ispriv="Public"
                htmltext.append(cc.startrow2+"...ISATAP host v4"+cc.rowdivider2+v4addr+" - "+ispriv+" ipv4 address."+cc.endrow1)
            elif details_flag == "EUI64":
                #EUI-64;
                MAC48 = oipv6address_truncate[17:23]+oipv6address_truncate[26:32]
                flag = cc.hexstring.find(oipv6address_truncate[17:18])
                flag2 = cc.hexstring[flag^2:flag^2+1]
                
                MAC48 = oipv6address_truncate[16:17] + flag2 +":"+ oipv6address_truncate[18:20] +":"+ oipv6address_truncate[20:22] +":"+ oipv6address_truncate[26:28] +":"+ oipv6address_truncate[28:30] +":"+ oipv6address_truncate[30:32]
                htmltext.append(cc.startrow1+"...MAC 48"+cc.rowdivider2+" Possible"+cc.rowdivider2+MAC48+cc.endrow1)
            elif details_flag == "SNM":
                #Solicited Node Multicast
                bit24=oipv6address_truncate[26:32]
                htmltext.append(cc.startrow1+"...24 bits"+cc.rowdivider1+bit24+cc.endrow1)
            elif details_flag == "v4compat":
                #v4 compatible address
                v4addr=getv4(oipv6address_truncate[24:32])
                istrue = isprivate(v4addr)
                ispriv=""
                if istrue:
                    ispriv="Private"
                else:
                    ispriv="Public"
                if v4addr == "0.0.0.0":
                    htmltext.append(cc.startrow2+"...v4 compatible v4"+cc.rowdivider2+v4addr+" - NOT v4-compatible."+cc.endrow1)
                else:
                    htmltext.append(cc.startrow2+"...v4 compatible v4"+cc.rowdivider2+v4addr+" - "+ispriv+" ipv4 address."+cc.endrow1)
            elif details_flag == "v4map":
                #v4 mapped address
                v4addr=getv4(oipv6address_truncate[24:32])
                istrue = isprivate(v4addr)
                ispriv=""
                if istrue:
                    ispriv="Private"
                else:
                    ispriv="Public"
                htmltext.append(cc.startrow2+"...v4 mapped v4"+cc.rowdivider2+v4addr+" - "+ispriv+" ipv4 address."+cc.endrow1)
            elif details_flag == "anyscope":
                #anyscope multicast address
                htmltext.append(cc.startrow1+cc.rowdivider1+"...Above is anyscope multicast ff0X::")

def isprivate(v4_address):
    v4addr = v4_address
    if (v4addr[0:2] == "10") or (v4addr[0:7] == "192.168") or (v4addr[0:6] == "172.16") or (v4addr == "0.0.0.0") or (v4addr[0:7] == "127.0.0") or (v4addr[0:15] == "255.255.255.255"):
        return True
    else:
        return False

def zalert(error_msg):
    global htmltext
    global inipv6address
    print "ERROR! "+error_msg
    print type(htmltext)
    htmltext.append('alert(Your Original Input '+inipv6address+' has an error.\nERROR! '+error_msg+')')
    #quit()
    return False

def binToHex(bin):
    ztemp3 = len(bin)
    if (((float(ztemp3) / 4) != int(ztemp3 / 4)) or (ztemp3 < 4) or (ztemp3 > 128)):
        zalert('Wrong bit length for hex conversion!')
        return False
    ztemp3=""
    for ztemp in range (0,len(bin),4):
        zchar=bin[ztemp:ztemp+4]
        ztemp2=(cc.binstring.find(zchar))/5
        ztemp3=ztemp3+cc.hexstring[ztemp2:ztemp2+1]
    return ztemp3

def hexToBin(hex):
    ztemp3=""
    for ztemp in range (0,len(hex)):
        zchar=hex[ztemp:ztemp+1]
        ztemp2=(cc.hexstring.find(zchar))*5
        ztemp3=ztemp3+cc.binstring[ztemp2:ztemp2+4]
    return ztemp3

def zand(and1, and2):
    if ((len(and1) != len(and2)) or (len(and1) != 128)):
        zalert("Can't AND non 128bit lengths!")
        return False
    ztemp3=""
    for ztemp in range(0,len(and1)):
        ztemp2=""
        if and1[ztemp:ztemp+1] == and2[ztemp:ztemp+1]:
            ztemp2=and1[ztemp:ztemp+1]
        else:
            ztemp2="0"
        ztemp3=ztemp3+ztemp2
    return ztemp3

def zchunk(address):
    if (len(address) != 32):
        zalert("Can't chunk non 32 hex string!")
        return False
    ztemp2=""
    for ztemp in range(0,32,4):
        zchar=address[ztemp:ztemp+4]
        if ztemp>0:
            zchar=":"+zchar
        ztemp2=ztemp2+zchar
    return ztemp2

def unchunk(address):
    if (len(address) != 39):
        zalert("Can't unchunk non 39 hex string!")
        return False
    ztemp2=""
    for ztemp in range (0,39,5):
        ztemp2=ztemp2+address[ztemp:4]
    return ztemp2

def maskanalyze():
    global htmltext
    global inipv6address
    global ipv6address
    global ipv6address_truncate
    global ipv6address_binary
    global ipv4address_embedded
    global firstipv4address_embedded
    global ipv4address_embedded
    global subnet
    global network
    global subnetmask
    global network_binary
    global osubnet
    global oipv6address
    global oipv6address_binary
    global oipv6address_truncate
    global onetwork
    
    htmltext.append("<br>"+cc.starttable2+cc.startrow4a+"Network Prefix Analysis /"+str(osubnet)+cc.endrow1)
    htmltext.append(cc.startrow4)
    for ztemp in range(0,40):
        ztemp2=oipv6address[ztemp:ztemp+1]
        htmltext.append(ztemp2)
        if ztemp<39:
            if (((float(ztemp)+2)/5) == int((ztemp+2)/5)):
                htmltext.append(cc.rowdivider4a)
            else:
                htmltext.append(cc.rowdivider4)
    htmltext.append(cc.endrow1)
    if osubnet < 1:
        htmltext.append(cc.startrow1a)
    else:
        htmltext.append(cc.startrow1)
    for ztemp in range (0,128):
        ztemp2=oipv6address_binary[ztemp:ztemp+1]
        htmltext.append(ztemp2)
        if ((ztemp+2) > osubnet):
            ztemp2=cc.rowdivider2a
        else:
            ztemp2=cc.rowdivider2
        if ztemp<127:
            if (((float(ztemp)+1)/16) == int((ztemp+1)/16)):
                htmltext.append(ztemp2+":"+ztemp2)
            else:
                htmltext.append(ztemp2)
    htmltext.append(cc.endrow1)
    htmltext.append(cc.startrow4)
    for ztemp in range (0,40):
        ztemp2=onetwork[ztemp:ztemp+1]
        htmltext.append(ztemp2)
        if ztemp<39:
            if (((float(ztemp)+2)/5) == int((ztemp+2)/5)):
                htmltext.append(cc.rowdivider4a)
            else:
                htmltext.append(cc.rowdivider4)
    htmltext.append(cc.startrow4b+" Prefix Length = "+str(osubnet)+" bits"+cc.endrow1)
    ztemp1 = 128-osubnet
    ztemp = comma("{}".format(2 ** ztemp1))
    htmltext.append(cc.startrow4b+" Hosts         = 2<sup>"+str(ztemp1)+"</sup>   =  "+ztemp+cc.endrow1)
    ztemp = 64-osubnet
    if ztemp>=0:
        ztemp1 = comma("{}".format(2 ** ztemp))
        htmltext.append(cc.startrow4b+" /64 networks = 2<sup>"+str(ztemp)+"</sup>     = "+ztemp1+cc.endrow1)

def comma(number):
    length=len(number)
    output=""
    if (length<3):
        return number
    while (length>3):
        output=","+number[length-3:length]+output
        number=number[0:length-3]
        length=len(number)
    output=number+output
    return output

def getv4(hex):
    if (len(hex) != 8):
        zalert("Can't get IPv4 address from non 8 hex string!")
        return False
    zchar=""
    ztemp=0
    v4addr=""
    for ztemp in range (0,7,2):
        zchar=hexToOctet(hex[ztemp:ztemp+2])
        v4addr=v4addr+zchar
        if ztemp<6:
            v4addr=v4addr+"."
    return v4addr
    
def hexToOctet(hex):
    if (len(hex) != 2):
        alert("Can't get octet from bad hex string!")
        return False
    high = cc.hexstring.find(hex[0:1]) * 16
    low = cc.hexstring.find(hex[1:2])
    ztemp3 = high + low
    return str(ztemp3)


