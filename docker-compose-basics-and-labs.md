## Docker Compose 기본 개념 및 동작 원리 + 실습 가이드

이 문서는 Docker Compose를 처음 접하는 초심자도 따라 할 수 있도록, 핵심 개념을 쉬운 말로 정리하고 단계별 실습을 제공합니다. 명령어와 설정 항목은 “무엇을 왜 하는지”를 함께 설명합니다.

---

### 1) Docker Compose란 무엇인가

- **여러 컨테이너를 하나의 서비스 묶음(프로젝트)으로 관리**하는 도구입니다.
- 애플리케이션은 보통 웹 서버, 데이터베이스, 캐시처럼 여러 컨테이너가 협력해 동작합니다. Compose는 이들을 하나의 프로젝트로 정의하고, 한 번의 명령으로 생성/실행/중지/삭제할 수 있게 합니다.
- 설정은 **YAML 파일**에 작성합니다. 이 파일에는 어떤 이미지를 쓸지, 포트를 어떻게 열지, 어떤 네트워크/볼륨을 쓸지 등 컨테이너 실행에 필요한 옵션이 들어갑니다.

용어(간단 설명)
- **컨테이너(Container)**: 이미지를 실행한 상태. 격리된 프로세스.
- **이미지(Image)**: 컨테이너를 만들기 위한 실행 패키지(파일 시스템 + 실행 정보).
- **서비스(Service)**: 동일한 목적/설정을 가진 컨테이너의 논리적 그룹(예: `web`, `db`).
- **프로젝트(Project)**: 한 개의 `docker-compose.yml`로 정의된 전체 묶음. 기본적으로 디렉터리명이 프로젝트 이름이 됩니다.
- **네트워크(Network)**: 컨테이너 간 통신을 위한 가상 네트워크.
- **볼륨(Volume)**: 컨테이너 재시작에도 남는 데이터 저장소.
- **YAML**: 들여쓰기로 구조를 표현하는 설정 파일 형식. Compose에서는 탭 대신 공백 2칸 사용을 권장합니다.

왜 쓰나(장점)
- 여러 컨테이너의 **옵션과 환경을 파일 하나로 표준화**하여, 재현 가능한 실행을 보장합니다.
- **의존성**(예: 웹이 DB에 의존)을 표현할 수 있고, **네트워크/볼륨**을 함께 정의합니다.
- 단일 호스트 기준으로 **스케일 아웃**(같은 서비스 컨테이너를 여러 개)도 간단히 할 수 있습니다.

동작 원리(아주 간단히)
- Compose는 YAML을 읽어 **정의된 순서/의존성에 따라 컨테이너를 만들어 실행**합니다.
- 각 서비스는 내부 DNS로 서로의 서비스 이름으로 통신할 수 있습니다(서비스 디스커버리).

명령 사용 형태
- 최신 Compose v2에서는 `docker compose ...`(띄어쓰기) 사용을 권장합니다. 구버전 `docker-compose ...`도 종종 보이지만, 본 가이드는 v2 표기를 주로 사용합니다.

프로젝트/서비스/컨테이너 이름 규칙
- 실제 컨테이너 이름은 보통 `[프로젝트]_[서비스]_[번호]` 형태로 생성됩니다. 예: `myapp_web_1`.

YAML 기본 구조
```yaml
version: '3.8'          # Compose 파일 포맷 버전(도커 엔진 버전에 의존)
services:               # 실행할 서비스(컨테이너)들의 모음
  web:                  # 서비스 이름(임의 지정)
    image: nginx        # 사용할 이미지
    ports:
      - "8080:80"      # 호스트:컨테이너 포트 매핑
volumes:                # (선택) 볼륨 정의
networks:               # (선택) 네트워크 정의
```

들여쓰기 주의
- 탭(Tab)이 아니라 **공백 2칸**으로 하위 항목을 들여쓰기 합니다.

---

