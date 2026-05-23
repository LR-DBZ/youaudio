import re,pytubefix
def obtain_itag(streams):
	A=streams
	if not isinstance(A,pytubefix.query.StreamQuery):return''
	B=A.filter(file_extension='mp4',progressive=False,only_audio=True).order_by('abr')
	if not B:return''
	D=str(B[-1]);C=re.search('itag="(\\d+)"',D)
	if C:return C.group(1)
	return''