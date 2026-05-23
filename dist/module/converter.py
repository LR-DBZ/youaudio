import os,shutil,subprocess
def convert_m4a_to_mp3(m4a_path,output_dir):B=m4a_path;A=True;D=os.path.splitext(os.path.basename(B))[0];C=os.path.join(output_dir,D+'.mp3');subprocess.run(['ffmpeg','-i',B,'-codec:a','libmp3lame','-b:a','320k','-y',C],check=A,capture_output=A,text=A);return C
def move_file(source,dest):shutil.move(source,dest)