#!/bin/bash
docker build -t base -f Dockerfile.base .
docker build -t instagram .
docker run --rm -it -p 8013:80 instagram

# 쉘어서 `/bin/bash docker-run.sh`로 실행해야 하는 것을 `./docker-run.sh`로 쓸 수도 있다.
# 파일 이름만 적어두면 shell 의 $PATH 에서 해당 파일을 찾는다.