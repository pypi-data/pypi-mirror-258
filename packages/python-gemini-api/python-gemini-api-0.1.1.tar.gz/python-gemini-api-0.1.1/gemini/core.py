# Copyright 2024 Minwoo(Daniel) Park, MIT License
import os
import re
import json
import base64
import random
import string
import requests
import browser_cookie3
from typing import Optional, Any

try:
    from deep_translator import GoogleTranslator
    from google.cloud import translate_v2 as translate
except ImportError:
    pass

from .constants import (
    ALLOWED_LANGUAGES,
    REQUIRED_COOKIE_LIST,
    SESSION_HEADERS,
    TEXT_GENERATION_WEB_SERVER_PARAM,
    SUPPORTED_BROWSERS,
    Tool,
)
from .models.base import (
    Candidate,
    GeminiOutput,
    GeneratedImage,
    WebImage,
)
from .models.exceptions import (
    APIError,
    GeminiError,
    TimeoutError,
)
from .utils import (
    extract_cookies_from_brwoser,
)


class Gemini:
    """
    Represents a Gemini instance for interacting with the Google Gemini service.

    Attributes:
        session (requests.Session): Requests session object.
        cookies (dict): Dictionary containing cookies (__Secure-1PSID, __Secure-1PSIDTS, __Secure-1PSIDCC, NID) with their respective values.
        timeout (int): Request timeout in seconds. Defaults to 20.
        proxies (dict): Proxy configuration for requests.
        language (str): Natural language code for translation (e.g., "en", "ko", "ja").
        conversation_id (str): ID for fetching conversational context.
        auto_cookies (bool): Flag indicating whether to retrieve a token from the browser.
        google_translator_api_key (str): Google Cloud Translation API key.
        run_code (bool): Flag indicating whether to execute code included in the answer (IPython only).
    """

    __slots__ = [
        "session",
        "cookies",
        "timeout",
        "proxies",
        "language",
        "conversation_id",
        "auto_cookies",
        "google_translator_api_key",
        "run_code",
    ]

    def __init__(
        self,
        auto_cookies: bool = False,
        session: Optional[requests.Session] = None,
        cookies: dict = None,
        timeout: int = 30,
        proxies: Optional[dict] = None,
        language: Optional[str] = None,
        conversation_id: Optional[str] = None,
        google_translator_api_key: Optional[str] = None,
        run_code: bool = False,
    ):
        """
        Initialize the Gemini instance.

        Args:
            session (requests.Session, optional): Requests session object.
            cookies (dict, optional): Dictionary containing cookies (__Secure-1PSID, __Secure-1PSIDTS, __Secure-1PSIDCC, NID) with their respective values.
            timeout (int, optional): Request timeout in seconds. Defaults to 20.
            proxies (dict, optional): Proxy configuration for requests.
            language (str, optional): Natural language code for translation (e.g., "en", "ko", "ja").
            conversation_id (str, optional): ID for fetching conversational context.
            google_translator_api_key (str, optional): Google Cloud Translation API key.
            run_code (bool, optional): Flag indicating whether to execute code included in the answer (IPython only).
            auto_cookies (bool, optional): Flag indicating whether to retrieve a token from the browser.
        """
        self.auto_cookies = auto_cookies
        self.proxies = proxies or {}
        self.timeout = timeout
        self.cookies = cookies or self._get_cookies(auto_cookies) or {}
        self.session = self._set_session(session)
        self.SNlM0e = self._get_snim0e()
        self.conversation_id = conversation_id or ""
        self.language = language or os.getenv("GEMINI_LANGUAGE")
        self.google_translator_api_key = google_translator_api_key
        self.run_code = run_code
        self._reqid = int("".join(random.choices(string.digits, k=4)))
        self.response_id = ""
        self.choice_id = ""
        self.og_pid = ""
        self.rot = ""
        self.exp_id = ""
        self.init_value = ""

    def _get_cookies_from_browser(self) -> None:
        """
        Extracts the specified Bard cookies from the browser's cookies.

        This function searches for the specified Bard cookies in various web browsers
        installed on the system. It supports modern web browsers and operating systems.

        Returns:
            dict: A dictionary containing the extracted Bard cookies.

        Raises:
            Exception: If no supported browser is found or if there's an issue with cookie extraction.
        """

        for browser_fn in SUPPORTED_BROWSERS:
            try:
                print(
                    f"Trying to automatically retrieve cookies from {browser_fn} using the browser_cookie3 package."
                )
                cj = browser_fn(domain_name=".google.com")
                found_cookies = {
                    cookie.name: cookie.value
                    for cookie in cj
                    if cookie.name.startswith("__Secure-1PSID")
                }
                self.cookies.update(found_cookies)
                if REQUIRED_COOKIE_LIST.issubset(found_cookies.keys()):
                    break
            except Exception as e:
                continue  # Ignore exceptions and try the next browser function

        if not self.cookies:
            raise ValueError(
                "Failed to get cookies. Set 'cookies' argument or 'auto_cookies' as True."
            )
        elif not REQUIRED_COOKIE_LIST.issubset(self.cookies.keys()):
            print(
                "Some recommended cookies not found: '__Secure-1PSIDTS', '__Secure-1PSIDCC', '__Secure-1PSID', and 'NID'."
            )

    def _get_cookies(self, auto_cookies: bool) -> dict:
        """
        Get the Gemini API token either from the provided token or from the browser cookie.

        Args:
            auto_cookies (bool): Whether to extract the token from the browser cookie.

        Returns:
            dict: The dictionary containing the extracted cookies.

        Raises:
            Exception: If the token is not provided and can't be extracted from the browser.
        """
        if os.getenv("__Secure-1PSID"):
            self.cookies.update({c: os.getenv(c) for c in REQUIRED_COOKIE_LIST})
        elif auto_cookies:
            self.cookies = extract_cookies_from_brwoser()
        elif not self.auto_cookies and self.cookies == {}:
            self.auto_cookies = True
            print(
                "Cookie loading issue, try auto_cookies set to True. Restart browser, log out, log in for Gemini Web UI to work. Keep single browser open."
            )
        else:
            raise Exception(
                "Gemini cookies must be provided as the 'cookies' argument or extracted from the browser."
            )

    def _set_session(self, session: Optional[requests.Session]) -> requests.Session:
        """
        Get the requests Session object.

        Args:
            session (requests.Session): Requests session object.

        Returns:
            requests.Session: The Session object.
        """
        if session is not None:
            return session
        elif not self.cookies:
            raise ValueError("Failed to set session. 'cookies' dictionary is empty.")

        session = requests.Session()
        session.headers = SESSION_HEADERS
        session.proxies = self.proxies

        if self.cookies is not None:
            session.cookies.update(self.cookies)

        return session

    def _get_snim0e(self) -> str:
        """
        Get the SNlM0e value from the Gemini API response.

        Returns:
            str: SNlM0e value.
        Raises:
            Exception: If the __Secure-1PSID value is invalid or SNlM0e value is not found in the response.
        """
        response = self.session.get(
            "https://gemini.google.com/app", timeout=self.timeout, proxies=self.proxies
        )
        if response.status_code != 200:
            raise Exception(
                f"Response status code is not 200. Response Status is {response.status_code}"
            )
        snim0e = re.search(r"SNlM0e\":\"(.*?)\"", response.text)
        if not snim0e:
            raise Exception(
                "SNlM0e value not found. Double-check cookies dict value or pass it as Gemini(cookies=Dict())"
            )
        return snim0e.group(1)

    def generate_content(
        self,
        prompt: str,
        session: Optional["GeminiSession"] = None,
        image: Optional[bytes] = None,
        tool: Optional[Tool] = None,
    ) -> dict:
        """
        Get an answer from the Gemini API for the given input text.

        Example:
        >>> cookies = Dict()
        >>> Gemini = Gemini(cookies=cookies)
        >>> response = Gemini.get_answer("나와 내 동년배들이 좋아하는 뉴진스에 대해서 알려줘")
        >>> print(response['content'])

        Args:
            prompt (str): Input text for the query.
            image (bytes): Input image bytes for the query, support image types: jpeg, png, webp
            image_name (str): Short file name
            tool : tool to use can be one of Gmail, Google Docs, Google Drive, Google Flights, Google Hotels, Google Maps, Youtube

        Returns:
            dict: Answer from the Gemini API in the following format:
                {
                    "content": str,
                    "conversation_id": str,
                    "response_id": str,
                    "factuality_queries": list,
                    "text_query": str,
                    "choices": list,
                    "links": list,
                    "images": list,
                    "program_lang": str,
                    "code": str,
                    "status_code": int
                }
        """
        if self.google_translator_api_key is not None:
            google_official_translator = translate.Client(
                api_key=self.google_translator_api_key
            )

        # [Optional] Language translation
        if (
            self.language is not None
            and self.language not in ALLOWED_LANGUAGES
            and self.google_translator_api_key is None
        ):
            translator_to_eng = GoogleTranslator(source="auto", target="en")
            prompt = translator_to_eng.translate(prompt)
        elif (
            self.language is not None
            and self.language not in ALLOWED_LANGUAGES
            and self.google_translator_api_key is not None
        ):
            prompt = google_official_translator.translate(prompt, target_language="en")
        data = {
            "at": self.SNlM0e,
            "f.req": json.dumps(
                [None, json.dumps([[prompt], None, session and session.metadata])]
            ),
        }

        # Get response
        try:
            response = self.session.post(
                "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
                data=data,
                timeout=self.timeout,
                proxies=self.proxies,
            )
        except:
            raise TimeoutError(
                "Request timed out. If errors persist, increase the timeout parameter in the Gemini class to a higher number of seconds."
            )

        if response.status_code != 200:
            raise APIError(f"Request failed with status code {response.status_code}")
        else:
            try:
                body = json.loads(
                    json.loads(response.text.split("\n")[2])[0][2]
                )  # Generated texts
                if not body[4]:
                    body = json.loads(
                        json.loads(response.text.split("\n")[2])[4][2]
                    )  # Non-textual data formats.
                if not body[4]:
                    raise APIError(
                        "Failed to parse body. The response body is unstructured. Please try again."
                    )  # Fail to parse
            except Exception:
                raise APIError(
                    "Failed to parse candidates. Unexpected structured response returned. Please try again."
                )  # Unexpected structured response

            try:
                candidates = []
                for candidate in body[4]:
                    web_images = (
                        candidate[4]
                        and [
                            WebImage(
                                url=image[0][0][0], title=image[2], alt=image[0][4]
                            )
                            for image in candidate[4]
                        ]
                        or []
                    )
                    generated_images = (
                        candidate[12]
                        and candidate[12][7]
                        and candidate[12][7][0]
                        and [
                            GeneratedImage(
                                url=image[0][3][3],
                                title=f"[Generated image {image[3][6]}]",
                                alt=image[3][5][i],
                                cookies=self.cookies,
                            )
                            for i, image in enumerate(candidate[12][7][0])
                        ]
                        or []
                    )
                    candidates.append(
                        Candidate(
                            rcid=candidate[0],
                            text=candidate[1][0],
                            web_images=web_images,
                            generated_images=generated_images,
                        )
                    )
                if not candidates:
                    raise GeminiError(
                        "Failed to generate candidates. No data of any kind returned. If this issue persists, please submit an issue at https://github.com/dsdanielpark/Gemini-API/issues."
                    )
                generated_content = GeminiOutput(
                    metadata=body[1], candidates=candidates
                )
            except IndexError:
                raise APIError(
                    "Failed to parse response body. Data structure is invalid. If this issue persists, please submit an issue at https://github.com/dsdanielpark/Gemini-API/issues."
                )
        # Retry to generate content by updating cookies and session
        if not generated_content:
            print(
                "Using the `browser_cookie3` package, automatically refresh cookies, re-establish the session, and attempt to generate content again."
            )
            for _ in range(2):
                self.cookies = self._get_cookies(True)
                self.session = self._set_session(None)
                try:
                    generated_content = self.generate_content(
                        prompt, session, image, tool
                    )
                    break
                except:
                    print(
                        "Failed to establish session connection after retrying. If this issue persists, please submit an issue at https://github.com/dsdanielpark/Gemini-API/issues."
                    )
            else:
                raise APIError("Failed to generate content.")

        return generated_content

    def speech(self, prompt: str, lang: str = "en-US") -> dict:
        """
        Get speech audio from Gemini API for the given input text.

        Example:
        >>> cookies = Dict()
        >>> Gemini = Gemini(cookies=cookies)
        >>> audio = Gemini.speech("Say hello!")
        >>> with open("Gemini.ogg", "wb") as f:
        >>>     f.write(bytes(audio['audio']))

        Args:
            prompt (str): Input text for the query.
            lang (str, optional, default = "en-US"): Input language for the query.

        Returns:
            dict: Answer from the Gemini API in the following format:
            {
                "audio": bytes,
                "status_code": int
            }
        """
        params = {
            "bl": TEXT_GENERATION_WEB_SERVER_PARAM,
            "_reqid": str(self._reqid),
            "rt": "c",
        }

        prompt_struct = [[["XqA3Ic", json.dumps([None, prompt, lang, None, 2])]]]

        data = {
            "f.req": json.dumps(prompt_struct),
            "at": self.SNlM0e,
        }

        # Get response
        response = self.session.post(
            "https://gemini.google.com/_/BardChatUi/data/batchexecute",
            params=params,
            data=data,
            timeout=self.timeout,
            proxies=self.proxies,
        )

        # Post-processing of response
        response_dict = json.loads(response.content.splitlines()[3])[0][2]
        if not response_dict:
            return {
                "content": f"Response Error: {response.content}. "
                f"\nUnable to get response."
                f"\nPlease double-check the cookie values and verify your network environment or google account."
            }
        resp_json = json.loads(response_dict)
        audio_b64 = resp_json[0]
        audio_bytes = base64.b64decode(audio_b64)
        return {"audio": audio_bytes, "status_code": response.status_code}


