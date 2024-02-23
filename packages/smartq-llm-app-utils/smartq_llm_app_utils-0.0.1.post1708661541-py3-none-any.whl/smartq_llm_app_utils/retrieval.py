from langchain_core.retrievers import BaseRetriever
import json
from langchain_core.documents.base import Document
from typing import (
    ClassVar,
    Collection,
    Dict,
    List,
)
from langchain_core.pydantic_v1 import Field, root_validator

EKM_DOC_RETRIEVAL_API_URL = 'http://sys-ekm/sys/sys-ekm/api/doc_retrieval/v1/search'


class SmartQLasRetriever(BaseRetriever):
    """
    以VectorStore.as_retriever(kwargs)為例, kwargs分成search_type（Optional[str]）及search_kwargs
    Optional[Dict]，search_kwargs這個dict裡可以有k, score_threshold, fetch_k, lambda_mult & filter.
    在construct SmartQLasRetriever時做為constructor parameters提供,
    ex：SmartQLasRetriever(user_email=..., search_type=..., search_kwargs={})
    """

    user_email: str = ''
    search_type: str = "similarity"
    """Type of search to perform. Defaults to "similarity"."""
    search_kwargs: dict = Field(default_factory=dict)
    """Keyword arguments to pass to the search function."""
    ekm_doc_retrieval_api_url: str = EKM_DOC_RETRIEVAL_API_URL
    """URL of SmartQ LAS EKM doc retrieval API, 
       ex: http://sys-ekm/sys/sys-ekm/api/doc_retrieval/v1/search"""
    app_id: str = 'app01'
    """LLM app id, ex: app01"""
    multi_query: bool = False,
    """是否使用Multiple query(ie: query transformation), 回傳多查詢結果的不重複聯集"""
    hyde: bool = False,
    """是否使用 HyDE(ie: 假設性文字嵌入)"""
    contextual_compression: bool = False
    """是否使用語境壓縮(LLMChainFilter)"""
    rerank: bool = False
    """是否使用 rerank"""

    allowed_search_types: ClassVar[Collection[str]] = (
        "similarity",
        "similarity_score_threshold",
        "mmr",
    )

    @root_validator()
    def validate_search_type(cls, values: Dict) -> Dict:
        """Validate search type."""
        # TODO: 對其它欄位的驗證
        search_type = values["search_type"]
        if search_type not in cls.allowed_search_types:
            raise ValueError(
                f"search_type of {search_type} not allowed. Valid values are: "
                f"{cls.allowed_search_types}"
            )
        if search_type == "similarity_score_threshold":
            score_threshold = values["search_kwargs"].get("score_threshold")
            if (score_threshold is None) or (not isinstance(score_threshold, float)):
                raise ValueError(
                    "`score_threshold` is not specified with a float value(0~1) "
                    "in `search_kwargs`."
                )
        return values

    def _get_relevant_documents(self, query: str) -> List[Document]:
        import requests

        # 設定 API 的 URL 和參數
        # ex: http://127.0.0.1:8000/sys/sys-ekm/doc_retrieval/v1/search/app01?
        # user_email=ken.hu@hwacom.com&query=查詢語句&search_type=similarity&k=3
        url = f'{self.ekm_doc_retrieval_api_url}/{self.app_id}'
        params = {
            "user_email": self.user_email,
            "query": query,
            "search_type": self.search_type,
            "multi_query": self.multi_query,
            "hyde": self.hyde,
            "rerank": self.rerank
        }
        params.update(self.search_kwargs)

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"call EKM API fails: status_code={response.status_code}, "
                            f"detail={json.loads(response.text)['detail']}")
        data: list[dict] = response.json()
        return [Document(page_content=d['page_content'], metadata=d['metadata']) for d in data]


if __name__ == '__main__':
    # Test Environment:
    #   EKM backend: local
    #   Qdrant,Redis: remote las-rd2-vm2 VM
    # If use EKM backend running on remote, set ekm_doc_retrieval_api_url as:
    #    http://127.0.0.1:8000/sys/sys-ekm/api/doc_retrieval/v1/search (note: with 'api')
    #
    # ssh -i ~/Documents/rd2-las-vm-1_key.pem -L 8000:localhost:8000 azureuser@las-rd2.eastasia.cloudapp.azure.com
    # kubectl port-forward service/sys-ekm 800:80
    from qdrant_client.http.models.models import Filter, FieldCondition, MatchValue

    query = "大門門頂匾額上的「福威鏢局」四個字是什麼顏色？"
    filter = Filter(
        must=[
            FieldCondition(
                key="metadata.chapter",
                match=MatchValue(value=1)
            )
        ]
    )

    # ekm_doc_retrieval_api_url = 'http://127.0.0.1:8000/sys/sys-ekm/api/doc_retrieval/v1/search'
    ekm_doc_retrieval_api_url = 'http://127.0.0.1:8000/sys/sys-ekm/doc_retrieval/v1/search'
    retriever = SmartQLasRetriever(app_id='app01',
                                   user_email='yh.leu@hwacom.com',
                                   search_type='similarity_score_threshold',
                                   search_kwargs={'k': 3, 'score_threshold': 0.7, 'filter': filter},
                                   ekm_doc_retrieval_api_url=ekm_doc_retrieval_api_url,
                                   multi_query=True,
                                   contextual_compression=True,
                                   rerank=False
                                   )
    print(retriever.ekm_doc_retrieval_api_url)
    try:
        docs: list[Document] = retriever.get_relevant_documents(query='公司總部在哪裡?')
        print(f'found {len(docs)} documents')
        print('\n\n####\n\n'.join([d.page_content for d in docs]))
    except Exception as e:
        print(e)

    # import requests
    # filter = {
    #     "must": [
    #         { "key": "city", "match": { "value": "London" } },
    #         { "key": "color", "match": { "value": "red" } }
    #     ]
    # }
    # url = 'http://127.0.0.1:8000/sys/sys-ekm/doc_retrieval/v1/test-filter'
    # params = {
    #     "filter": filter
    # }
    # response = requests.get(url, params=params)