from typing import Optional

from ..jobs import (
    Enum,
    JobType,
    JobResponse,
    Country,
    DescriptionFormat
)


class Site(Enum):
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    ZIP_RECRUITER = "zip_recruiter"
    GLASSDOOR = "glassdoor"


class ScraperInput:
    def __init__(self, site_type: list[Site], search_term: Optional[str] = None, location: Optional[str] = None,
                 country: Optional[Country] = Country.USA, distance: Optional[int] = None, is_remote: bool = False,
                 job_type: Optional[JobType] = None, easy_apply: Optional[bool] = None, offset: int = 0,
                 linkedin_fetch_description: bool = False, linkedin_company_ids: Optional[list[int]] = None,
                 description_format: Optional[DescriptionFormat] = DescriptionFormat.MARKDOWN, results_wanted: int = 15,
                 hours_old: Optional[int] = None):
        self.site_type = site_type
        self.search_term = search_term
        self.location = location
        self.country = country
        self.distance = distance
        self.is_remote = is_remote
        self.job_type = job_type
        self.easy_apply = easy_apply
        self.offset = offset
        self.linkedin_fetch_description = linkedin_fetch_description
        self.linkedin_company_ids = linkedin_company_ids
        self.description_format = description_format
        self.results_wanted = results_wanted
        self.hours_old = hours_old


class Scraper:
    def __init__(self, site: Site, proxy: list[str] | None = None):
        self.site = site
        self.proxy = (lambda p: {"http": p, "https": p} if p else None)(proxy)

    def scrape(self, scraper_input: ScraperInput) -> JobResponse: ...
