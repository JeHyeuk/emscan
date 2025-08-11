# emscan

Engine Management System(EMS) - ASW/CAN Convenient Tool<br>
엔진제어시스템 ASW 및 CAN 개발 편의 도구

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
