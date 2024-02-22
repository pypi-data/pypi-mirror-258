#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.02.20 19:00:00                  #
# ================================================== #

import json
import ssl

import re
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import quote


class WebSearch:
    def __init__(self, plugin=None):
        """
        Web search

        :param plugin: plugin
        """
        self.plugin = plugin
        self.signals = None

    def url_get(self, url: str) -> bytes:
        """
        Get URL content

        :param url: URL
        :return: data
        """
        req = Request(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'},
        )
        if self.plugin.get_option_value('disable_ssl'):
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            data = urlopen(
                req,
                context=context,
                timeout=self.plugin.get_option_value('timeout'),
            ).read()
        else:
            data = urlopen(
                req,
                timeout=self.plugin.get_option_value('timeout'),
            ).read()
        return data

    def google_search(
            self,
            q: str,
            num: int,
            offset: int = 1
    ) -> list:
        """
        Google search

        :param q: query string
        :param num: number of results
        :param offset: offset
        :return: list of URLs
        """
        key = self.plugin.get_option_value("google_api_key")
        cx = self.plugin.get_option_value("google_api_cx")

        if num < 1:
            num = 1
        if num > 10:
            num = 10

        if num + offset > 100:
            num = 100 - offset

        urls = []
        try:
            url = 'https://www.googleapis.com/customsearch/v1'
            url += '?key=' + str(key)
            url += '&cx=' + str(cx)
            url += '&num=' + str(num)
            url += '&sort=date-sdate:d:s'
            url += '&fields=items(link)'
            url += '&start=' + str(offset)
            url += '&q=' + quote(q)
            self.debug(
                "Plugin: cmd_web_google:google_search: calling API: {}".format(url)
            )
            data = self.url_get(url)
            res = json.loads(data)
            self.debug(
                "Plugin: cmd_web_google:google_search: received response: {}".format(res)
            )
            if 'items' not in res:
                return []
            for item in res['items']:
                urls.append(item['link'])
            self.debug(
                "Plugin: cmd_web_google:google_search [urls]: {}".format(urls)
            )
            return urls
        except Exception as e:
            self.error(e)
            self.debug(
                "Plugin: cmd_web_google:google_search: error: {}".format(e)
            )
            self.log("Error in Google Search: " + str(e))
        return []

    def get_urls(self, query: str) -> list:
        """
        Search the web and returns URLs

        :param query: query string
        :return: list of founded URLs
        """
        return self.google_search(
            query,
            int(self.plugin.get_option_value("num_pages")),
        )

    def query_url(self, url: str) -> str:
        """
        Query a URL and return the text content

        :param url: URL to query
        :return: text content
        """
        self.debug(
            "Plugin: cmd_web_google:query_url: crawling URL: {}".format(url)
        )
        text = ''
        html = ''
        try:
            data = self.url_get(url)
            # try to decode
            try:
                html = data.decode("utf-8")
            except Exception as e:
                pass

            if html:
                soup = BeautifulSoup(html, "html.parser")
                for element in soup.find_all('html'):
                    text += element.text
                text = text.replace("\n", " ").replace("\t", " ")
                text = re.sub(r'\s+', ' ', text)
                self.debug(
                    "Plugin: cmd_web_google:query_url: received text: {}".format(text)
                )
                return text
        except Exception as e:
            self.error(e)
            self.debug(
                "Plugin: cmd_web_google:query_url: error querying: {}".format(url)
            )
            self.log("Error in query_web: " + str(e))

    def to_chunks(
            self,
            text: str,
            chunk_size: int
    ) -> list:
        """
        Split text into chunks

        :param text: text to split
        :param chunk_size: chunk size
        :return: list of chunks
        """
        if text is None or text == "":
            return []
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    def get_summarized_text(
            self,
            chunks: list,
            query: str,
            summarize_prompt: str = None
    ) -> str:
        """
        Get summarized text from chunks

        :param chunks: chunks of text
        :param query: query string
        :param summarize_prompt: custom summarize prompt
        :return: summarized text
        """
        summary = ""
        sys_prompt = "Summarize text in English in a maximum of 3 paragraphs, trying to find the most important " \
                     "content that can help answer the following question: {query}".format(query=query)

        # get custom prompt if set
        custom_summarize = self.plugin.get_option_value('prompt_summarize')
        if custom_summarize is not None and custom_summarize != "":
            sys_prompt = str(custom_summarize.format(query=query))
        max_tokens = int(self.plugin.get_option_value("summary_max_tokens"))

        # custom summarize prompt
        if summarize_prompt is not None and summarize_prompt != "":
            sys_prompt = summarize_prompt
        else:
            if query is None or query == "":
                sys_prompt = str(self.plugin.get_option_value(
                    'prompt_summarize_url'
                ).format(query=query))

        # get model
        model = self.plugin.window.core.models.from_defaults()
        tmp_model = self.plugin.get_option_value("summary_model")
        if self.plugin.window.core.models.has(tmp_model):
            model = self.plugin.window.core.models.get(tmp_model)

        # summarize per chunk
        for chunk in chunks:
            # print("Chunk: " + chunk)
            self.debug(
                "Plugin: cmd_web_google:get_summarized_text (chunk, max_tokens): {}, {}".format(chunk, max_tokens)
            )
            try:
                response = self.plugin.window.core.bridge.quick_call(
                    prompt=chunk,
                    system_prompt=sys_prompt,
                    max_tokens=max_tokens,
                    model=model,
                )
                if response is not None and response != "":
                    summary += response
            except Exception as e:
                self.error(e)
                self.debug(
                    "Plugin: cmd_web_google:get_summarized_text: error: {}".format(e)
                )
        return summary

    def make_query(
            self,
            query: str,
            page_no: int = 1,
            summarize_prompt: str = ""
    ) -> (str, int, int, str):
        """
        Get result from search query

        :param query: query to search
        :param page_no: page number
        :param summarize_prompt: custom prompt
        :return: result, total_found, current, url
        """
        self.log("Using web query: " + query)
        urls = self.get_urls(query)

        # get options
        max_per_page = int(self.plugin.get_option_value("max_page_content_length"))
        chunk_size = int(self.plugin.get_option_value("chunk_size"))
        max_result_size = int(self.plugin.get_option_value("max_result_length"))

        total_found = len(urls)
        result = ""
        i = 1
        current = 1
        url = ""
        for url in urls:
            if url is None or url == "":
                continue

            # check if requested page number
            if current != page_no:
                current += 1
                continue

            self.log("Web attempt: " + str(i) + " of " + str(len(urls)))
            self.log("URL: " + url)
            content = self.query_url(url)
            if content is None or content == "":
                i += 1
                continue

            self.log("Content found (chars: {}). Please wait...".format(len(content)))
            if 0 < max_per_page < len(content):
                content = content[:max_per_page]

            chunks = self.to_chunks(content, chunk_size)  # it returns list of chunks
            self.debug(
                "Plugin: cmd_web_google: URL: {}".format(url)
            )
            result = self.get_summarized_text(
                chunks,
                str(query),
                summarize_prompt,
            )
            # if result then stop
            if result is not None and result != "":
                self.log("Summary generated (chars: {})".format(len(result)))

                # index webpage if auto-index is enabled
                self.index_url(url)
                break
            i += 1

        self.debug(
            "Plugin: cmd_web_google: summary: {}".format(result)
        )
        if result is not None:
            self.debug(
                "Plugin: cmd_web_google: summary length: {}".format(len(result))
            )

        if len(result) > max_result_size:
            result = result[:max_result_size]

        self.debug(
            "Plugin: cmd_web_google: result length: {}".format(len(result))
        )

        return \
            result, \
            total_found, \
            current, \
            url

    def open_url(self, url: str, summarize_prompt: str = "") -> (str, str):
        """
        Get result from specified URL

        :param url: URL to visit
        :param summarize_prompt: custom prompt
        :return: result, url
        """
        self.log("Using URL: " + url)

        # get options
        max_per_page = int(self.plugin.get_option_value("max_page_content_length"))
        chunk_size = int(self.plugin.get_option_value("chunk_size"))
        max_result_size = int(self.plugin.get_option_value("max_result_length"))

        self.log("URL: " + url)
        content = self.query_url(url)
        self.log("Content found (chars: {}). Please wait...".format(len(content)))

        # index webpage if auto-index is enabled
        if content:
            self.index_url(url)

        if 0 < max_per_page < len(content):
            content = content[:max_per_page]
        chunks = self.to_chunks(
            content,
            chunk_size,
        )  # it returns list of chunks

        self.debug("Plugin: cmd_web_google: URL: {}".format(url))  # log

        result = self.get_summarized_text(chunks, "", summarize_prompt)

        if result is not None and result != "":
            self.log("Summary generated (chars: {})".format(len(result)))

        self.debug("Plugin: cmd_web_google: summary: {}".format(result))  # log
        if result is not None:
            self.debug(
                "Plugin: cmd_web_google: summary length: {}".format(len(result))
            )

        if len(result) > max_result_size:
            result = result[:max_result_size]

        self.debug(
            "Plugin: cmd_web_google: result length: {}".format(len(result))
        )

        return result, url

    def open_url_raw(self, url: str) -> (str, str):
        """
        Get raw content from specified URL

        :param url: URL to visit
        :return: result, url
        """
        self.log("Using URL: " + url)

        # get options
        max_result_size = int(self.plugin.get_option_value("max_page_content_length"))

        self.log("URL: " + url)
        result = self.query_url(url)
        self.log("Content found (chars: {}). Please wait...".format(len(result)))

        # index webpage if auto-index is enabled
        if result:
            self.index_url(url)

        # strip if too long
        if 0 < max_result_size < len(result):
            result = result[:max_result_size]

        self.debug(
            "Plugin: cmd_web_google: result length: {}".format(len(result))
        )

        return result, url

    def index_url(self, url: str):
        """
        Index URL if auto-index is enabled

        :param url: URL to index
        """
        if not self.plugin.get_option_value("auto_index"):
            return

        self.log("Indexing URL: " + url)
        try:
            num, errors = self.plugin.window.core.idx.index_urls(
                self.plugin.get_option_value("idx"),
                [url],
            )
            if errors:
                self.error(str(errors))
            elif num > 0:
                self.log("Indexed URL: " + url + " to index: " + self.plugin.get_option_value("idx"))
            else:
                self.error("Failed to index URL: " + url)
        except Exception as e:
            self.error(e)

    def error(self, err: any):
        """
        Log error message

        :param err: exception
        """
        if self.signals is not None:
            self.signals.error.emit(err)

    def status(self, msg: str):
        """
        Send status message

        :param msg: status message
        """
        if self.signals is not None:
            self.signals.status.emit(msg)

    def debug(self, msg: str):
        """
        Log debug message

        :param msg: message to log
        """
        if self.signals is not None:
            self.signals.debug.emit(msg)

    def log(self, msg: str):
        """
        Log message

        :param msg: message to log
        """
        if self.signals is not None:
            self.signals.log.emit(msg)
