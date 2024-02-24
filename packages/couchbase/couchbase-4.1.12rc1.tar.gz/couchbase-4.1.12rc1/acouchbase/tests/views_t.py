#  Copyright 2016-2023. Couchbase, Inc.
#  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License")
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from datetime import timedelta

import pytest
import pytest_asyncio

from couchbase.exceptions import AmbiguousTimeoutException, DesignDocumentNotFoundException
from couchbase.management.views import DesignDocumentNamespace
from couchbase.options import ViewOptions
from couchbase.views import ViewMetaData, ViewOrdering
from tests.environments import CollectionType
from tests.environments.views_environment import AsyncViewsTestEnvironment


class ViewsTestSuite:
    TEST_MANIFEST = [
        'test_bad_view_query',
        'test_view_query',
        'test_view_query_ascending',
        'test_view_query_descending',
        'test_view_query_endkey',
        'test_view_query_endkey_docid',
        'test_view_query_key',
        'test_view_query_keys',
        'test_view_query_startkey',
        'test_view_query_startkey_docid',
        'test_view_query_timeout',
    ]

    @pytest.mark.asyncio
    async def test_bad_view_query(self, cb_env):
        view_result = cb_env.bucket.view_query('fake-ddoc',
                                               'fake-view',
                                               limit=10,
                                               namespace=DesignDocumentNamespace.DEVELOPMENT)

        with pytest.raises(DesignDocumentNotFoundException):
            [r async for r in view_result]

    @pytest.mark.asyncio
    async def test_view_query(self, cb_env):

        expected_count = 10
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               limit=expected_count,
                                               namespace=DesignDocumentNamespace.DEVELOPMENT)

        await cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    @pytest.mark.asyncio
    async def test_view_query_ascending(self, cb_env):

        expected_count = 10
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               limit=expected_count,
                                               namespace=DesignDocumentNamespace.DEVELOPMENT,
                                               order=ViewOrdering.ASCENDING)

        rows = await cb_env.assert_rows(view_result, expected_count, return_rows=True)
        results = list(map(lambda r: r.key, rows))
        sorted_results = sorted(results, key=lambda x: x[0], reverse=True)
        assert results == sorted_results

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    @pytest.mark.asyncio
    async def test_view_query_descending(self, cb_env):
        expected_count = 10
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               limit=expected_count,
                                               namespace=DesignDocumentNamespace.DEVELOPMENT,
                                               order=ViewOrdering.DESCENDING)

        rows = await cb_env.assert_rows(view_result, expected_count, return_rows=True)
        results = list(map(lambda r: r.key, rows))
        sorted_results = sorted(results, key=lambda x: x[0])
        assert results == sorted_results

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    @pytest.mark.asyncio
    async def test_view_query_endkey(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 5
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           endkey=[f'{batch_id}::10', f'{batch_id}::20'])
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        await cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    @pytest.mark.asyncio
    async def test_view_query_endkey_docid(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 5
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           endkey_docid=f'{batch_id}::15')
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        await cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    @pytest.mark.asyncio
    async def test_view_query_key(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 1
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           key=[f'{batch_id}', f'{batch_id}::10'])
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        await cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    @pytest.mark.asyncio
    async def test_view_query_keys(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 5
        keys = [[f'{batch_id}', f'{batch_id}::0'],
                [f'{batch_id}', f'{batch_id}::1'],
                [f'{batch_id}', f'{batch_id}::2'],
                [f'{batch_id}', f'{batch_id}::3'],
                [f'{batch_id}', f'{batch_id}::4']]
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           keys=keys)
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        await cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    @pytest.mark.asyncio
    async def test_view_query_startkey(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 5
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           startkey=[f'{batch_id}', f'{batch_id}::0'])
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        await cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    @pytest.mark.asyncio
    async def test_view_query_startkey_docid(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 5
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           startkey_docid=f'{batch_id}::0')
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        await cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    # creating a new connection, allow retries
    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    @pytest.mark.asyncio
    async def test_view_query_timeout(self, cb_env):
        from acouchbase.cluster import Cluster
        from couchbase.auth import PasswordAuthenticator
        from couchbase.options import ClusterOptions, ClusterTimeoutOptions
        conn_string = cb_env.config.get_connection_string()
        username, pw = cb_env.config.get_username_and_pw()
        auth = PasswordAuthenticator(username, pw)
        # Prior to PYCBC-1521, this test would fail as each request would override the cluster level views_timeout.
        # If a timeout was not provided in the request, the default 75s timeout would be used.  PYCBC-1521 corrects
        # this behavior so this test will pass as we are essentially forcing an AmbiguousTimeoutException because
        # we are setting the cluster level views_timeout such a small value.
        timeout_opts = ClusterTimeoutOptions(views_timeout=timedelta(milliseconds=1))
        cluster = await Cluster.connect(f'{conn_string}', ClusterOptions(auth, timeout_options=timeout_opts))
        # don't need to do this except for older server versions
        bucket = cluster.bucket(f'{cb_env.bucket.name}')
        with pytest.raises(AmbiguousTimeoutException):
            res = bucket.view_query(cb_env.DOCNAME,
                                    cb_env.TEST_VIEW_NAME,
                                    limit=10,
                                    namespace=DesignDocumentNamespace.DEVELOPMENT)
            [r async for r in res.rows()]
        # if we override the timeout w/in the request the query should succeed.
        res = bucket.view_query(cb_env.DOCNAME,
                                cb_env.TEST_VIEW_NAME,
                                limit=10,
                                namespace=DesignDocumentNamespace.DEVELOPMENT,
                                timeout=timedelta(seconds=10))
        rows = [r async for r in res.rows()]
        assert len(rows) > 0


class ClassicViewsTests(ViewsTestSuite):
    @pytest.fixture(scope='class')
    def test_manifest_validated(self):
        def valid_test_method(meth):
            attr = getattr(ClassicViewsTests, meth)
            return callable(attr) and not meth.startswith('__') and meth.startswith('test')
        method_list = [meth for meth in dir(ClassicViewsTests) if valid_test_method(meth)]
        compare = set(ViewsTestSuite.TEST_MANIFEST).difference(method_list)
        return compare

    @pytest_asyncio.fixture(scope='class', name='cb_env', params=[CollectionType.DEFAULT])
    async def couchbase_test_environment(self, acb_base_env, test_manifest_validated, request):
        if test_manifest_validated:
            pytest.fail(f'Test manifest not validated.  Missing tests: {test_manifest_validated}.')

        acb_env = AsyncViewsTestEnvironment.from_environment(acb_base_env)
        acb_env.enable_views_mgmt()
        await acb_env.setup(request.param)
        yield acb_env
        await acb_env.teardown(request.param)
