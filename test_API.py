#!/usr/bin/env python


"""test_API.py: This test suite is for testing the Gitbhub API for repositories
    Python version 2.7.10
    To run test suite enter: pytest test_API.py"""

from requests import get
from requests.auth import HTTPBasicAuth

__author__ = "Azfar Ahmed"
__version__ = "1.00"
__email__ = "ahmedaz100@yahoo.com"


class TestAPI:
    base_url = 'https://api.github.com'         # Base URL for endpoint
    username = 'username'             # update with valid username
    password = 'password'              # update with valid password
    headers = {'content-type': 'application/json'}      # header for content type

# test for authentication with invalid password
    def test_authentication_invalid_password(self):
        print 'Invalid authentication test'
        user_url = self.base_url + '/Users/azahmed100'
        response = get(user_url, auth=HTTPBasicAuth(self.username, 'wrong password'), headers=self.headers,
                       allow_redirects=True)
        assert response.status_code == 401, "Did not return HTTP code 401"
        print response.content

# test for authentication with valid credentials
    def test_authentication_valid(self):
        print 'Valid authentication test'
        user_url = self.base_url + '/users/azahmed100'

        # expected response for the API call
        expected_response = \
            {
                "login": "azahmed100",
                "id": "35506085",
                "node_id": "MDQ6VXNlcjM1NTA2MDg1",
                "avatar_url": "https://avatars0.githubusercontent.com/u/35506085?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/azahmed100",
                "html_url": "https://github.com/azahmed100",
                "followers_url": "https://api.github.com/users/azahmed100/followers",
                "following_url": "https://api.github.com/users/azahmed100/following{/other_user}",
                "gists_url": "https://api.github.com/users/azahmed100/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/azahmed100/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/azahmed100/subscriptions",
                "organizations_url": "https://api.github.com/users/azahmed100/orgs",
                "repos_url": "https://api.github.com/users/azahmed100/repos",
                "events_url": "https://api.github.com/users/azahmed100/events{/privacy}",
                "received_events_url": "https://api.github.com/users/azahmed100/received_events",
                "type": "User",
                "site_admin": "False",
                "name": "None",
                "company": "None",
                "blog": "",
                "location": "None",
                "email": "None",
                "hireable": "None",
                "bio": "None",
                "public_repos": "0",
                "public_gists": "0",
                "followers": "0",
                "following": "0",
                "created_at": "2018-01-16T20:38:21Z",
                "updated_at": "2018-06-21T21:55:33Z"
            }
        parsed_expected_response = dict(expected_response)      # parse expected response to dict
        response = get(user_url, auth=HTTPBasicAuth(self.username, self.password), headers=self.headers,
                       allow_redirects=True)
        assert response.status_code == 200, "Did not return HTTP code 200 "
        response_data = response.json()         # parse json response as dict

        # Compare expected key values with response key values
        for k, v in parsed_expected_response.iteritems():
            print "key: ", str(k), "value: ", str(v), "/n"
            assert str(response_data[k]) == str(v), "expected value not equivalent for " + k
        print response.text

# test querying a topic
    def test_query_topic(self):
        print 'Query by topic'
        query_url = self.base_url + '/search/repositories?q=topic:ruby+topic:rails'
        response = get(query_url, headers=self.headers, allow_redirects=True)
        # print parsed
        print response.text
        data = response.json()      # parse json response as dict
        assert response.status_code == 200, "Did not return http code 200"
        assert data['total_count'] > 0, "Did not return any results"

# test query with sorting
    def test_query_sort(self):
        print 'Query and sort by id'
        query_url = self.base_url + '/search/repositories?q=tetris+language:python&sort=stars&order=desc'
        response = get(query_url, headers=self.headers, allow_redirects=True)
        print response.text
        # print 'Link: ' + response.headers['Link']
        data = response.json()      # parse json response as dict
        assert response.status_code == 200, "Did not return http code 200"
        assert data['total_count'] > 0, "Did not return any results"

        # Verify that the results are in descending order for the sort for the first 20
        for x in xrange(0, 19):
            assert data['items'][x]['stargazers_count'] >= data['items'][x+1]['stargazers_count'], \
                "Sort is not in descending order"

# test query with pagination
    def test_query_pagination(self):
        print 'Query and pagination'
        query_url = self.base_url + '/search/repositories?q=tetris+language:python&page=2&per_page=100'
        # pagination is returned as header
        expected_link_header = \
        '<https://api.github.com/search/repositories?q=tetris+language%3Apython&page=1&per_page=100>; ' \
        'rel="prev", <https://api.github.com/search/repositories?q=tetris+language%3Apython&page=3&per_page=100>; ' \
        'rel="next", <https://api.github.com/search/repositories?q=tetris+language%3Apython&page=10&per_page=100>; ' \
        'rel="last", <https://api.github.com/search/repositories?q=tetris+language%3Apython&page=1&per_page=100>; ' \
        'rel="first"'
        response = get(query_url, headers=self.headers, allow_redirects=True)
        data = response.json()      # parse json response as dict
        print response.text
        assert response.status_code == 200, "Did not return http code 200"
        assert data['total_count'] > 0, "Did not return any results"
        # The Link header includes pagination information
        print response.headers['Link']

        # Verify pagination is as expected
        assert response.headers['Link'] == expected_link_header

