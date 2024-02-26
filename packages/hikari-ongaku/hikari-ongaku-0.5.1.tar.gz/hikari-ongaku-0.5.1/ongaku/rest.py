"""Rest client.

All REST based actions, happen in here.
"""

from __future__ import annotations

import enum
import typing as t

import aiohttp
import hikari

from . import internal
from .abc.filters import Filter
from .abc.lavalink import ExceptionError
from .abc.lavalink import Info
from .abc.player import Player
from .abc.player import PlayerVoice
from .abc.session import Session
from .abc.track import Playlist
from .abc.track import SearchResult
from .abc.track import Track
from .errors import BuildException
from .errors import LavalinkException

_logger = internal.logger.getChild("rest")

if t.TYPE_CHECKING:
    from .client import Client

__all__ = ("RESTClient",)


class _HttpMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class RESTClient:
    """Base REST Client.

    The base REST client, for all rest related actions.

    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    def __init__(self, client: Client) -> None:
        self._client = client

        self._rest_track = RESTTrack(self)
        self._rest_player = RESTPlayer(self)
        self._rest_session = RESTSession(self)

        self._session: aiohttp.ClientSession | None = None

    @property
    def track(self) -> RESTTrack:
        """The track related rest actions."""
        return self._rest_track

    @property
    def player(self) -> RESTPlayer:
        """The player related rest actions."""
        return self._rest_player

    @property
    def session(self) -> RESTSession:
        """The session related rest actions."""
        return self._rest_session

    async def fetch_info(self) -> Info:
        """Fetch information.

        Fetch the information about the Lavalink server.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build `abc.Info`
        TypeError
            When the response was of an incorrect type.

        Returns
        -------
        Info
            Returns an information object.
        """
        try:
            _logger.log(internal.Trace.LEVEL, f"running GET /info")
            resp = await self._rest_handler(
                "/info", self._client._internal.headers, _HttpMethod.GET
            )
        except LavalinkException:
            raise
        except ValueError as e:
            raise LavalinkException(e)

        if isinstance(resp, t.Sequence):
            raise TypeError("Incorrect type provided.")

        try:
            info_resp = Info._from_payload(resp)
        except Exception as e:
            raise BuildException(e)

        return info_resp

    async def _rest_handler(
        self,
        url: str,
        headers: t.Mapping[str, t.Any],
        method: _HttpMethod,
        json: t.Mapping[str, t.Any] | t.Sequence[t.Any] = {},
        params: t.Mapping[str, t.Any] = {},
    ) -> t.Mapping[str, t.Any] | t.Sequence[t.Any]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method.value,
                    self._client._internal.base_uri + url,
                    headers=headers,
                    json=json,
                    params=params,
                ) as response:
                    _logger.log(
                        internal.Trace.LEVEL,
                        f"Received code: {response.status} with response {await response.text()}",
                    )
                    if response.status >= 400:
                        raise LavalinkException(
                            f"A {response.status} error has occurred."
                        )

                    try:
                        payload = await response.json()
                    except Exception:
                        if method == _HttpMethod.DELETE:
                            return {}
                        else:
                            raise ValueError(
                                "Json data was not received from the response."
                            )
                    else:
                        return payload
            except Exception as e:
                raise LavalinkException(e)


class RESTSession:
    """REST Session.

    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    async def update(self, session_id: str) -> Session:
        """Session Update.

        Update the current session.

        Parameters
        ----------
        session_id : str
            The Session ID connected to the update.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the session object.
        TypeError
            When the response was of an incorrect type.

        Returns
        -------
        Session
            The session object information.
        """
        try:
            _logger.log(internal.Trace.LEVEL, f"running PATCH /sessions/{session_id}")
            resp = await self._rest._rest_handler(
                "/sessions/" + session_id,
                self._rest._client._internal.headers,
                _HttpMethod.PATCH,
            )
        except LavalinkException:
            raise
        except ValueError as e:
            raise LavalinkException(e)

        if isinstance(resp, t.Sequence):
            raise TypeError("Incorrect type provided.")

        try:
            session_model = Session._from_payload(resp)
        except Exception as e:
            raise BuildException(e)

        return session_model


