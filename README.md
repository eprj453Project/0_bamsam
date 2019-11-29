# :clipboard: README



### :slightly_smiling_face: 팀원

|     이름     |                   역할                   |             정보             |
| :----------: | :--------------------------------------: | :--------------------------: |
|    박상원    |  User 백엔드, Movie 백엔드, JavaScript   | 식품산업외식학 한국조리 전공 |
| 이해인(팀장) | HTML, CSS, BootStrap, Movie 백엔드, 배포 |     미술대학 한국화 전공     |



****



*\# 목표서비스 구현 및 실제 구현 정도 (가능하다면 일자별 업무 진행 정도 포함)*

### :chart_with_upwards_trend: 진행 상황

#### 191122(금)

> - project 시작 : 환경변수와 라이브러리 설치, 프로젝트 시작 전 기본 틀 작성
>   **=>** *Django - settings, models, forms, urls, templates ...ect*
> - 소셜로그인 추가, 구글로 로그인 시도 시, `profile/` 이라는 알 수 없는 경로로 들어가게된다. **=>** settings.py 에 `LOGIN_REDIRECT_URL` 추가

#### 191123(토)

> - Model 수정
>   - User Model, Movie Model이 가지고 있어야 할 FIeid 재정의
> - 새로운 Model 정의
>   - 쪽지를 위한 Message Model 정의
>   - BLANK=True와 null=True를 헷갈릴 수 있다.
> - Movie DB API에서 필요한 정보를 추출해 영화 DB구축

#### 191124(일)

> - 메세지 기능 구현 중
> - git branch를 잘못 선택하여 약 7시간의 작업물 모두 사라짐.
> - 한번 사용한 branch는 더 이상 사용하지 않는 것이 좋다.
> - git push branch **=>** git checkout master **=>** merge **=>**  

#### 191125(월)

> - 유저 정보, 영화 정보, 댓글 달기, 댓글 수정 등 대부분의 백엔드 기능 구현
> - 댓글 수정 시 form 페이지로 다시 redirect하지 않고 댓글과 수정 form이 서로 번갈아가면서 display block과 display none을 가지며 전환되도록 JS코드 작성. 
> - 댓글 수정 form 클릭시 스크롤 최상단 이동 -> display 변경 함수에 return false를 주어 스크롤 이동 방지.
> - 메세지 기능 구현을 위해 z-index와 modal을 이용해 주위 화면은 반투명해지며 클릭이 안되게, modal만 z-index를 크게 주어 메세지를 보내는 창을 만들었으나 이미 bootstrap의 modal에서 전부 제공해주는 기능이었음. 
>
> ```html
> <a id="sendBtn" class="btn btn-primary mt-3" href="#">메세지 보내기</a>
> ```
>
> ```javascript
> const modal = document.querySelector('#modal')
>    const sendBtn = document.querySelector('#sendBtn')
>    const dimm = document.createElement('div')
>    const closeBtn = document.querySelector('.close')
>    sendBtn.onclick = function(){
>      document.body.appendChild(dimm)
>      dimm.setAttribute('class','dimm');
>      dimm.style.display = 'block'
>      modal.style.display = 'block'
>      modal.style.zIndex = '1'
>    }
> ```
>
> 편하고 간결하게 modal에서 제공해주는 기능을 쓰기로 함.
>
> - json.py를 만들어서 loaddata를 함 (genres, casts, movies)
> - HTML 디자인 시작 **=>** bootstrap, style ... ect
> - static을 가져올 때 서버를 재 시작해주어야 불러올 수 있는 경우가 多
> - ManyToMany Field은 json파일로 불러올 때 주의
> - 로그인폼에 소셜로그인, 회원가입까지 담아서 디자인
> - 유저를 반겨주는 프롤로그 페이지와 영화추천 리스트를 출력하는 페이지를 디자인

​	

#### 191126(화)

> - django와 javascript로만으로 짰던 평점 작성, 수정, 삭제를 Vue.js를 이용한 비동기 형태로 변경하는 과정에서 문법 충돌. 전체 페이지의 url 요청을 전부 수정할수도 있는 대작업이 예상됨.
> - Vue.js와 연동하는 과정에서 일어나는 충돌들을 해결하지 못하고 다시 동기로 전환. 비동기를 완전히 배제하고 짠 백엔드 코드에 프론트엔드를 붙이는건 매우 복잡하기 때문에 처음부터 프론트엔드를 염두에 두고 백엔드 코드를 짜야함.

#### 191127(수)

