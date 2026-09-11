# 내가 각 틀린 문제의 오답노트를 작성 중이야.
# 내가 왜 해당 답을 골랐는지 이유와 정답을 줄게
# 내가 무엇을 놓쳤고, 어떤 개념이 부족한지 알기 쉽게 설명해줘.

# 다음 코드의 실행 결과로 올바른 것을 고르시오.
t = (1, [2, 3], 4)
t[1].append(5)
print(t)

# 내가 고른 답은 AttributeError야.
# 튜플은 수정이 안되니 저런식의 접근은 안되어 오류가 날거라 생각했어.
# 근데 답은 (1, [2, 3, 5], 4)이야.
# 튜플 속 리스트니까 저런식의 접근도 괜찮았단거지?

# 다음 코드가 실행되었을 때 출력되는 결과로 올바른 것을 고르시오.
data = ["A", "B", "A", "C", "B"]
s = set(data)
d = {}
for i, v in enumerate(data):
    d[v] = i
print(len(s), d["A"], d.get("D", 0))

# 내가 고른 답은 3 0 0 이야.
# len(s)는 set(data)로 data의 중복을 없앴으니 3이고
# d["A"] 이건 솔직히 모르겠어.
# d.get("D", 0)는 어차피 "D"가 없으니 0이잖아.
# 정답은 3 2 0 이래

# 다음 코드가 실행되었을 때 출력되는 결과로 올바른 것을 고르시오.
def add_item(item, box=[]):
    box.append(item)
    return box
print(add_item("a"))
print(add_item("b"))

# 내가 고른 답은 ['a'] ['b']야
# 난 저렇게 각 print 문으로 생성되는 box는 각각 별개라고 생각했어.
# 근데 정답은 ['a'] ['a', 'b'] 이래

# 다음 코드가 실행되었을 때 출력되는 결과로 올바른 것을 고르시오.
class Counter:
    count = 0

    def __init__(self):
        Counter.count += 1
        self.id = Counter.count
c1 = Counter()
c2 = Counter()
print(c1.count, c2.id)

# 내가 고른 답은 1 1 이야. 근데 정답은 2 2야.
# 솔직히 이건 내가 개념이 정확히 몰라서 고른 거야.

# 다음 코드가 실행되었을 때 콘솔에 출력되는 내용을 순서대로 나열한 것을 고르시오.
def divide(a, b):
    try:
        result = a /b
    except ZeroDivisionError:
        return "0으로 나눌 수 없습니다."
    else:
        return result
    finally:
        print("계산 종료")
print(divide(10, 0))

# 내가 고른 답은 0으로 나눌 수 없습니다. 계산 종료 야.
# 근데 정답은 계산 종료 0으로 나눌 수 없습니다. 야.
# 난 예외 처리가 먼저인줄 알았는데 finally 실행 후 예외 처리문이 실행되는거야?

# 아래와 같이 myapp 패키지를 구성하고 main.py를 실행했습니다. 실행 결과가 어떻게 되는지 쓰고,
# 그 이유를 파이썬의 import 동작 방식과 연관 지어 설명하시오. 또한 의도한 대로 동작하도록 만드는
# import 방법 2가지를 코드로 제시하시오.

"""
myapp/
    - __init__.py
    - calc.py
main.py

# myapp/calc.py
def add(a, b):
    return a + b

# main.py
from myapp.calc import add

print(myapp.calc.add(3, 4))
"""

# 난 이 부분 내용을 다 까먹어서 정답 안 적었어.
# 정답은
"""
이유: 오류 발생
NameError: name 'myapp' is not defined

해결 방법:
1. from ~ import로 가져온 이름을 그대로 사용
from myapp.calc import add
print(add(3, 4))
2. 모듈 자체를 import 하여 전체 경로로 사용
from myapp import calc
print(calc.add(3, 4))
"""

# 다음은 은행 계좌를 표현한 클래스입니다. 이 코드에는 총 2가지의 잘못된 부분이 있습니다.
# 어느 부분이 잘못되었는지 찾아 그 원인을 설명하고, 올바르게 수정한 전체 코드를 작성하시오.
class BankAccount:
    def __init__(owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("잔액이 부족합니다")
        self.balance -= amount
        return self.balance

acc = BankAccount("홍길동", 10000)
print(acc.withdraw(30000))

"""
정답
잘못된 부분:
1. BankAccount 클래스의 생성자 매개변수 누락 (self)
2. withdraw 메소드 관련 예외처리 누락

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("잔액이 부족합니다")
        self.balance -= amount
        return self.balance

acc = BankAccount("홍길동", 10000)
try:
    print(acc.withdraw(30000))
except ValueError as e:
    print(f"오류 발생: {e}")
except Exception as e:
    print(e)
else:
    print("출금 완료")
"""

# 이건 매번 자동 완성 기능으로 코드를 작성하다 보니 내가 이론적인 부분을 놓쳐서 몰랐어.