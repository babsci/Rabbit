from pydub import AudioSegment
import numpy as np

def find_max(list_):
    index=0
    for i in range(0,len(list_)):
        if(list_[i]>list_[index]):
            index=i
    return index


src = "EverlastingTruth.mp3"
audio = AudioSegment.from_file(src,"mp3")
#raw_audio_data = audio.raw_data
#decibel = audio[4900:5000].dBFS
#data = np.fromstring(audio._data, np.int16)
data_length = len(audio)
print(data_length)


#每500ms=0.5s算一个音
note_time = 500
bar = data_length//note_time + 1
note_decibel = []

for i in range(0,bar):
    note_decibel.append((audio[500*i:500*(i+1)]).dBFS)
note_num=len(note_decibel)
print(note_num)


#设置每7s为一个小节
piece_time = 7000
note_every_piece = piece_time // note_time
piece_num = 500*len(note_decibel)//piece_time
piece_max=[]
point_max=[]

for i in range(0,piece_num):
    piece_max.append(max(note_decibel[i*note_every_piece:(i+1)*note_every_piece]))
    point_max.append(find_max(note_decibel[i*note_every_piece:(i+1)*note_every_piece]))
    
    
print(len(piece_max))
print(piece_max)

stress_time=[]
print("Stress time:")
for i in range(0,len(point_max)):
    stress_time.append(i*7+0.5*point_max[i])
    print(i*7+0.5*point_max[i],"s")


#print(max(note_decibel))
#
#decibel_time = 500
#print(len(audio._data))
#print(len(raw_audio_data))


"""
print(decibel)
loudness = audio.dBFS
print(loudness)
data = np.fromstring(loudness,np.int16)
print(data)
length = len(data)
for i in data:
    if(i!=0):
        print(i)
print(data[100:200])

"""