> - Jqeury를 사용한 이미지 슬라이더 작성, 태그구성을 잘 확인해야 할 것
> - bootstrap css가 다른 css보다 우선순위가 되는 경우가 많기때문에 유의해야 할 것
> - if문과 닫히는 태그가 있어도 그 사이를 감싸서 속성을 줄 수있다.
> - 배포시 일어나는 에러가 어디서부터 어디까지인지 확인불가. 배포는 한번도 해본적 없기 때문에 에러 수정이 매우 어려움.
> - 자바스크립트 문법 또한 django template 문법과 충돌 발생 (url namespace의 경우 "" 안에 '' 가 들어가 있는데 자바스크립트는 이를 허용하지 않음. "" 안에 ''가 없는 url 접근으로 해결)
>
> ```javascript
> moreInfo.href = `/movies/movie_detail/${movieId}/` ----> ok
> moreInfo.href = `{% url 'movies:movie_modify' ${movieId} %}` ----> error
> ```
>
> - 편하다고 그 방법밖에 알지 못하면 여러 상황을 해결하는 능력이 부족해진다. 기본적으로 여러가지 방법을 알고 있는 상태에서 가장 편한 방법을 찾아 쓰도록 하자.
> - 백엔드와 Vue.js를 연동해서 썼다면 더 효율적인 코드가 되었을텐데 자바스크립트만으로는 백엔드(db)에 접근하는게 한계가 있어서 비효율적인 코드가 짜여질 수 밖에 없음. 
> - 서버 500 error 발생 시, 서버 재 구축이 필요함, 서버 구축을 위해 변경된 reqruirments.txt 때문에 깃헙에서 메일이 오지만 신경쓰지 않아도 된다고 함
> - 서버 구축 도중에는 requirments를 수정하면 안되므로 기본 셋팅을 확실하게,
> - 100MB가 넘는 파일은 commit을 하게되면 error가 난다. 따로 파일을 github large file 을 이용하여 파일 수정이 필요, 하지만 이미 100MB이상의 파일의 커밋이 저장되어있으면 커밋을 지우거나 새로 fork를 떠야 한다.

#### 191128(목)

> - css를 위해 추가한 js가 main.html의 navBar에 영향을 주는 것을 발견후 고침

****



###  :pushpin: ERD

- 데이터베이스 모델링 ([entity-relationship diagram)](http://www.terms.co.kr/ERD.htm))
- [ERD Design Site](https://www.erdcloud.com/)

[![20191128_160014](https://user-images.githubusercontent.com/52685258/69784070-4414d900-11f8-11ea-8b4b-454c2720b8e7.png)



****



### :pushpin: 핵심 기능

1. 로그인, 회원가입 등 기본기능
2. 구글, 카카오톡, 네이버 소셜로그인 기능
3. 영화 장르에 따른 추천영화 기능
4. 영화 리스트에서 iframe을 이용한 티저영상, 상세보기 기능
5. 유저 간 메세지 남기기 기능
6. 댓글 및 평점 남기기 기능
7. 관리자 권한을 가진 유저의 영화 정보, 유저 정보 수정 기능



****



### :pushpin: 배포 서버

[bamsam.pr73cnh8mn.ap-northeast-2.elasticbeanstalk.com](http://bamsam.pr73cnh8mn.ap-northeast-2.elasticbeanstalk.com/) 



****



### :pencil: 후기

| 박상원                                                       |
| ------------------------------------------------------------ |
| Vue.js의 component 개념을 이용한 비동기 처리로 프로젝트를 완성하려 했으나 숙련도 부족으로 실패했다. 최소한의 비동기 처리를 위해 Javascript로 코딩을 했으며, 백엔드는 Django를 이용해 구축했다. 교육시간에는 짧은 시간에 최대한 많은 것을 배울 수 있도록 ssafy의 방향과 강사님의 교육방식에 맞추어 조금은 빠르지만 쉽게 배울 수 있는 개념들을 배웠다. 그러나 실제 원하는대로 코딩을 하려고 보니 때로는 어쩔 수 없이 어려운 방식을 선택해 돌아가야 하는 경우가 생겼다. 쉽다고 그 방법만 고집하기보단 여러 가지 방법을 알고 있는 상태에서 상황에 가장 맞는 방법을 찾는 것이 제일 좋은 방법이라는 생각이 들었다. |

| 이해인                                                       |
| ------------------------------------------------------------ |
| 장기간의 django 프로젝트와 교육을 했음에도 불구하고 협동 프로젝트를 하면서 날린 시간이 많았다. 특히나 git과 서버(eb)에 관련된 작업을 할 때는 경험이 부족해서 몇시간동안 작업한 내용을 날리기도하고, 깃이 꼬여 클론을 서너번 받기도 했다. 혼자 프로젝트를 할 때 겪지못했던 어려움을 마주하게 되니 합을 맞추는 부분이 굉장히 어려웠고 소통이 잦아야 했다. 하지만 협업으로 인해 파트가 자세히 나눠지면서 각자 할 일에대해 집중하게 되니 프로젝트의 속도향상을 체감할 수 있었다. |





