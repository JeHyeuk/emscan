from xml.etree.ElementTree import parse



tree = parse(
    r"D:\SVN\GSL_Build\1_AswCode_SVN\PostAppSW\0_XML\DEM_Rename\ambt_confdata.xml"
)
root = tree.getroot()

def search(tag, cnt=0):
    print("\t" * cnt, tag)
    if len(tag) < 1:
        return
    cnt += 1
    for itag in tag:
        search(itag, cnt)
search(root)