#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from pages.feedback import FeedbackPage


class AndroidFeedbackFormPage(FeedbackPage):
    _page_title = 'Firefox Feedback :: Firefox Input'

    def go_to_feedback_page(self, version='', channel='',
                            last_visited='', in_device=False):
        url = self.base_url + '/feedback/android'
        params = []

        if version:
            url = url + '/' + version

        if channel:
            url = url + '/' + channel

        if in_device:
            params.append('utm_source=feedback-prompt')

        if last_visited:
            params.append('url=%s' % (last_visited))

        if len(params) > 0:
            params = '&'.join(params)
            url = url + '/?' + params

        self.selenium.get(url)
        self.is_the_current_page

    # Intro card
    _happy_button_locator = (By.ID, 'happy-button')
    _sad_button_locator = (By.ID, 'sad-button')

    def click_happy_feedback(self):
        self.selenium.find_element(*self._happy_button_locator).click()

    # Happy thanks
    _playstore_locator = (By.ID, 'play-store')

    @property
    def playstore_link_is_http_release(self):
        href = self.selenium.find_element(
            *self._playstore_locator
        ).get_attribute('href')
        return href == 'https://play.google.com/store/apps/details?id=org.mozilla.firefox#details-reviews'

    @property
    def playstore_link_is_intent_release(self):
        href = self.selenium.find_element(
            *self._playstore_locator
        ).get_attribute('href')
        return href == 'market://details?id=org.mozilla.firefox'

    @property
    def playstore_link_is_intent_beta(self):
        href = self.selenium.find_element(
            *self._playstore_locator
        ).get_attribute('href')
        return href == 'market://details?id=org.mozilla.firefox_beta'

    @property
    def on_device_links_present(self):
        if (self.is_element_visible_no_wait((By.ID, 'maybe-later')) and
                self.is_element_visible_no_wait((By.ID, 'no-thanks'))):
                    return True

        return False

    def click_sad_feedback(self):
        self.selenium.find_element(*self._sad_button_locator).click()
        self.wait_for(self._moreinfo_text_locator)

    # Moreinfo card
    _moreinfo_text_locator = (By.ID, 'description')
    _url_locator = (By.ID, 'id_url')
    _submit_locator = (By.ID, 'form-submit-btn')
    _checkbox_locator = (By.ID, 'last-checkbox')

    def set_description(self, text):
        desc = self.selenium.find_element(*self._moreinfo_text_locator)
        desc.clear()
        desc.send_keys(text)

    @property
    def is_submit_enabled(self):
        return self.selenium.find_element(*self._submit_locator).is_enabled()

    @property
    def support_link_present(self):
        return self.is_element_visible_no_wait(
            (By.CSS_SELECTOR, '.footer.sad .help-section a')
        )

    def url_prepopulated(self):
        contents = self.selenium.find_element(
            *self._url_locator
        ).get_attribute("value")
        return contents

    def set_url(self, text):
        url = self.selenium.find_element(*self._url_locator)
        url.clear()
        url.send_keys(text)

    def uncheck_url(self):
        self.selenium.find_element(*self._checkbox_locator).click()

    _thanks_locator = (By.ID, 'thanks')

    def submit(self, expect_success=True):
        self.selenium.find_element(*self._submit_locator).click()
        if expect_success:
            self.wait_for((By.ID, 'thanks'))

    @property
    def current_card(self):
        for card in ('intro', 'moreinfo', 'thanks'):
            if self.is_element_visible_no_wait((By.ID, card)):
                return card

    @property
    def current_sentiment(self):
        for sentiment in ('happy', 'sad'):
            if self.is_element_visible_no_wait((By.CSS_SELECTOR, '#moreinfo .' + sentiment)):
                return sentiment