### 2) 실습 1: 프라이빗 레지스트리 + 레지스트리 UI 구성

목표: 사설 Docker Registry(`registry:2`)와 그 UI(`joxit/docker-registry-ui`)를 Compose로 올립니다.

사전 준비(외부 리소스 생성)
```bash
# 외부 볼륨과 네트워크를 미리 만들어 둡니다(Compose에서 external: true를 사용할 것이기 때문).
sudo docker volume create image-volume
sudo docker network create net2
```

1) 원격 호스트 접속(예시)
```bash
ssh <user>@container1
```
- 원격 서버에 접속합니다. `<user>`와 `container1`은 환경에 맞게 바꾸세요.

2) 작업 디렉터리와 Compose 파일 만들기
```bash
mkdir -p docker_workspace && cd docker_workspace
cat > docker-compose.yaml <<'YAML'
version: '3.8'

services:
  registry:
    image: registry:2
    ports:
      - 5000:5000
    volumes:
      - image-volume:/var/lib/registry
    networks:
      - net2

  registry_ui:
    image: joxit/docker-registry-ui:2.5.7
    ports:
      - 80:80
    networks:
      - net2
    environment:
      - SINGLE_REGISTRY_MODE=true
      - REGISTRY_TITLE="MY Image Hub"
      - DELETE_IMAGES=true
      - SHOW_CONTENT_DIGEST=true
      - NGINX_PROXY_PASS_URL=http://registry:5000
      - SHOW_CATALOG_NB_TAGS=true
      - TAGLIST_PAGE_SIZE=10
      - REGISTRY_SECURED=false
      - CATALOG_ELEMENTS_LIMIT=1000

volumes:
  image-volume:
    external: true

networks:
  net2:
    external: true
YAML
```

구성 설명(핵심)
- `registry`: 공식 레지스트리 이미지. `5000:5000`으로 호스트 5000 포트를 공개합니다.
- `volumes: image-volume:/var/lib/registry`: 레지스트리 저장소를 이름 볼륨에 영구 보관합니다.
- `networks: net2`: 두 서비스가 같은 사용자 정의 네트워크에서 통신하도록 합니다.
- `registry_ui`: UI 컨테이너. `environment`로 UI 동작을 제어하고, `NGINX_PROXY_PASS_URL=http://registry:5000`으로 백엔드 레지스트리를 가리킵니다.
- `external: true`: 이미 존재하는 볼륨/네트워크를 사용합니다(그래서 사전 생성이 필요했습니다).

3) 기동
```bash
sudo docker compose up -d
```
- 백그라운드로 컨테이너를 생성/실행합니다.

4) 확인
```bash
sudo docker compose ps | cat
```
- UI는 호스트 80 포트에서, 레지스트리는 5000 포트에서 응답합니다.

스케일 예시(참고)
```bash
sudo docker compose up --scale registry=2 -d
sudo docker compose ps | cat
```
- 동일 서비스의 컨테이너 수를 늘릴 수 있습니다(단일 호스트 기준).

---

### 3) 개념 보강: 서비스 정의에서 자주 쓰는 키

- **depends_on**: 다른 서비스가 먼저 생성/실행되도록 순서를 지정합니다.
  - 예: `web`이 `mysql`에 의존하면 `web`보다 `mysql`이 먼저 올라갑니다.
  - 애플리케이션 “준비 완료”까지는 확인하지 않으므로(헬스체크 아님) 필요시 엔트리포인트 스크립트로 대기 로직을 넣습니다.

- **links**: 예전 방식의 링크. 오늘날에는 같은 네트워크에서 **서비스 이름으로 DNS 통신**이 가능하므로 일반적으로 필요하지 않습니다.

- **ports**: 호스트와 컨테이너 포트 매핑(예: `"8080:80"`).

- **build**: 도커파일로 이미지를 빌드해 사용합니다.
  - `context`: 빌드 컨텍스트 디렉터리
  - `dockerfile`: 사용할 도커파일 이름
  - `args`: 빌드 시 전달할 인자(도커파일의 `ARG`로 받음)

