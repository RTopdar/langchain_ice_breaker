from langchain_community.utilities import GoogleSerperAPIWrapper

from dotenv import load_dotenv

load_dotenv()


def get_profile_url(name: str):


    search = GoogleSerperAPIWrapper(type="search", include_domains=["linkedin.com"])
    res = search.results(f"{name} linkedin")
    return res["organic"][0]["link"]


if __name__ == "__main__":
    print(get_profile_url("Rounak Topdar"))