class RESTPlayer:
    """REST Player.

    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    async def fetch_all(self, session_id: str) -> t.Sequence[Player] | None:
        """Fetch all players.

        Fetch all of the players in the current session.

        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        TypeError
            When the response was of an incorrect type.

        Returns
        -------
        typing.Sequence[Player]
            The players that are attached to the session.
        """
        try:
            _logger.log(
                internal.Trace.LEVEL, f"running GET /sessions/{session_id}/players"
            )
            resp = await self._rest._rest_handler(
                "/sessions/" + session_id + "/players",
                self._rest._client._internal.headers,
                _HttpMethod.GET,
            )
        except LavalinkException:
            raise
        except ValueError as e:
            raise LavalinkException(e)

        player_list: list[Player] = []

        if isinstance(resp, t.Sequence):
            for value in resp:
                try:
                    player_model = Player._from_payload(value)
                except Exception as e:
                    raise BuildException(e)

                player_list.append(player_model)
        else:
            for _, value in resp.items():
                try:
                    player_model = Player._from_payload(value)
                except Exception as e:
                    raise BuildException(e)

                player_list.append(player_model)

        return player_list

    async def fetch(self, session_id: str, guild_id: hikari.Snowflake) -> Player | None:
        """Fetch a player.

        Fetch a specific player, for the specified Guild id.

        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.
        guild_id : hikari.Snowflake
            The Guild ID that the player is attached to.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        TypeError
            When the response was of an incorrect type.

        Returns
        -------
        Player
            The player that was found for the specified guild.
        """
        try:
            _logger.log(
                internal.Trace.LEVEL,
                f"running GET /sessions/{session_id}/players/{guild_id}",
            )
            resp = await self._rest._rest_handler(
                "/sessions/" + session_id + "/players/" + str(guild_id),
                self._rest._client._internal.headers,
                _HttpMethod.GET,
            )
        except LavalinkException:
            raise
        except ValueError as e:
            raise LavalinkException(e)

        if isinstance(resp, t.Sequence):
            raise TypeError("Incorrect type provided.")

        try:
            player_model = Player._from_payload(resp)
        except Exception as e:
            raise BuildException(e)

        return player_model

    async def update(
        self,
        guild_id: hikari.Snowflake,
        session_id: str,
        *,
        track: hikari.UndefinedNoneOr[Track] = hikari.UNDEFINED,
        position: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        end_time: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        volume: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        paused: hikari.UndefinedOr[bool] = hikari.UNDEFINED,
        filter: hikari.UndefinedNoneOr[Filter] = hikari.UNDEFINED,
        voice: hikari.UndefinedOr[PlayerVoice] = hikari.UNDEFINED,
        no_replace: bool = True,
    ) -> Player:
        """Update a player.

        Update a specific player, for the specified Guild id.

        !!! info
            If no_replace is True, then setting a track to the track option, will not do anything.

        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.
        guild_id : hikari.Snowflake
            The Guild ID that the player is attached to.
        track : hikari.UndefinedNoneOr[Track]
            The track you wish to set.
        position : hikari.UndefinedNoneOr[int]
            The new position for the track.
        end_time : hikari.UndefinedNoneOr[int]
            The end time for the track.
        volume : hikari.UndefinedNoneOr[int]
            The volume of the player.
        paused : hikari.UndefinedNoneOr[bool]
            Whether or not to pause the player.
        filter : hikari.UndefinedNoneOr[Filter]
            The filter you wish to set, or remove.
        voice : hikari.UndefinedNoneOr[PlayerVoice]
            The player voice object you wish to set.
        no_replace : bool
            Whether or not the track can be replaced.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        TypeError
            When the response was of an incorrect type.

        Returns
        -------
        Player
            The player that was found for the specified guild.
        """
        patch_data: dict[str, t.Any] = {}

        if track != hikari.UNDEFINED:
            if track is None:
                patch_data.update(
                    {
                        "track": {
                            "encoded": None,
                        }
                    }
                )
            else:
                patch_data.update(
                    {
                        "track": {
                            "encoded": track.encoded,
                        }
                    }
                )

        if position != hikari.UNDEFINED:
            patch_data.update({"position": position})

        if end_time != hikari.UNDEFINED:
            patch_data.update({"endTime": end_time})

        if volume != hikari.UNDEFINED:
            patch_data.update({"volume": volume})

        if paused != hikari.UNDEFINED:
            patch_data.update({"paused": paused})

        if voice != hikari.UNDEFINED:
            patch_data.update(
                {
                    "voice": {
                        "token": voice.token,
                        "endpoint": voice.endpoint[6:],
                        "sessionId": voice.session_id,
                    }
                }
            )

        if filter != hikari.UNDEFINED:
            if filter is None:
                patch_data.update({"filters": None})
            else:
                patch_data.update({"filters": filter._build()})

        new_headers = self._rest._client._internal.headers.copy()

        new_headers.update({"Content-Type": "application/json"})

        params = {"noReplace": "false"}

        if no_replace:
            params.update({"noReplace": "true"})

        try:
            _logger.log(
                internal.Trace.LEVEL,
                f"running PATCH /sessions/{session_id}/players/{guild_id} with params: {params} and json: {patch_data}",
            )
            resp = await self._rest._rest_handler(
                "/sessions/" + session_id + "/players/" + str(guild_id),
                self._rest._client._internal.headers,
                _HttpMethod.PATCH,
                json=patch_data,
                params=params,
            )
        except LavalinkException:
            raise
        except ValueError as e:
            raise LavalinkException(e)

        if isinstance(resp, t.Sequence):
            raise TypeError("Incorrect type provided.")

        try:
            player_model = Player._from_payload(resp)
        except Exception as e:
            raise BuildException(e)

        return player_model

    async def delete(self, session_id: str, guild_id: hikari.Snowflake) -> None:
        """Delete player.

        Delete a specific player, from the specified guild.

        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.
        guild_id : hikari.Snowflake
            The Guild ID that the player is attached to.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        ValueError
            Json data could not be found or decoded.
        """
        try:
            _logger.log(
                internal.Trace.LEVEL,
                f"running DELETE /sessions/{session_id}/players/{guild_id}",
            )
            await self._rest._rest_handler(
                "/sessions/" + session_id + "/players/" + str(guild_id),
                self._rest._client._internal.headers,
                _HttpMethod.DELETE,
            )
        except LavalinkException:
            raise
        except ValueError as e:
            raise LavalinkException(e)


class RESTTrack:
    """REST Track.

    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    async def load(self, query: str) -> SearchResult | Playlist | Track | None:
        """Load tracks.

        Load tracks to be able to play on a player.

        Parameters
        ----------
        query : str
            The query for a track/url

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            If it fails to build the [SearchResult][ongaku.abc.track.SearchResult], [Playlist][ongaku.abc.track.Playlist] or [Track][ongaku.abc.track.Track]
        TypeError
            When the response was of an incorrect type.

        Returns
        -------
        SearchResult
            If it was not a url, you will always receive this.
        Playlist
            If a playlist url is sent, you will receive this option.
        Track
            If a song/track url is sent, you will receive this option.
        """
        params: dict[str, t.Any] = {"identifier": query}

        try:
            _logger.log(
                internal.Trace.LEVEL, f"running GET /loadtracks with params: {params}"
            )
            resp = await self._rest._rest_handler(
                "/loadtracks",
                self._rest._client._internal.headers,
                _HttpMethod.GET,
                params=params,
            )
        except LavalinkException:
            raise
        except ValueError as e:
            raise LavalinkException(e)

        if isinstance(resp, t.Sequence):
            raise TypeError("Incorrect type provided.")

        load_type = resp["loadType"]

        build = None

        if load_type == "empty":
            _logger.log(internal.Trace.LEVEL, f"loadType is empty.")

        elif load_type == "error":
            _logger.log(internal.Trace.LEVEL, f"loadType caused an error.")
            raise LavalinkException(ExceptionError._from_payload(resp["data"]))

        elif load_type == "search":
            _logger.log(internal.Trace.LEVEL, f"loadType was a search result.")
            build = SearchResult._from_payload(resp["data"])

        elif load_type == "track":
            _logger.log(internal.Trace.LEVEL, f"loadType was a track link.")
            build = Track._from_payload(resp["data"])

        elif load_type == "playlist":
            _logger.log(internal.Trace.LEVEL, f"loadType was a playlist link.")
            build = Playlist._from_payload(resp["data"])

        else:
            raise Exception("An unknown loadType was received.")

        return build

    async def decode(self, code: str) -> Track:
        """Decode a track.

        Decode a track, from its BASE64 Object.

        Parameters
        ----------
        code : str
            The BASE64 code, of the specified track.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            If it fails to build the [SearchResult][ongaku.abc.track.SearchResult], [Playlist][ongaku.abc.track.Playlist] or [Track][ongaku.abc.track.Track]
        TypeError
            When the response was of an incorrect type.

        Returns
        -------
        Track
            The track that came from the encoded code.
        """
        params = {"encodedTrack": code}

        try:
            _logger.log(
                internal.Trace.LEVEL, f"running GET /decodetrack with params: {params}"
            )
            resp = await self._rest._rest_handler(
                self._rest._client._internal.base_uri + "/decodetrack",
                self._rest._client._internal.headers,
                _HttpMethod.GET,
                params=params,
            )
        except LavalinkException:
            raise
        except ValueError as e:
            raise LavalinkException(e)

        if isinstance(resp, t.Sequence):
            raise TypeError("Incorrect type provided.")

        try:
            track = Track._from_payload(resp)
        except Exception as e:
            raise BuildException(e)

        return track

    async def decode_many(self, codes: t.Sequence[str]) -> t.Sequence[Track]:
        """Decode multiple tracks.

        Decode multiple tracks, via their BASE64 codes.

        Parameters
        ----------
        codes : typing.Sequence[str]
            The BASE64 codes, of the specified tracks.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            If it fails to build the [SearchResult][ongaku.abc.track.SearchResult], [Playlist][ongaku.abc.track.Playlist] or [Track][ongaku.abc.track.Track]

        Returns
        -------
        typing.Sequence[Track]
            The track that came from the encoded code.
        """
        try:
            _logger.log(
                internal.Trace.LEVEL, f"running GET /decodetracks with json: {[*codes]}"
            )
            resp = await self._rest._rest_handler(
                self._rest._client._internal.base_uri + "/decodetracks",
                self._rest._client._internal.headers,
                _HttpMethod.GET,
                json=[*codes],
            )
        except LavalinkException:
            raise
        except ValueError as e:
            raise LavalinkException(e)

        tracks: list[Track] = []

        if isinstance(resp, t.Sequence):
            for track in resp:
                try:
                    track = Track._from_payload(track)
                except Exception as e:
                    raise BuildException(e)

                tracks.append(track)

        else:
            for _, track in resp.values():
                try:
                    track = Track._from_payload(track)
                except Exception as e:
                    raise BuildException(e)

                tracks.append(track)

        return tracks


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
