"""
def bmi(cm, kg):
    m = cm * 0.01
    return round((kg / (m * m)), 2)
kg = int(input("몸무게를 입력하세요(kg): "))
cm = int(input("키를 입력하세요(cm): "))

print(f"BMI: {bmi(cm, kg)}")
"""
"""
def avg(num):
    return sum(num) / len(num)
num = []
while True:
    val = input("숫자 입력 (q 입력 시 종료) : ")
    if val == 'q':
        break
    num.append(float(val))
if len(num) == 0:
    print("값이 없습니다.")
else:
    print(f"---> 평균: {round((avg(num)), 2)}")
"""
wo = {}
bunshou = input("문장을 입력하세요: ")
word = bunshou.split(" ")
for w in word:
    count = 0
    for s in word:
        if w.lower() == s.lower():
            count += 1
    