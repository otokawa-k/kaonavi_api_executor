from .auth.api_access_token_fetcher import ApiAccessTokenFetcher
from .api_executor import ApiExecutor
from .api.get_member_api import GetMemberApi
from .http_client.http_methods import Post


def main():
    fetcher = ApiAccessTokenFetcher(Post())
    token = fetcher.fetch_access_token()
    api_model = GetMemberApi(token=token)
    api_executor = ApiExecutor(api_model)
    response = api_executor.execute()
    print(response.updated_at)

if __name__ == "__main__":
    main()
