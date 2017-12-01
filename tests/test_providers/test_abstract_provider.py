import logging
from datetime import datetime
from unittest import TestCase, skipIf

import sys
from unittest.mock import patch, mock_open, call

from tests import MockArgParse, fixture
from tests.test_providers import MockProvider
from virga.providers.abstract import AbstractProvider, SUCCESS


class TestAbstractProvider(TestCase):

    def setUp(self):
        self.arg_parse = MockArgParse(
            debug=False,
            silent=True,
            logfile=None,
            output='/tmp',
            definitions='any'
        )
        self.provider = MockProvider(self.arg_parse)

    def test_abstract_method(self):
        class Provider(AbstractProvider):
            pass
        provider = Provider(MockArgParse(debug=False, silent=False, logfile=None))

        with self.assertRaises(NotImplementedError):
            provider.action()
        with self.assertRaises(NotImplementedError):
            provider.lookup('', '', '')

    @patch('logging.addLevelName')
    def test_set_logger_add_success(self, mock_add_level):
        arg_parse = MockArgParse(debug=False, silent=False, logfile=None)
        provider = MockProvider(arg_parse)
        provider.set_logger(arg_parse)
        mock_add_level.assert_called_once_with(SUCCESS, 'SUCCESS')

    @patch('logging.Formatter')
    def test_set_logger_set_formatter(self, mock_formatter):
        arg_parse = MockArgParse(debug=False, silent=False, logfile=None)
        provider = MockProvider(arg_parse)
        provider.set_logger(arg_parse)
        mock_formatter.assert_called_once_with('%(asctime)s %(levelname)s - %(message)s')

    def test_set_logger_logging_level_info(self):
        arg_parse = MockArgParse(debug=False, silent=False, logfile=None)
        provider = MockProvider(arg_parse)
        provider.set_logger(arg_parse)
        self.assertEqual(logging.INFO, provider.logger.level)

    def test_set_logger_logging_level_debug(self):
        arg_parse = MockArgParse(debug=True, silent=False, logfile=None)
        provider = MockProvider(arg_parse)
        provider.set_logger(arg_parse)
        self.assertEqual(logging.DEBUG, provider.logger.level)

    def test_set_logger_logging_level_silent(self):
        self.provider.set_logger(self.arg_parse)
        self.assertEqual(logging.CRITICAL, self.provider.logger.level)

    @patch('logging.FileHandler')
    @skipIf(sys.platform.startswith('win'), 'Seriously?')
    def test_set_logger_log_on_file(self, mock_file_handler):
        arg_parse = MockArgParse(debug=False, silent=True, logfile='/dev/null')
        provider = MockProvider(arg_parse)
        provider.set_logger(arg_parse)
        mock_file_handler.assert_called_once_with('/dev/null')

    @patch('logging.StreamHandler')
    def test_set_logger_log_on_stream(self, mock_stream_handler):
        self.provider.set_logger(self.arg_parse)
        mock_stream_handler.assert_called_once_with()

    @patch('logging.getLogger')
    def test_set_logger_instantiate_the_logger(self, mock_get_logger):
        self.provider.set_logger(self.arg_parse)
        mock_get_logger.assert_called_once_with('virga.providers.abstract')
        self.assertIsNotNone(self.provider.logger)

    @patch('logging.Logger.setLevel')
    @patch('logging.Logger.addHandler')
    def test_set_logger_set_the_logger_properties(self, mock_add_handler, mock_set_level):
        self.provider.set_logger(self.arg_parse)
        mock_add_handler.assert_called_once()
        mock_set_level.assert_called_once_with(logging.CRITICAL)

    @patch('virga.providers.abstract.AbstractProvider.set_logger')
    def test_logs_instantiate_the_logger_if_it_is_none(self, mock_set_logger):
        self.provider.logs([{}])
        mock_set_logger.assert_called_once_with(self.arg_parse)

    @patch('logging.Logger.log')
    def test_logs_empty_outcomes(self, mock_log):
        self.provider.logs([])
        mock_log.assert_not_called()

    @patch('logging.Logger.log')
    def test_logs_outcomes_success(self, mock_log):
        self.provider.logs([{
            'level': SUCCESS,
            'message': 'Success'
        }])
        mock_log.assert_called_once_with(SUCCESS, 'Success')

    @patch('logging.Logger.log')
    def test_logs_outcomes_failure(self, mock_log):
        self.provider.logs([{
            'level': logging.ERROR,
            'message': 'Failure'
        }])
        mock_log.assert_called_once_with(logging.ERROR, 'Failure')

    @patch('logging.Logger.log')
    def test_logs_default_outcomes_failure(self, mock_log):
        self.provider.logs([{}])
        mock_log.assert_called_once_with(logging.CRITICAL, 'No message')

    def test_flatten_empty_list(self):
        self.assertListEqual([], self.provider.flatten([]))

    def test_flatten_one_string(self):
        self.assertListEqual(['t1'], self.provider.flatten('t1'))

    def test_flatten_one_none(self):
        self.assertListEqual([None], self.provider.flatten(None))

    def test_flatten_list_one_level(self):
        self.assertListEqual(['t1', 't2', 't3'], self.provider.flatten(['t1', 't2', 't3']))

    def test_flatten_list_one_level_multiple_types(self):
        self.assertListEqual(['t1', None, False], self.provider.flatten(['t1', None, False]))

    def test_flatten_list_two_levels(self):
        data = [
            ['t1', 't2', 't3'],
            ['t4', 't5', 't6'],
        ]
        expected = ['t1', 't2', 't3', 't4', 't5', 't6']
        self.assertListEqual(expected, self.provider.flatten(data))

    def test_flatten_list_three_levels(self):
        data = [
            ['t1', 't2', ['t3', 't4']],
            ['t5', ['t6', 't7', 't8'], ['t9', None]],
        ]
        expected = ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', None]
        self.assertListEqual(expected, self.provider.flatten(data))

    def test_outcome_result_none(self):
        self.assertFalse(self.provider.outcome(None))

    @patch('virga.providers.abstract.AbstractProvider.flatten')
    def test_outcome_flatten_result(self, mock_flatten):
        self.provider.outcome('any')
        mock_flatten.called_once_with('any')

    def test_outcome_result_empty(self):
        self.assertFalse(self.provider.outcome([]))

    def test_outcome_all_result_are_none(self):
        self.assertFalse(self.provider.outcome([None, None]))

    def test_outcome_all_result_are_false(self):
        self.assertFalse(self.provider.outcome([False, False]))

    def test_outcome_all_result_are_empty(self):
        self.assertFalse(self.provider.outcome(['', '']))

    def test_outcome_any_result_exists(self):
        self.assertTrue(self.provider.outcome(['test', '']))

    def test_lookup_not_there(self):
        data = 'Any=`any`'
        self.assertEqual(data, self.provider._lookup(data))

    # mocking the mock!!!
    @patch('tests.test_providers.MockProvider.lookup')
    def test_lookup_with_one_lookup(self, mock_lookup):
        mock_lookup.return_value = 'lookup-return'
        data = 'Any=`_lookup(section, identifier, id)`'
        expected = 'Any=`lookup-return`'
        self.assertEqual(expected, self.provider._lookup(data))

    @patch('tests.test_providers.MockProvider.lookup')
    def test_lookup_with_multiple_lookups(self, mock_lookup):
        mock_lookup.return_value = 'lookup-return'
        data = 'Any=`_lookup(section_1, identifier1, id-1)` && Any=`_lookup(section_2, identifier2, id-2)`'
        expected = 'Any=`lookup-return` && Any=`lookup-return`'
        self.assertEqual(expected, self.provider._lookup(data))

    @patch('builtins.open', new_callable=mock_open)
    def test_output_save_resource_on_file(self, mock_opened):
        data = {
            'k1': 'v1',
            'k2': 'v2'
        }
        # this one is copied from the debug
        # I expected the calls where split only by the CR
        expected = [
            call('{'), call('\n  '),
            call('"k1"'), call(': '), call('"v1"'), call(',\n  '),
            call('"k2"'), call(': '), call('"v2"'), call('\n'),
            call('}')
        ]
        self.provider.output(data, 'any')
        mock_opened.assert_called_once_with('/tmp/any.json', 'w')
        handle = mock_opened()
        handle.write.assert_has_calls(expected)

    @patch('builtins.open', new_callable=mock_open)
    def test_output_save_resource_with_datetime(self, mock_opened):
        data = {
            'k1': 'v1',
            'k2': datetime(2015, 1, 1, 12, 30, 59)
        }
        expected = [
            call('{'), call('\n  '),
            call('"k1"'), call(': '), call('"v1"'), call(',\n  '),
            call('"k2"'), call(': '), call('"2015-01-01T12:30:59"'), call('\n'),
            call('}')
        ]
        self.provider.output(data, 'any')
        mock_opened.assert_called_once_with('/tmp/any.json', 'w')
        handle = mock_opened()
        handle.write.assert_has_calls(expected)

    @patch('virga.providers.abstract.AbstractProvider.output')
    def test_assertion_call_output(self, mock_output):
        self.provider.assertion("AnyKey=='any-value'", 'Context', {}, 'resource-id')
        mock_output.assert_called_once_with({}, 'resource-id')

    @patch('virga.providers.abstract.AbstractProvider._lookup')
    def test_assertion_call_lookup(self, mock_lookup):
        mock_lookup.return_value = "AnyKey=='any-value'"
        self.provider.assertion("AnyKey=='any-value'", 'Context', {}, 'resource-id')
        mock_lookup.assert_called_once_with("AnyKey=='any-value'")

    @patch('jmespath.search')
    def test_assertion_call_search(self, mock_search):
        self.provider.assertion("AnyKey=='any-value'", 'Context', {}, 'resource-id')
        mock_search.assert_called_once_with("AnyKey=='any-value'", {})

    @patch('logging.Logger.debug')
    def test_assertion_call_debug(self, mock_debug):
        self.provider.assertion("AnyKey=='any-value'", 'Context', {}, 'resource-id')
        mock_debug.assert_called_once_with("resource-id: AnyKey=='any-value' eval False == False")

    @patch('virga.providers.abstract.AbstractProvider.outcome')
    def test_assertion_call_outcome(self, mock_outcome):
        self.provider.assertion("AnyKey=='any-value'", 'Context', {}, 'resource-id')
        mock_outcome.assert_called_once_with(False)

    @patch('os.listdir', return_value=['bare-valid.yaml'])
    @patch('builtins.open', new_callable=mock_open, read_data=fixture('bare-valid.yaml'))
    def test_definition_file(self, *args):
        self.provider.definitions_path = 'any'
        self.assertDictEqual({'test': 'ok'}, self.provider.definitions)

    @patch('builtins.open', new_callable=mock_open, read_data=fixture('bare-valid.yaml'))
    def test_definition_file_missing(self, *args):
        with self.assertRaisesRegex(NotImplementedError, 'Implement definition_file property'):
            _ = self.provider.definitions

    @patch('sys.stderr.write')
    @patch('sys.exit')
    def test_result_no_messages(self, mock_exit, mock_write):
        self.provider.result([])
        mock_exit.assert_not_called()
        mock_write.assert_not_called()

    @patch('sys.stderr.write')
    @patch('sys.exit')
    def test_result_only_successful_messages(self, mock_exit, mock_write):
        messages = [
            {'success': True},
            {'success': True},
            {'success': True},
        ]
        self.provider.result(messages)
        mock_exit.assert_not_called()
        mock_write.assert_not_called()

    @patch('sys.stderr.write')
    @patch('sys.exit')
    def test_result_only_one_failing_message(self, mock_exit, mock_write):
        messages = [
            {'success': True},
            {'success': True},
            {'success': False},
        ]
        self.provider.result(messages)
        mock_exit.assert_called_once_with(1)
        mock_write.assert_called_once_with('There is an error on 3 tests.\n')

    @patch('sys.stderr.write')
    @patch('sys.exit')
    def test_result_only_failing_messages(self, mock_exit, mock_write):
        messages = [
            {'success': False},
            {'success': False},
            {'success': False},
        ]
        self.provider.result(messages)
        mock_exit.assert_called_once_with(1)
        mock_write.assert_called_once_with('There are 3 errors on 3 tests.\n')