class GeminiSession:
    """
    Chat data to retrieve conversation history. Only if all 3 ids are provided will the conversation history be retrieved.

    Parameters
    ----------
    gemini: `Gemini`
        Gemini client interface for https://gemini.google.com/
    metadata: `list[str]`, optional
        List of chat metadata `[cid, rid, rcid]`, can be shorter than 3 elements, like `[cid, rid]` or `[cid]` only
    cid: `str`, optional
        Chat id, if provided together with metadata, will override the first value in it
    rid: `str`, optional
        Reply id, if provided together with metadata, will override the second value in it
    rcid: `str`, optional
        Reply candidate id, if provided together with metadata, will override the third value in it
    """

    # @properties needn't have their slots pre-defined
    __slots__ = ["__metadata", "gemini", "gemini_output"]

    def __init__(
        self,
        gemini: Gemini,
        metadata: Optional[list[str]] = None,
        cid: Optional[str] = None,  # chat id
        rid: Optional[str] = None,  # reply id
        rcid: Optional[str] = None,  # reply candidate id
    ):
        self.__metadata: list[Optional[str]] = [None, None, None]
        self.gemini: Gemini = gemini
        self.gemini_output: Optional[GeminiOutput] = None

        if metadata:
            self.metadata = metadata
        if cid:
            self.cid = cid
        if rid:
            self.rid = rid
        if rcid:
            self.rcid = rcid

    def __str__(self):
        return f"GeminiSession(cid='{self.cid}', rid='{self.rid}', rcid='{self.rcid}')"

    __repr__ = __str__

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name == "gemini_output" and isinstance(value, GeminiOutput):
            self.metadata = value.metadata
            self.rcid = value.rcid

    def send_message(self, prompt: str) -> GeminiOutput:
        """
        Generates contents with prompt.
        Use as a shortcut for `Gemini.generate_content(prompt, self)`.

        Parameters
        ----------
        prompt: `str`
            Prompt provided by user

        Returns
        -------
        :class:`GeminiOutput`
            Output data from gemini.google.com, use `GeminiOutput.text` to get the default text reply, `GeminiOutput.images` to get a list
            of images in the default reply, `GeminiOutput.candidates` to get a list of all answer candidates in the gemini_output
        """
        return self.gemini.generate_content(prompt, self)

    def choose_candidate(self, index: int) -> GeminiOutput:
        """
        Choose a candidate from the last `GeminiOutput` to control the ongoing conversation flow.

        Parameters
        ----------
        index: `int`
            Index of the candidate to choose, starting from 0
        """
        if not self.gemini_output:
            raise ValueError(
                "No previous gemini_output data found in this chat session."
            )

        if index >= len(self.gemini_output.candidates):
            raise ValueError(
                f"Index {index} exceeds the number of candidates in last model gemini_output."
            )

        self.gemini_output.chosen = index
        self.rcid = self.gemini_output.rcid
        return self.gemini_output

    @property
    def metadata(self):
        return self.__metadata

    @metadata.setter
    def metadata(self, value: list[str]):
        if len(value) > 3:
            raise ValueError("metadata cannot exceed 3 elements")
        self.__metadata[: len(value)] = value

    @property
    def cid(self):
        return self.__metadata[0]

    @cid.setter
    def cid(self, value: str):
        self.__metadata[0] = value

    @property
    def rid(self):
        return self.__metadata[1]

    @rid.setter
    def rid(self, value: str):
        self.__metadata[1] = value

    @property
    def rcid(self):
        return self.__metadata[2]

    @rcid.setter
    def rcid(self, value: str):
        self.__metadata[2] = value
