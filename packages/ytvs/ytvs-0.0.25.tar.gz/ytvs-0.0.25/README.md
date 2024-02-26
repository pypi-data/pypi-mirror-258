# TODO
* 여유될때, extractor 부분 좀더 구조화 가능.
* 또한, 각 Resource에서 비디오, 채널등 특화된 추출 코드들을 Extractor로 옮기고, YoutubeBasicInfoExtractor를 상속해서 구성하면
  훨씬 깔끔할듯
* 필요하면, TorNetwork를 이용해서 접근 IP를 감출 수 있음
* 추후, 응답 데이터 빌드 단계는 분리하기.
* requests_oauth, pip install dataclasses-json, isodate, pip install python-youtube, webdriver_manager

# References - thanks
[**pyyoutube**]  https://github.com/sns-sdks/python-youtube/tree/a531987cf5f426170399f227ca07a85ecba1358f
[Youtube-Local] https://github.com/search?q=repo%3Auser234683%2Fyoutube-local%20request_comments&type=code
[Youtube-DL] https://github.com/ytdl-org/youtube-dl/blob/be008e657d79832642e2158557c899249c9e31cd/youtube_dl/extractor/common.py#L1014
[Youtube-Crawler] https://github.com/jaryeonge/youtube-crawler/blob/5af1421ed4a76a1b9ca57ea968c936e63395675f/src/crawling_module/vod_meta.py#L141
[Youtube-Search-Python] https://github.com/GHOSTEPROG-OFFICIAL/youtube-search-python/blob/main/youtubesearchpython/core/comments.py
[Mining] https://github.com/medialab/minet/tree/82d862dbd434d6535a6bec23cfb7c35d864440c0
https://github.com/x4nth055/pythoncode-tutorials/blob/cf194de63299b9a7de25cdd046721da172426e3b/web-scraping/youtube-extractor/extract_video_info.py#L2
# Update
```bash
pip install --upgrade ytvs
```


# Build and publish
```bash
poetry build  # Build
python -m twine upload --skip-existing dist/*   # Deployment
```



# Version history

## 0.0.4
  - API 파라미터는 Keyword parameter로 입력받도록 제약 걸기
  - 각 API 함수의 응답 타입 명시하기
  - build_search_v1_resource_url
  - video.py 76 번째 줄, extract_comments_header_render 부분 수정
  - DataParameterBuilder, kr -> KR 수정
  - extract_comments_header_renderer, 입력 파라미터가 None인 경우 예외처리 추가
  - extract_like_count, extract_view_count
    -> number string 확인 후 예외 처리 추가 필요
