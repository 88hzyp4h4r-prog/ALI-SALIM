import json, subprocess, os, glob, re, sys
S="/tmp/claude-0/-workspace-ALI-SALIM/c5a766e6-dd35-5dfc-aaec-04bf2024fd95/scratchpad"
W="/workspace/ALI-SALIM/dropbox-v2"
CL="/workspace/ALI-SALIM/dropbox-clips/clips"
OUT=S+"/build"; FPS=30
D=json.load(open(S+"/stt.json"))
words=[w for w in D['words'] if w['type']=='word']
TOTAL=55.2

# (clip, start_in_clip, timeline_start)  end = next start
segs=[("IMG_4993",0.0,0.0),("IMG_4995",10.0,3.2),("IMG_5027",0.0,6.0),("IMG_5029",0.0,10.4),
("IMG_5033",0.3,11.46),("IMG_5012",0.0,14.54),("IMG_5018",0.0,16.32),("IMG_4996",0.0,17.24),
("IMG_5011",0.0,18.36),("IMG_5002",0.5,22.7),("IMG_5006",0.5,24.76),("IMG_5003",3.0,28.12),
("IMG_5007",0.5,30.18),("IMG_4997",0.0,34.0),("IMG_5022",0.0,35.16),("IMG_5020",0.5,37.84),
("IMG_5018",0.0,40.72),("IMG_5029",0.0,43.42),("IMG_5028",0.0,46.4),("IMG_5019",0.0,49.96),("IMG_5017",4.0,52.44)]
bounds=[round(s[2]*FPS) for s in segs]+[round(TOTAL*FPS)]
files=[]
for i,(c,ss,t0) in enumerate(segs):
    nf=bounds[i+1]-bounds[i]; dur=nf/FPS
    out=f"{OUT}/seg{i:02d}.mp4"; files.append(out)
    z=f"'trunc(1080*(1.00+0.09*t/{dur:.3f})/2)*2'"; h=f"'trunc(1920*(1.00+0.09*t/{dur:.3f})/2)*2'"
    vf=(f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps={FPS},"
        f"scale=w={z}:h={h}:eval=frame,crop=1080:1920,eq=brightness=0.04:contrast=1.07:saturation=1.18,setsar=1,format=yuv420p")
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ss),"-i",f"{CL}/{c}.mov","-vf",vf,"-frames:v",str(nf),"-an",
        "-c:v","libx264","-crf","16","-preset","veryfast","-r",str(FPS),out],check=True)
open(OUT+"/list.txt","w").write("".join(f"file '{f}'\n" for f in files))
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",OUT+"/list.txt","-c","copy",OUT+"/video.mp4"],check=True)

