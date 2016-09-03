#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

import pytest

import wolframalpha


@pytest.fixture(scope='session')
def API_key():
	"""
	To run the tests fully, the environment must be configured
	with a WOLFRAMALPHA_API_KEY environment variable. Otherwise,
	skip them.
	"""
	try:
		return os.environ['WOLFRAMALPHA_API_KEY']
	except KeyError:
		pytest.skip("Need WOLFRAMALPHA_API_KEY in environment")


@pytest.fixture(scope='session')
def client(API_key):
	return wolframalpha.Client(API_key)


@pytest.fixture(scope='module')
def temp_result(client):
	return client.query('30 deg C in deg F')

def test_basic(temp_result):
	res = temp_result
	assert len(list(res.pods)) > 0
	result, = res.results
	assert result.text == '86 °F  (degrees Fahrenheit)'
	assert result.texts == ['86 °F  (degrees Fahrenheit)']


def test_results_iterator(temp_result):
	"""
	A Result.results should be an iterator.
	"""
	res = temp_result
	next(res.results)


def test_properties(temp_result):
	"""
	A result should have a number of properties.
	"""
	res = temp_result
	info = list(res.info)
	warnings = list(res.warnings)
	assert all(isinstance(item, wolframalpha.Warning) for item in warnings)
	assumptions = list(res.assumptions)
	assert all(
		isinstance(item, wolframalpha.Assumption)
		for item in assumptions
	)
	pods = list(res.pods)
	assert all(isinstance(item, wolframalpha.Pod) for item in pods)
	assert len(info) == len(pods) + len(warnings) + len(assumptions)


def test_invalid_app_id():
	client = wolframalpha.Client('abcdefg')
	with pytest.raises(Exception):
		client.query('30 deg C in deg F')
