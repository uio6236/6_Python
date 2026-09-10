"""
name = input("이름 입력: ")
gender = input("성별(M/F) 입력: ")
if gender == 'M':
    gender = '남'
else: 
    gender = '여'
age = int(input("나이 입력: "))
height = float(input("키 입력: "))

print(f"이름: {name}, 성별: {gender}, 나이: {age}, 키: {height}cm")
"""
"""
alpha = input("영문 소문자를 입력하세요: ")
big = alpha.upper()
print(f"소문자: {alpha}")
print(f"대문자: {big}")
"""
"""
first = int(input("첫 번째 정수를 입력하세요: "))
second = int(input("두 번째 정수를 입력하세요: "))
print(f"합: {first + second}")
print(f"차: {first - second}")
print(f"곱: {first * second}")
print(f"몫: {round(first / second)}")
print(f"나머지: {first % second}")
"""
"""
first = int(input("첫 번째 정수를 입력하세요: "))
second = int(input("두 번째 정수를 입력하세요: "))
print(f"{first}의 제곱: {first ** first}")
print(f"{second}의 제곱근: {second}?")
"""
"""
score = int(input("점수를 입력하세요(0-100): "))
if score >= 90:
    print("학점: A")
elif score >= 80:
    print("학점: B")
elif score >= 70:
    print("학점: C")
elif score >= 60:
    print("학점: D")
elif score >= 0:
    print("학점: F")
else:
    print("점수를 올바르게 입력해주세요.")
"""
"""
for i in range(1, 101):
    if (i % 2 == 0):
        print(i)
"""
"""
sum = 0
for i in range(1, 101):
    if i % 3 == 0 and i % 5 != 0:
       sum += i
print(sum)
"""