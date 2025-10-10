# pyems

파이썬을 이용한 엔진제어시스템(EMS)의 Application SW 및 CAN통신 개발 편의 도구<br>
Python tool for developing EMS application SW and CAN communication SW. 

# 개발자 가이드 Developer Guide

## 🧾 Naming Convention Guide

| 변수 이름(Variable) | 함수 이름(Function) | 클래스 이름(Class) | 시스템 상수(Constant) |
|------------------|-----------------|---------------------------|---|
| `snake_case`     | `snake_case`    | `CamelCase`(`PascalCase`) | `upper case` |
* 클래스 이름은 약어 구분 없이 적용됩니다. 단어가 대문자로만 구성되어도 `CamelCase`를 적용해주세요. (PEP 8)
* Class names are not restricted by abbreviations. Use `CamelCase` despite of the abbreviation. (PEP 8)

```
''' Example '''

# 변수 이름 Variable Name
pyems_pressure = 12 - 8;

# 함수 이름 Function Name
def some_function(a:int, b:int) -> int:
    return a + b
    
# 클래스 이름 Class Name
class CanDb(object):
    pass
    
# 시스템 상수 System Constant
USERNAME = 'LEE JEHYEUK'
```

## 🧾 Type Hint
* 모든 함수는 `typing` (또는 `built-in`)의 힌트를 적용해주세요.
* All functions must be applied by the type-hint (`typing` or `built-in`)

```
''' Example '''

from typing import Union

def some_function(a:Union[int, float], b:float) -> Union[int, float]:
    return a + b
```

## 🧾 Docstring
* 모든 함수는 Docstring(`__doc__`)가 정적으로 정의되어야 하며 동적 `__doc__`는 지양해야 합니다.
* All functions must define docstring (`__doc__`) only by static post, not dynamic allocation.

# Functionality

## api
기능: Application Interface<br>
담당: LEE JE HYEUK<br>
내용: TBD<br>

## can
기능: CAN 통신 전반<br>
담당: LEE JE HYEUK, JO JAE HYUNG, JO GYU NA<br>
내용: TBD<br>

## core
기능: ASW 기능 전반<br>
담당: LEE JE HYEUK, JO JAE HYEUNG<br>
내용: TBD<br>

## env
기능: 개발 환경 전반<br>
담당: LEE JE HYEUK<br>
### - error.py
<b>요약</b> : 각종 에러 및 에러 핸들러 정의
### - PATH.py
<b>요약</b> : 개발 경로 정의<br>
<b>사용 예시</b><br>
1) 미리 정의된 SVN 경로 호출
```python
from PATH import SVN

print(SVN.CAN)
print(SVN.MODEL) # SVN.MD 또는 SVN.MDL로 접근 가능
print(SVN.MODEL.CAN)
print(SVN.MODEL.DB) # SVN의 경우 .db 파일 경로 제공
```

```python
# 결과
D:\svn\dev.bsw\hkmc.ems.bsw.docs\branches\HEPG_Ver1p1\11_ProjectManagement
D:\svn\model\ascet\trunk
D:\svn\model\ascet\trunk\HNB_GASOLINE\_29_CommunicationVehicle
D:\svn\model\ascet\trunk\.svn\wc.db
```
