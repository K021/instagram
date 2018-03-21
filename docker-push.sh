#!/usr/bin/env bash
# 위 코드는 *.sh를 인식하는 모듈을 파이참에 설치한 상태에서, *.sh 파일이 생성되면 자신이 알아서 넣어준다.
# env 는 환경변수에 저장된 위치를 찾아서 실행해준다
docker build -t base -f Dockerfile.base .
docker tag base k021/base
docker push k021/base