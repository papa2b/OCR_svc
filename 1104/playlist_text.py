#songs 리스트에 담긴 곡명과 가수를 CSV로 저장한다.

import csv
from parse_text import songs

csv_file = "playlist_text.csv" #csv 파일로 지정합니다. 이 파이썬을 통해 파일을 만들어야 그걸로 스포티파이에 연동 할 수 있겠죠?

#위 songs의 ocr결과를 csv 파일로 저장한다
with open(csv_file, mode="w", newline="", encoding="utf-8") as f: #csv파일을 쓰기모드로 열어 f라는 이름으로 사용할 준비
    writer = csv.writer(f) #csv.writer()은 csv파일에 데이터를 쓰는 도구로, f 파일 안에 글을 쓸 수 있다.
    writer.writerow(["곡명", "가수"]) # 첫째줄에 항목을 어떻게 설정할래
    writer.writerows(songs) # 이게 들어가야 리스트 안의 튜플을 한 줄씩 써준다
    #for song in songs:
        #writer.writerow(songs) #각 곡-가수 쌍 작성
        
print(f"CSV 저장 완료: {csv_file}")
#csv를 기반으로 spotify 재생목록 생성