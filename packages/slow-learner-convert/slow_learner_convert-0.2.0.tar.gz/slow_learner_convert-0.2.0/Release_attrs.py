import attrs
from typing import List
from typing import Literal
from typing_extensions import NotRequired
from typing import Optional
from typing import TypedDict
from typing import Union


@attrs.define
class ReleaseAuthor:
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: Literal['']
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: Literal['User']
    site_admin: Literal[False]


@attrs.define
class ReleaseAssetsItemUploader:
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: Literal['']
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: Literal['User']
    site_admin: Literal[False]


@attrs.define
class ReleaseAssetsItem:
    url: str
    id: int
    node_id: str
    name: str
    label: Optional[str]
    uploader: ReleaseAssetsItemUploader
    content_type: Union[Literal['text/javascript'], Literal['application/javascript'], Literal['application/x-javascript'], Literal['application/zip']]
    state: Literal['uploaded']
    size: int
    download_count: int
    created_at: str
    updated_at: str
    browser_download_url: str


@attrs.define
class ReleaseReactions:
    url: str
    total_count: int
    laugh: int
    hooray: int
    confused: Literal[0]
    heart: int
    rocket: int
    eyes: int


@attrs.define
class Release:
    url: str
    assets_url: str
    upload_url: str
    html_url: str
    id: int
    author: ReleaseAuthor
    node_id: str
    tag_name: str
    target_commitish: str
    name: str
    draft: Literal[False]
    prerelease: bool
    created_at: str
    published_at: str
    assets: List[ReleaseAssetsItem]
    tarball_url: str
    zipball_url: str
    body: str
    reactions: NotRequired[ReleaseReactions]