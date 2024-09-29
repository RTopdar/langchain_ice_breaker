import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    This function is going to be used to scrap information from Linkedin profiles.
    We will manually scrape the information from the Linkedin profile page.
    """
    api_key = os.environ.get("PROXYCURL_API_KEY")
    headers = {"Authorization": "Bearer " + api_key}

    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"

    params = {
        "linkedin_profile_url": f"{linkedin_profile_url}",
        "extra": "include",
        "github_profile_id": "include",
        "facebook_profile_id": "include",
        "twitter_profile_id": "include",
        "personal_contact_number": "include",
        "personal_email": "include",
        "inferred_salary": "include",
        "skills": "include",
        "use_cache": "if-present",
        "fallback_to_cache": "on-error",
    }

    response = requests.get(api_endpoint, params=params, headers=headers)
    return response.json()


def remove_empty_keys(data):
    """
    Remove keys with empty values from a dictionary.
    """
    keys_to_remove = ["people_also_viewed", "similarly_named_profiles"]
    if isinstance(data, dict):
        return {
            k: remove_empty_keys(v)
            for k, v in data.items()
            if v and k not in keys_to_remove
        }
    elif isinstance(data, list):
        return [remove_empty_keys(item) for item in data]
    else:
        return data


if __name__ == "__main__":
    res = scrape_linkedin_profile(linkedin_profile_url="linkedin.com/in/rtopdar")
    cleaned_res = remove_empty_keys(res)
    print(cleaned_res)