# test query issues
    def test_query_issues(self):
        print 'Query by issues'
        query_url = self.base_url + '/search/issues?q=state:open&sort=created&order=asc'
        response = get(query_url, headers=self.headers, allow_redirects=True)
        data = response.json()      # parse json response as dict
        assert response.status_code == 200, "Did not return http code 200"
        assert data['total_count'] > 0, "Did not return any results"

# test query codes
    def test_query_code(self):
        print 'Query for codes'
        query_url = self.base_url + '/search/code?q=addClass+in:file+language:js+repo:jquery/jquery'
        response = get(query_url, headers=self.headers, allow_redirects=True)
        data = response.json()      # parse json response as dict
        assert response.status_code == 200, "Did not return http code 200"
        assert data['total_count'] > 0, "Did not return any results"

# test query users
    def test_search_users(self):
        print 'Query for users'
        query_url = self.base_url + '/search/users?q=tom+repos:%3E42+followers:%3E1000'
        response = get(query_url, headers=self.headers, allow_redirects=True)
        data = response.json()  # parse json response as dict
        assert response.status_code == 200, "Did not return http code 200"
        assert data['total_count'] > 0, "Did not return any results"

# test query commits
    def test_query_commits(self):
        print "Query by commits"
        headers = {'Accept': 'application/vnd.github.cloak-preview'}        # required header for request
        query_url = self.base_url + '/search/commits?q=repo:octocat/Spoon-Knife+css'
        response = get(query_url, auth=HTTPBasicAuth(self.username, self.password),
                       headers=headers, allow_redirects=True)
        assert response.content != '', "Did not return results"
        assert response.status_code == 200, "Did not return HTTP code 200"
        print response.content

# test query labels
    def test_search_labels(self):
        print 'Query for search labels'
        headers = {'Accept': 'application/vnd.github.symmetra-preview+json'}    # header to query labels
        query_url = self.base_url + '/search/labels?repository_id=64778136&q=bug+defect+enhancement'
        response = get(query_url, headers=headers, allow_redirects=True)
        data = response.json()  # parse json response as dict
        assert response.status_code == 200, "Did not return http code 200"
        assert data['total_count'] > 0, "Did not return any results"
        print response.content

# test query labels with highlights
    def test_search_labels_highlight(self):
        print 'Query labels with highlights'
        headers = {'Accept': 'application/vnd.github.v3.text-match+json',
                   'Accept': 'application/vnd.github.symmetra-preview+json'}    # header for highlight labels query
        query_url = self.base_url + '/search/labels?repository_id=64778136&q=bug+defect+enhancement'
        response = get(query_url, headers=headers, allow_redirects=True)
        data = response.json()      # parse json response as dict
        # Verify values
        assert response.status_code == 200, "Did not return http code 200"
        assert data['total_count'] > 0, "Did not return any results"
        assert data['items'][0]['url'] == "https://api.github.com/repos/octocat/linguist/labels/enhancement"
        assert data['items'][0]['name'] == 'enhancement'
        assert data['items'][0]['color'] == '84b6eb'
        print response.content

# test query text match metadata
    def test_search_text_match_metadata(self):
        print 'Query text match metadata'
        headers = {'Accept': 'application/vnd.github.v3.text-match+json'}   # header to highlight labels
        query_url = self.base_url + '/search/issues?q=windows+label:' \
                                    'bug+language:python+state:open&sort=created&order=asc'

        expected_response_labels = \
            {
                "id": "84627441,",
                "url": "https://api.github.com/repos/ansible/ansible/labels/affects_2.7",
                "name": "bug",
                "color": "ededed",
                "default": "true",
                "description": "",
                "node_id": "MDU6TGFiZWw4NDYyNzM0NA=="
            }

        parsed_expected_response_labels = dict(expected_response_labels)      # parse expected response to dict
        response = get(query_url, headers=headers, allow_redirects=True)
        response_data = response.json()     # parse json response as dict
        # verify response data
        assert response.status_code == 200, "Did not return http code 200"
        assert response_data['total_count'] > 0, "Did not return any results"
        assert response_data['items'][0]['labels'][0]['node_id'] == parsed_expected_response_labels['node_id'], \
            "incorrect value of labels node_id"
        assert response_data['items'][0]['labels'][0]['name'] == expected_response_labels['name'], \
            "incorrect value of labels name"
        assert response_data['items'][0]['labels'][0]['color'] == expected_response_labels['color'], \
            " incorrect value of labels color"

        print response.content