# ---------- ASS ----------
def ts(t):
    t=max(t,0); h=int(t//3600); m=int(t%3600//60); s=t%60
    return f"{h}:{m:02d}:{s:05.2f}"
RED="&H002E10C8&"; GRN="&H003B7F1B&"; GOLD="&H000AD6FF&"; WHITE="&H00FFFFFF&"; BLK="&H00000000&"
ev=[]
def rect(w,h): return f"{{\\p1}}m 0 0 l {w} 0 {w} {h} 0 {h}{{\\p0}}"
def box(t0,t1,x,y,w,h,col,anim=True,alpha="00"):
    a="\\fscx0\\fscy0\\t(0,140,\\fscx108\\fscy108)\\t(140,260,\\fscx100\\fscy100)" if anim else ""
    ev.append(f"Dialogue: 0,{ts(t0)},{ts(t1)},G,,0,0,0,,{{\\an5\\pos({x},{y})\\1c{col}\\alpha&H{alpha}&\\bord0\\shad0{a}\\fad(0,160)}}{rect(w,h)}")
def txt(t0,t1,x,y,text,size,col=WHITE,anim=True):
    a="\\fscx0\\fscy0\\t(0,140,\\fscx108\\fscy108)\\t(140,260,\\fscx100\\fscy100)" if anim else ""
    ev.append(f"Dialogue: 1,{ts(t0)},{ts(t1)},G,,0,0,0,,{{\\an5\\pos({x},{y})\\fs{size}\\1c{col}\\b1\\bord0\\shad0{a}\\fad(0,160)}}{text}")
def tag(t0,t1,text,y,col=RED,size=64):
    w=90+int(size*0.52*len(text)); h=size+50
    box(t0,t1,540,y,w,h,col); txt(t0,t1,540,y-4,text,size)
# progress bar
ev.append(f"Dialogue: 0,{ts(0)},{ts(TOTAL)},G,,0,0,0,,{{\\an7\\pos(0,0)\\1c{GOLD}\\bord0\\shad0\\fscx0\\t(0,{int(TOTAL*1000)},\\fscx100)}}{rect(1080,14)}")
# hook (0 - 5.6)
box(0.1,5.6,540,360,940,190,RED); txt(0.1,5.6,540,352,"أقوى وألذ مشروع منزلي",84)
box(0.45,5.6,540,540,560,130,GRN); txt(0.45,5.6,540,534,"في المعبيلة",70)
# flash at the hit (1.58)
ev.append(f"Dialogue: 2,{ts(1.55)},{ts(1.85)},G,,0,0,0,,{{\\an7\\pos(0,0)\\1c{WHITE}\\bord0\\shad0\\alpha&H20&\\t(0,300,\\alpha&HFF&)}}{rect(1080,1920)}")
# watermark chip
box(6.0,TOTAL,200,130,300,86,RED,anim=False); txt(6.0,TOTAL,200,127,"زوادة",50,anim=False)
tag(11.46,14.3,"إدارة عُمانية بالكامل",360,GRN,60)
tag(14.54,16.2,"مخبوزات",360); tag(16.32,17.1,"حلويات",360,GRN); tag(17.24,18.3,"معجنات",360)
tag(23.34,24.7,"بيتزا الدجاج",360); tag(24.76,28.0,"فطيرة لبنة وزعتر",360,GRN)
tag(35.36,38.0,"اللقيمات",360)
tag(43.98,46.0,"اطلب أي كمية",360,GRN); tag(46.12,49.9,"حفلات ومناسبات",360)
# end card
ev.append(f"Dialogue: 0,{ts(50.0)},{ts(TOTAL)},G,,0,0,0,,{{\\an7\\pos(0,0)\\1c{BLK}\\alpha&H70&\\bord0\\shad0\\fad(250,0)}}{rect(1080,1920)}")
box(50.3,TOTAL,540,820,900,210,RED); txt(50.3,TOTAL,540,812,"توصيل لمحافظة مسقط",84)
box(52.44,TOTAL,540,1010,760,150,GRN); txt(52.44,TOTAL,540,1004,"التفاصيل في حسابهم",64)
# captions
chunks=[];cur=[]
for w in words:
    cur.append(w); t=w['text']
    if re.search(r"[.،,!؟?]$",t) or len(cur)>=3 or sum(len(x['text']) for x in cur)>=15:
        chunks.append(cur);cur=[]
if cur: chunks.append(cur)

import numpy as np
from PIL import Image
def ink(full):
    h=("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
    "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n"
    "Style: C,Cairo,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,5,40,40,0,1\n\n[Events]\n"
    "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")
    open(OUT+"/tt.ass","w").write(h+"Dialogue: 0,0:00:00.00,0:00:01.00,C,,0,0,0,,{\\an5\\pos(540,960)\\bord0\\shad0}"+full+"\n")
    subprocess.run(["ffmpeg","-v","error","-y","-f","lavfi","-i","color=c=black:s=1080x1920:d=1","-vf",f"ass={OUT}/tt.ass:fontsdir={W}/fonts","-frames:v","1",OUT+"/tt.png"],check=True)
    c=np.where((np.array(Image.open(OUT+"/tt.png").convert("L"))>128).any(0))[0]
    return c.min(),c.max()
clean=lambda s:re.sub(r"[.،,!؟?]","",s)
json.dump([[clean(x['text']) for x in ch] for ch in chunks],open(OUT+"/chunks.json","w"),ensure_ascii=False)
meas=[None]*len(chunks)
RLE="\u202b"; PDF="\u202c"
for ch,m in zip(chunks,meas):
    full=RLE+" ".join(clean(x['text']) for x in ch)+PDF
    ev.append(f"Dialogue: 3,{ts(ch[0]['start'])},{ts(ch[-1]['end']+0.1)},C,,0,0,0,,{{\\an5\\pos(540,1420)\\1c{WHITE}}}{full}")
    imin,imax=ink(full)
    ws_=[ink(RLE+clean(x['text'])+PDF) for x in ch]
    wid=[b_-a_ for a_,b_ in ws_]
    sp=((imax-imin)-sum(wid))/max(len(ch)-1,1)
    pos=[];r_=imax
    for wd in wid:
        pos.append((r_-wd,r_)); r_=r_-wd-sp
    for i,w in enumerate(ch):
        a=w['start']; b2=ch[i+1]['start'] if i+1<len(ch) else w['end']+0.1
        l,r=pos[i]; l-=sp/2; r+=sp/2
        ev.append(f"Dialogue: 4,{ts(a)},{ts(b2)},C,,0,0,0,,{{\\an5\\pos(540,1420)\\1c{GOLD}\\clip({l:.0f},1330,{r:.0f},1520)}}{full}")
hdr=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: G,Cairo,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: C,Cairo,80,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,1,0,0,0,100,100,0,0,1,9,4,5,40,40,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
open(OUT+"/sub.ass","w").write(hdr+"\n".join(ev)+"\n")

# ---------- audio ----------
def find(name):
    return [f for f in glob.glob(W+"/sfx/pack/**/*",recursive=True) if "__MACOSX" not in f and os.path.basename(f)==name][0]
riser=find("Risers-020.wav"); hit=find("Hit-005.wav"); whoosh=find("whoosh soft-056.wav"); pop=find("اصوات البوب pop.mp3")
voice=W+"/x/Lulu Pharmacy 3.m4a"
inputs=[voice,riser,hit]; fl=["[0:a]loudnorm=I=-15:TP=-1.5:LRA=7,apad=whole_dur=%.2f[v]"%TOTAL,
 "[1:a]atrim=start=0.676,asetpts=PTS-STARTPTS,afade=t=in:d=0.15,volume=1.6,adelay=0|0[r]",
 "[2:a]volume=1.0,adelay=1580|1580[h]"]
mix=["[v]","[r]","[h]"]; n=3
for t in [6.0,14.54,22.7,35.16,43.42,49.96]:
    inputs.append(whoosh)
    fl.append(f"[{n}:a]atrim=0:0.7,afade=t=out:st=0.4:d=0.3,volume=0.28,adelay={int((t-0.3)*1000)}|{int((t-0.3)*1000)}[w{n}]"); mix.append(f"[w{n}]"); n+=1
pops=[(11.46,0.66,0.85),(14.54,1.99,2.17),(23.34,3.86,3.98),(35.36,0.66,0.85),(43.98,1.99,2.17),(50.3,3.86,3.98)]
for t,a,b in pops:
    inputs.append(pop)
    fl.append(f"[{n}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,volume=0.35,adelay={int(t*1000)}|{int(t*1000)}[p{n}]"); mix.append(f"[p{n}]"); n+=1
fl.append("".join(mix)+f"amix=inputs={len(mix)}:normalize=0:dropout_transition=0,alimiter=limit=0.89,atrim=0:{TOTAL}[a]")
cmd=["ffmpeg","-v","error","-y"]
for f in inputs: cmd+=["-i",f]
cmd+=["-filter_complex",";".join(fl),"-map","[a]",OUT+"/audio.m4a","-c:a","aac","-b:a","192k"]
cmd=[c for c in cmd]
subprocess.run(["ffmpeg","-v","error","-y"]+sum([["-i",f] for f in inputs],[])+["-filter_complex",";".join(fl),"-map","[a]","-c:a","aac","-b:a","192k",OUT+"/audio.m4a"],check=True)
os.makedirs("/workspace/ALI-SALIM/output",exist_ok=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",OUT+"/video.mp4","-i",OUT+"/audio.m4a","-vf",f"ass={OUT}/sub.ass:fontsdir={W}/fonts","-map","0:v","-map","1:a",
 "-c:v","libx264","-crf","19","-preset","medium","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart","-t",str(TOTAL),"/workspace/ALI-SALIM/output/zawad-reel.mp4"],check=True)
print("done")
