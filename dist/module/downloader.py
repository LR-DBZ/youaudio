import os,re,queue,threading,pytubefix
from module.config import load_and_validate_paths
from module.stream import obtain_itag
from module.converter import convert_m4a_to_mp3,move_file
def _process_first_m4a(source_dir,dest_dir):
	C=dest_dir;A=source_dir
	for B in os.listdir(A):
		if B.endswith('.m4a'):D=os.path.join(A,B);F=convert_m4a_to_mp3(D,A);G=re.sub('[?&#/:*?"<>|]','_',os.path.splitext(B)[0]);E=G+'.mp3';H=os.path.join(C,E);move_file(F,H);os.remove(D);return f"Downloaded {E} on Folder: {C}"
	raise FileNotFoundError(f"No .m4a files found in {A}")
def download_audio(link):
	L='downloading';G=None;C='msg';B='pct';A='step';H,M=load_and_validate_paths();D=queue.Queue();F=[]
	def N(stream,chunk,bytes_remaining):
		E=stream
		if E.filesize:F=E.filesize-bytes_remaining;G=15+int(F/E.filesize*45);D.put({A:L,B:G,C:'Downloading audio...','loaded':F,'total':E.filesize})
	yield{A:'fetching',B:5,C:'Fetching video info...'};O=pytubefix.YouTube(link,on_progress_callback=N);I=O.streams;yield{A:'selecting',B:10,C:'Selecting audio stream...'};J=obtain_itag(I)
	if not J:raise RuntimeError('No suitable audio stream found')
	P=I.get_by_itag(J);yield{A:L,B:15,C:'Starting download...'}
	def Q():
		try:P.download(H);D.put(G)
		except Exception as A:F.append(A)
	K=threading.Thread(target=Q);K.start()
	while K.is_alive():
		try:
			E=D.get(timeout=.2)
			if E is G:break
			yield E
		except queue.Empty:pass
	if F:raise F[0]
	while not D.empty():
		E=D.get_nowait()
		if E is not G:yield E
	yield{A:'converting',B:60,C:'Converting to MP3...'};R=_process_first_m4a(H,M);yield{A:'done',B:100,C:R}