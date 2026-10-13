from pathlib import Path
import json,wave,numpy as np,math,sys
R=Path(__file__).resolve().parents[1]/'runtime/results';name=sys.argv[1] if len(sys.argv)>1 else 'portrait-fountain-post-mute';reportName='continuous-campus16-verification.json' if name=='continuous-campus16-walk' else name+'-verification.json';d=json.loads((R/reportName).read_text());w=wave.open(str(R/(name+'.wav')));rate=w.getframerate();channels=w.getnchannels();frameCount=w.getnframes()
segments=d.get('audioSegments',[])
if not segments:
 samples=d['samples']
 for label in ['court-fountain','riverside-fire','StudentHub-connected-office-and-gallery','public-classroom-and-stage']:
  eligible=[s for s in samples if s['audio'].get('source')==label or s['audio'].get('zone')==label]
  runs=[]
  for s in eligible:
   if not runs or s['recordingMs']-runs[-1][-1]['recordingMs']>300:runs.append([])
   runs[-1].append(s)
  if runs:
   run=max(runs,key=len);segments.append({'label':label,'muted':False,'startMs':run[0]['recordingMs'],'endMs':run[-1]['recordingMs']})
out=[]
for s in segments:
 start=s['startMs']/1000+.4;end=s['endMs']/1000-.2
 if end<=start:continue
 end=min(end,start+12);w.setpos(min(int(start*rate),frameCount));x=np.frombuffer(w.readframes(max(0,int((end-start)*rate))),np.int16).astype(float).reshape(-1,channels)/32768;rms=float(np.sqrt(np.mean(x*x)));out.append({**s,'analyzedStartSeconds':start,'analyzedEndSeconds':end,'samplesPerChannel':len(x),'rms':rms,'rmsDbFS':20*math.log10(rms) if rms else None,'peak':float(np.max(np.abs(x)))})
result={'source':'Actual captured Opus track from exact concatenated browser chunks; decoded PCM channel-power RMS, no downmix cancellation or added soundtrack.','recordingSeconds':frameCount/rate,'sampleRate':rate,'channels':channels,'segments':out,'limitation':'No microphone or competing speech was sampled; this does not establish speech separation.'}
if d.get('audioSegments'):result.update(audibleOutputNonzero=out[0]['rms']>0 and out[2]['rms']>0,muteAttenuationPass=out[1]['rms']<out[0]['rms']/100)
(R/(name+'-audio-energy.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