- **extends**: 다른 YAML의 서비스 속성을 상속(잘 쓰진 않지만 가능).

- 네트워크 정의
  - `driver`: `bridge`(기본), `overlay`(스웜), 등 드라이버 지정
  - `ipam`: 서브넷, 게이트웨이 같이 IP 할당 정책 지정
  - `external: true`: 이미 만들어진 네트워크를 사용

- 볼륨 정의
  - `driver`, `driver_opts`로 드라이버 및 옵션 지정 가능
  - `external: true`: 이미 만들어진 볼륨을 사용

- 파일 검증
```bash
docker compose config
```
- YAML 병합 결과와 문법 오류를 확인할 수 있습니다.

---

### 4) 실습 2: Ubuntu 24.04 + Nginx 이미지 빌드, 용량 최적화 비교

1) 디렉터리와 파일 생성
```bash
mkdir -p nginx-lab && cd nginx-lab

cat > docker-compose.yaml <<'YAML'
# Ubuntu 24.04 기본 이미지를 사용해서
# nginx 설치 및 기본 설정 후 컨테이너 실행

version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    image: container.company.co.kr/nginx-server:latest
    ports:
      - 8000:80
YAML

cat > Dockerfile <<'DOCKER'
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
DOCKER
```

설명
- `build.context`: 현재 폴더의 내용을 빌드 컨텍스트로 사용합니다.
- `image`: 빌드 결과에 붙일 이미지 이름/태그입니다.
- `ports 8000:80`: 호스트 8000 → 컨테이너 80으로 접속합니다.

2) 빌드 및 실행
```bash
sudo docker compose up -d --build
```

3) 이미지 용량 확인(초기)
```bash
sudo docker image ls container.company.co.kr/nginx-server --format '{{.Repository}}:{{.Tag}}  {{.Size}}'
```

4) Dockerfile 최적화(apt 캐시 제거)
```bash
cat > Dockerfile <<'DOCKER'
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
DOCKER

sudo docker compose up -d --build
```

5) 이미지 용량 재확인(비교)
```bash
sudo docker image ls container.company.co.kr/nginx-server --format '{{.Repository}}:{{.Tag}}  {{.Size}}'
```
- `rm -rf /var/lib/apt/lists/*`: 패키지 인덱스 캐시를 제거해 최종 이미지 용량을 줄입니다.

---

### 5) 실습 3: Nginx 설정을 빌드 인자(ARG)로 제어 + 템플릿 적용

1) Compose 수정(빌드 인자 추가, 포트 변경)
```bash
cat > docker-compose.yaml <<'YAML'
# Ubuntu 24.04 기본 이미지를 사용해서
# nginx 설치 및 기본 설정 후 컨테이너 실행

version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    args:
      - NGINX_SERVER_PORT=8080
      - NGINX_SERVER_ROOT=/var/www/html
    image: container.company.co.kr/nginx-server:latest
    ports:
      - 8000:8080
YAML
```

2) Nginx 템플릿 파일 준비
```bash
mkdir -p nginx/sites-available
cat > nginx/sites-available/default <<'CONF'
server {
    listen       ${NGINX_SERVER_PORT};
    server_name  _;
    root         ${NGINX_SERVER_ROOT};

    location / {
        try_files $uri $uri/ =404;
    }
}
CONF
```
- `${NGINX_SERVER_PORT}`, `${NGINX_SERVER_ROOT}`는 빌드 시 `envsubst`로 치환됩니다.

