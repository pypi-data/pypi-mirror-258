from asknews_sdk.api.base import BaseAPI
from asknews_sdk.dto.stories import (
    StoriesResponse,
    StoryResponse,
    SourceReportResponse,
)


class StoriesAPI(BaseAPI):
    """
    Stories API

    https://api.asknews.app/docs#/stories
    """
    async def get_stories(
        self,
        query: str | None = None,
        categories: str | None = None,
        start_timestamp: int | None = None,
        end_timestamp: int | None = None,
        full_details: bool = False,
        sort_by_time: bool = False,
        offset: int = 0,
    ) -> StoriesResponse:
        """
        Get the news stories.

        https://docs.asknews.app/#/stories/get_stories

        :param query: The query.
        :type query: str | None
        :param categories: The categories.
        :type categories: str | None
        :param start_timestamp: The start timestamp.
        :type start_timestamp: int | None
        :param end_timestamp: The end timestamp.
        :type end_timestamp: int | None
        :param full_details: Whether to return full details.
        :type full_details: bool
        :param sort_by_time: Whether to sort by time.
        :type sort_by_time: bool
        :param offset: The offset.
        :type offset: int
        :return: The stories response.
        :rtype: StoriesResponse
        """
        response = await self.client.get(
            endpoint="/v1/stories",
            query={
                "query": query,
                "categories": categories,
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "full_details": full_details,
                "sort_by_time": sort_by_time,
                "offset": offset,
            },
            accept=[(StoriesResponse.__content_type__, 1.0)]
        )
        return StoriesResponse.model_validate(response.content)

    async def get_story(self, story_id: str) -> StoryResponse:
        """
        Get a single news story given the ID.

        https://docs.asknews.app/#/stories/get_story

        :param story_id: The story ID.
        :type story_id: str
        :return: The story response.
        :rtype: StoryResponse
        """
        response = await self.client.get(
            endpoint="/v1/stories/{story_id}",
            params={"story_id": story_id},
            accept=[(StoryResponse.__content_type__, 1.0)]
        )
        return StoryResponse.model_validate(response.content)

    async def get_sources_report(
        self,
        n_points: int = 100,
        start_timestamp: int | None = None,
        end_timestamp: int | None = None,
        metric: str = "countries_diversity",
        sampling: str = "1h",
    ) -> SourceReportResponse:
        """
        Get the sources report.

        https://docs.asknews.app/#/stories/get_sources_report

        :param n_points: The number of points.
        :type n_points: int
        :param start_timestamp: The start timestamp.
        :type start_timestamp: int | None
        :param end_timestamp: The end timestamp.
        :type end_timestamp: int | None
        :param metric: The metric.
        :type metric: str
        :param sampling: The sampling.
        :type sampling: str
        :return: The source report response.
        :rtype: SourceReportResponse
        """
        response = await self.client.get(
            endpoint="/v1/stories/sources",
            query={
                "n_points": n_points,
                "start_timestamp": start_timestamp,
                "end_timestamp": end_timestamp,
                "metric": metric,
                "sampling": sampling,
            },
            accept=[(SourceReportResponse.__content_type__, 1.0)]
        )
        # return SourceReportResponse.model_validate(response.content)
        return response.content
