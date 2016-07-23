import json

import requests
import six


class SlackRequest(object):
    def __init__(self, token):
        self.token = token
        self.connect_timeout = 3.05
        self.read_timeout = 10

    def do(
        self,
        request="?",
        post_data=None,
        domain="slack.com",
        connect_timeout=None,
        read_timeout=None,
    ):
        '''
        Perform a POST request to the Slack Web API

        Args:
            request (str): the method to call from the Slack API. For example: 'channels.list'
            post_data (dict): key/value arguments to pass for the request. For example:
                {'channel': 'CABC12345'}
            domain (str): if for some reason you want to send your request to something other
                than slack.com
        '''
        post_data = post_data or {}

        read_timeout = read_timeout or self.read_timeout
        connect_timeout = connect_timeout or self.connect_timeout

        for k, v in six.iteritems(post_data):
            if not isinstance(v, six.string_types):
                post_data[k] = json.dumps(v)

        url = 'https://{0}/api/{1}'.format(domain, request)
        post_data['token'] = self.token
        files = {'file': post_data.pop('file')} if 'file' in post_data else None

        return requests.post(
            url,
            data=post_data,
            files=files,
            timeout=(connect_timeout, read_timeout, ),
        )