3) Dockerfile 수정(ARG/ENV + envsubst)
```bash
cat > Dockerfile <<'DOCKER'
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y nginx gettext-base && rm -rf /var/lib/apt/lists/*

ARG NGINX_SERVER_PORT
ARG NGINX_SERVER_ROOT

ENV NGINX_SERVER_PORT=${NGINX_SERVER_PORT}
ENV NGINX_SERVER_ROOT=${NGINX_SERVER_ROOT}

COPY nginx/sites-available/default /etc/nginx/sites-available/default
RUN envsubst '${NGINX_SERVER_PORT} ${NGINX_SERVER_ROOT}' < /etc/nginx/sites-available/default \
    | tee /etc/nginx/sites-available/default > /dev/null

EXPOSE ${NGINX_SERVER_PORT}

CMD ["nginx","-g", "daemon off;"]
DOCKER
```
- `gettext-base` 패키지에는 `envsubst`가 포함됩니다.
- `envsubst`: 템플릿의 `${...}` 변수를 환경변수 값으로 치환합니다.

4) 빌드/실행
```bash
sudo docker compose up -d --build
```

---

### 6) 실습 4: Apache 서비스 추가(템플릿 기반 설정)

1) Compose에 Apache 서비스 추가
```bash
cat >> docker-compose.yaml <<'YAML'
  apache-server:
    build:
      context: .
      dockerfile: Dockerfile.apache
      args:
        - APACHE_SERVER_PORT=8080
        - APACHE_SERVER_ROOT=/var/www/html
    image: container.company.co.kr/apache-server:latest
    container_name: apache-server
    ports:
      - 8001:8080
YAML
```
- `apache-server`는 호스트 8001 포트로 노출됩니다.

2) 기본 설정 파일 가져오기(한 번 실행 후 복사)
```bash
sudo docker compose up -d --build apache-server
sudo docker cp apache-server:/etc/apache2 ./
```
- 컨테이너 내부의 `/etc/apache2` 디렉터리를 현재 폴더로 복사합니다.

3) 기본 가상호스트 파일 템플릿으로 수정
```bash
cat > apache2/sites-available/000-default.conf <<'CONF'
<VirtualHost *:${APACHE_SERVER_PORT}>
    ServerAdmin webmaster@localhost
    DocumentRoot ${APACHE_SERVER_ROOT}

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
CONF
```
- `${APACHE_SERVER_PORT}`, `${APACHE_SERVER_ROOT}`는 빌드 시 치환될 자리표시자입니다.

4) `Dockerfile.apache` 생성(envsubst로 템플릿 치환)
```bash
cat > Dockerfile.apache <<'DOCKER'
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y apache2 gettext-base && rm -rf /var/lib/apt/lists/*

ARG APACHE_SERVER_PORT
ARG APACHE_SERVER_ROOT

ENV APACHE_SERVER_PORT=${APACHE_SERVER_PORT}
ENV APACHE_SERVER_ROOT=${APACHE_SERVER_ROOT}

COPY apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.conf
RUN echo "Listen ${APACHE_SERVER_PORT}" >> /etc/apache2/ports.conf
RUN envsubst '${APACHE_SERVER_PORT} ${APACHE_SERVER_ROOT}' < /etc/apache2/sites-available/000-default.conf \
    | tee /etc/apache2/sites-available/000-default.conf > /dev/null

EXPOSE ${APACHE_SERVER_PORT}

CMD ["apache2ctl","-D", "FOREGROUND"]
DOCKER
```

5) 빌드/실행
```bash
sudo docker compose up -d --build
sudo docker compose ps | cat
```

---

### 부록: 트러블슈팅 힌트

- `external: true` 리소스가 없다고 나오면, 먼저 해당 **볼륨/네트워크를 생성**하세요.
- YAML 들여쓰기 오류가 의심되면 `docker compose config`로 **구문/병합 확인**을 하세요.
- 포트 충돌 시, 이미 사용 중인 호스트 포트를 다른 값으로 바꿔 매핑하세요(예: `8000:8080` → `8002:8080`).

---

필요 시 다음 단계로, 헬스체크 추가, 멀티 스테이지 빌드로 이미지 더 줄이기, Compose 프로파일 사용 등을 이어서 실습할 수 있습니다.

