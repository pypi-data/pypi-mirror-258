from __future__ import annotations

from typing import Annotated
from datetime import datetime
from uuid import UUID
from pydantic import AnyUrl, AwareDatetime, BaseModel, Field, RootModel

from asknews_sdk.dto.base import BaseSchema


class StoryResponseArticleEntities(BaseModel):
    DATE: Annotated[list[str], Field(title='Date')]
    EVENT: Annotated[list[str], Field(title='Event')]
    GPE: Annotated[list[str], Field(title='Gpe')]
    ORG: Annotated[list[str], Field(title='Org')]
    PERSON: Annotated[list[str], Field(title='Person')]


class StoryResponseArticle(BaseModel):
    article_url: Annotated[AnyUrl, Field(title='Article Url')]
    classification: Annotated[list[str], Field(title='Classification')]
    country: Annotated[str, Field(title='Country')]
    domain: Annotated[str, Field(title='Domain')]
    domain_rank: Annotated[int, Field(title='Domain Rank')]
    domain_url: Annotated[AnyUrl, Field(title='Domain Url')]
    eng_ttl: Annotated[str, Field(title='Eng Ttl')]
    entities: StoryResponseArticleEntities
    image_url: Annotated[AnyUrl, Field(title='Image Url')]
    keywords: Annotated[list[str], Field(title='Keywords')]
    language: Annotated[str, Field(title='Language')]
    medeoid_distance: Annotated[float, Field(title='Medeoid Distance')]
    page_content: Annotated[str, Field(title='Page Content')]
    pubDate: Annotated[AwareDatetime, Field(title='Pubdate')]
    summary: Annotated[str, Field(title='Summary')]
    timestamp: Annotated[int, Field(title='Timestamp')]
    title: Annotated[str, Field(title='Title')]
    type: Annotated[str, Field(title='Type')]


class StoryResponseUpdate(BaseModel):
    articles: Annotated[list[StoryResponseArticle], Field(title='Articles')]
    title: Annotated[str, Field(title='Title')]
    summary: Annotated[str, Field(title='Summary')]
    story_update_ts: Annotated[int, Field(title='Story Update Ts')]
    sources_urls: Annotated[dict[str, int], Field(title='Sources Urls')]
    languages_pct: Annotated[dict[str, float], Field(title='Languages Pct')]
    countries_pct: Annotated[dict[str, float], Field(title='Countries Pct')]
    key_takeaways: Annotated[list[str], Field(title='Key Takeaways')]
    contradictions: Annotated[list[str], Field(title='Contradictions')]
    people: Annotated[list[str], Field(title='People')]
    locations: Annotated[list[str], Field(title='Locations')]
    new_information: Annotated[str, Field(title='New Information')]
    image_url: Annotated[AnyUrl, Field(title='Image Url')]
    prompt: Annotated[str, Field(title='Prompt')]


class StoryResponse(BaseSchema):
    uuid: Annotated[UUID, Field(title='Uuid')]
    categories: Annotated[list[str], Field(title='Categories')]
    sources_urls: Annotated[dict[str, int], Field(title='Sources Urls')]
    languages_pct: Annotated[dict[str, float], Field(title='Languages Pct')]
    countries_pct: Annotated[dict[str, float], Field(title='Countries Pct')]
    sentiment: Annotated[list[int], Field(title='Sentiment')]
    n_articles: Annotated[list[int], Field(title='N Articles')]
    current_update_key: Annotated[str, Field(title='Current Update Key')]
    updates: Annotated[dict[str, StoryResponseUpdate], Field(title='Updates')]


class StoriesResponse(BaseSchema, RootModel[list[StoryResponse]]):
    root: Annotated[list[StoryResponse], Field(title='StoriesResponse')]


class SourceReportItem(BaseModel):
    bson_date: Annotated[datetime, Field(title='Bson Date')]
    n_bucket: Annotated[int, Field(title='Number of Buckets')]
    n_selected: Annotated[int, Field(title='Number of Selected')]
    bucket_counts: Annotated[dict[str, int], Field(title='Bucket Counts')]
    selected_counts: Annotated[dict[str, int], Field(title='Selected Counts')]
    bucket_pct: Annotated[dict[str, float], Field(title='Bucket Percentage')]
    selected_pct: Annotated[dict[str, float], Field(title='Selected Percentage')]

class SourceReportResponse(BaseSchema, RootModel[list[SourceReportItem]]):
    root: Annotated[list[SourceReportItem], Field(title='SourceReportResponse')]
