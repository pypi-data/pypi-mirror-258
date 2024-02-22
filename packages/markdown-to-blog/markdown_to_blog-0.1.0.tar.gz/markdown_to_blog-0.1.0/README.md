# Markdown to Blogger

이 프로젝트는 마크다운 파일을 HTML로 변환하여 Blogger에 게시하는 도구입니다. Python과 Blogger API를 사용하여 마크다운 파일을 블로그 포스트로 쉽게 변환하고 업로드할 수 있습니다.

## 설치 방법

이 도구를 사용하기 전에, Python이 설치되어 있어야 합니다. 그 후에, 필요한 패키지를 설치하기 위해 다음 명령어를 실행하세요:

```bash
poetry install
```

## 사용법

이 도구는 명령줄 인터페이스(CLI)를 통해 다양한 명령어를 제공합니다. 사용 가능한 명령어는 다음과 같습니다:

### 블로그 ID 설정

블로그 ID를 설정하려면 다음 명령어를 사용하세요:

```bash
mdb set_blogid [블로그 ID]
```

### 현재 설정된 블로그 ID 확인

현재 설정된 블로그 ID를 확인하려면 다음 명령어를 사용하세요:

```bash
mdb get_blogid
```

### 마크다운 파일을 HTML로 변환

마크다운 파일을 HTML로 변환하려면 다음 명령어를 사용하세요:

```bash
mdb convert --input [마크다운 파일명] --output [저장될 HTML 파일명]
```

### Client Secret 파일 설정

Google API 사용을 위한 `client_secret.json` 파일을 설정하려면 다음 명령어를 사용하세요:

```bash
mdb set_client_secret [client_secret.json 파일 경로]
```

### 인증 정보 갱신

Google API의 인증 정보를 갱신하려면 다음 명령어를 사용하세요:

```bash
mdb refresh_auth
```

### 마크다운 파일을 Blogger에 게시

마크다운 파일을 Blogger에 직접 게시하려면 다음 명령어를 사용하세요:

```bash
mdb publish --title "[블로그 제목]" [마크다운 파일명]
```

### HTML 파일을 Blogger에 게시

HTML 파일을 Blogger에 게시하려면 다음 명령어를 사용하세요:

```bash
mdb publish_html --title "[블로그 제목]" [HTML 파일명]
```

## 기여하기

프로젝트에 기여하고 싶으신 분은 GitHub를 통해 Pull Request를 보내주시거나, 이슈를 등록해 주세요.
