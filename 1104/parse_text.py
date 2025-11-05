#OCR로 얻은 텍스트에서 타임스탬프는 버리고 곡명과 가수로 분리한다.
#예외적으로 곡명만 있는 경우에는 후처리를 하여 정보의 불완전성을 완전하게 만든다.


from read_text import text #1104/read_text.py 안에 OCR 결과 text 변수

#text = extract_text("proprecessed.png")
#print(text)

lines = text.strip().split("\n") #OCR로 추출된 긴 텍스트(text)를 줄 단위로 나눈다.
songs = [] #songs 라는 빈 상자를 만들었다. 추후에 "곡과 가수" 한 쌍씩 담는다.

for line in lines:
    if "-" in line:
        parts = line.split("-") #-를 기준으로 왼쪽은 parts[0] 오른쪽은 parts[1] 이 됩니다.
        song_name = parts[0].split("]")[-1].strip() # parts[0]은 타임라인이 있기 때문에 ]을 기준으로 또 쪼개고 제일 마지막에 있는 부분[-1]을 strip 공백없이 가져옵니다.
        artist_name = parts[1].strip() #parts[1]은 혼자 있으니까 strip공백만 제외하고 가져와요.
        songs.append((song_name, artist_name)) 
for song in songs:
    #print(song)
    pass
