_G='MUSIC_FOLDER'
_F='methods'
_E='origins'
_D='/download'
_C='DELETE'
_B='GET'
_A='error'
import os,json
from flask import Flask,request,jsonify,render_template,send_from_directory,Response,stream_with_context
from module.downloader import download_audio
from module.config import load_config
from flask_cors import CORS
app=Flask(__name__)
CORS(app,resources={_D:{_E:'*',_F:['POST']},'/audio/*':{_E:'*',_F:[_B,_C]}})
cfg=load_config()
MUSIC_FOLDER=os.path.abspath(os.getenv(_G,cfg.get(_G,'./music/')))
@app.before_request
def require_auth():
	if request.method=='OPTIONS':return
	B=os.environ.get('AUTH_USERNAME');C=os.environ.get('AUTH_PASSWORD')
	if B and C:
		A=request.authorization
		if not A or A.username!=B or A.password!=C:return jsonify({_A:'Unauthorized'}),401,{'WWW-Authenticate':'Basic realm="Login Required"'}
@app.route('/',methods=[_B])
def home():return render_template('index.html')
@app.route(_D,methods=['POST'])
def download():
	try:
		C=request.json;A=C.get('link')
		if not A:return jsonify({_A:'No link provided'}),400
		def D():
			try:
				for C in download_audio(A):yield json.dumps(C)+'\n'
			except Exception as B:print(f"Error en stream: {B}",flush=True);yield json.dumps({'step':_A,'msg':str(B)})+'\n'
		return Response(stream_with_context(D()),mimetype='application/x-ndjson')
	except Exception as B:print(f"Error en /download: {B}",flush=True);return jsonify({_A:str(B)}),500
@app.route('/songs',methods=[_B])
def list_songs():
	C='mtime'
	try:
		B=[]
		for A in os.listdir(MUSIC_FOLDER):
			if A.endswith('.mp3'):D=os.path.join(MUSIC_FOLDER,A);B.append({'name':A,'url':'/audio/'+A,C:os.path.getmtime(D)})
		B.sort(key=lambda s:s[C],reverse=True);return jsonify(B)
	except FileNotFoundError:return jsonify([])
@app.route('/audio/<filename>',methods=[_B,_C])
def handle_audio(filename):
	A=filename
	if request.method==_C:
		if'..'in A or'/'in A:return jsonify({_A:'Invalid filename'}),400
		B=os.path.join(MUSIC_FOLDER,A)
		if not os.path.exists(B):return jsonify({_A:'File not found'}),404
		os.remove(B);return jsonify({'message':f"Deleted {A}"})
	return send_from_directory(MUSIC_FOLDER,A)
@app.errorhandler(400)
def bad_request(error):return'Bad Request: {}'.format(error),400
if __name__=='__main__':app.run(host='0.0.0.0',port=5000)