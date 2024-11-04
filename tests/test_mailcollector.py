# Copyright 2024 Timo Kankare <timo.kankare@iki.fi>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#

"""Test cases for MailCollector."""

import pytest
from Mailnag.daemon.mails import MailCollector
from fakeaccount import FakeAccount


message_template = """\
From: You <you@example.org>
To: Me <me@example.org>
Subject: {subject}
Message-ID: mid-123456
Date: Tue, 01 May 2018 16:28:08 +0300

...World!
"""


def test_no_accounts():
    # GIVEN
    mc = MailCollector(None, [])

    # WHEN
    mails = mc.collect_mail()

    # THEN
    assert mails == []


def test_one_account_no_mails():
    # GIVEN
    acc = FakeAccount()
    mc = MailCollector(None, [acc])

    # WHEN
    mails = mc.collect_mail()

    # THEN
    assert mails == []

@pytest.mark.parametrize('input_subject,expected_subject',
    [
        ("", ""),
        ("abc", "abc"),
        ("=?iso-8859-1?q?this is some text?=", "this is some text"),
        ("=?iso-8859-1?q?this=20is=20some=20text?=", "this is some text"),
        ("=?ISO-8859-1?Q?a?=", "a"),
        ("=?ISO-8859-1?Q?a?= b", "a b"),
        ("=?ISO-8859-1?Q?a?= =?ISO-8859-1?Q?b?=", "ab"),
        ("=?ISO-8859-1?Q?a?==?ISO-8859-1?Q?b?=", "ab"),
        ("=?ISO-8859-1?Q?a?=  =?ISO-8859-1?Q?b?=", "ab"),
        ("=?ISO-8859-1?Q?a_b?=", "a b"),
        ("a =?ISO-8859-1?Q?b?=", "a b"),
    ]
)
def test_collector_should_parse_subjects_correctly(input_subject, expected_subject):
    # GIVEN
    acc = FakeAccount()
    acc.set_current_messages([message_template.format(subject=input_subject)])
    mc = MailCollector(None, [acc])

    # WHEN
    mails = mc.collect_mail()

    # THEN
    assert len(mails) == 1
    mail = mails[0]
    assert mail.subject == expected_subject
#    assert False, "WIP"


# TODO: collector_should_open_account
# TODO: collector_should_close_account

